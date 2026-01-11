"""
Audio assembly service for V2
Assembles TTS segments with background audio
Includes natural pauses, overlap prevention, and smooth transitions
"""

import os
import logging
import tempfile
from typing import List, Dict, Any
from pydub import AudioSegment

logger = logging.getLogger(__name__)


class AudioAssembler:
    """Audio assembly service with natural pacing"""
    
    def __init__(self, job_id: str):
        self.job_id = job_id
        # Configuration for natural speech
        self.MIN_PAUSE_BETWEEN_SEGMENTS = 0.3  # Minimum pause in seconds (300ms)
        self.IDEAL_PAUSE_BETWEEN_SEGMENTS = 0.5  # Ideal pause in seconds (500ms)
        self.FADE_IN_DURATION = 50  # Fade in duration in milliseconds
        self.FADE_OUT_DURATION = 100  # Fade out duration in milliseconds
        self.SEGMENT_PADDING = 0.1  # Small padding at start/end of segments (100ms)
    
    def _add_fade_effects(self, audio: AudioSegment) -> AudioSegment:
        """Add fade in and fade out to audio segment for smooth transitions"""
        # Fade in at the beginning
        audio = audio.fade_in(self.FADE_IN_DURATION)
        # Fade out at the end
        audio = audio.fade_out(self.FADE_OUT_DURATION)
        return audio
    
    def _add_natural_pause(self, audio: AudioSegment, pause_duration_ms: int) -> AudioSegment:
        """Add silence at the end of audio segment for natural breathing room"""
        if pause_duration_ms > 0:
            silence = AudioSegment.silent(duration=pause_duration_ms)
            audio = audio + silence
        return audio
    
    def _calculate_non_overlapping_positions(
        self,
        tts_segments: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Calculate non-overlapping positions for segments with natural pauses
        
        Returns segments with updated final_start_time and final_end_time
        """
        logger.info(f"[JOB {self.job_id}] Calculating non-overlapping positions for {len(tts_segments)} segments")
        
        positioned_segments = []
        current_end_time = 0.0
        
        for i, seg in enumerate(tts_segments):
            if "audio" not in seg:
                # Skip segments without audio
                positioned_segments.append(seg)
                continue
            
            audio = seg["audio"]
            audio_duration = len(audio) / 1000.0  # Convert ms to seconds
            original_start = seg.get("start_time", 0)
            
            # Calculate pause needed
            if i == 0:
                # First segment: start at original time or 0, whichever is later
                final_start = max(0.0, original_start)
            else:
                # Subsequent segments: ensure minimum pause from previous segment
                pause_needed = self.IDEAL_PAUSE_BETWEEN_SEGMENTS
                
                # Try to maintain original timing if possible, but ensure no overlap
                ideal_start = original_start
                min_start = current_end_time + self.MIN_PAUSE_BETWEEN_SEGMENTS
                
                # Use the later of ideal_start or min_start
                final_start = max(ideal_start, min_start)
            
            # Add natural pause at the end of this segment
            pause_duration_ms = int(self.IDEAL_PAUSE_BETWEEN_SEGMENTS * 1000)
            audio_with_pause = self._add_natural_pause(audio, pause_duration_ms)
            
            # Update segment with positioned audio
            seg_copy = seg.copy()
            seg_copy["audio"] = audio_with_pause
            seg_copy["final_start_time"] = final_start
            seg_copy["final_end_time"] = final_start + (len(audio_with_pause) / 1000.0)
            seg_copy["audio_duration"] = len(audio_with_pause) / 1000.0
            
            positioned_segments.append(seg_copy)
            current_end_time = seg_copy["final_end_time"]
            
            logger.debug(
                f"[JOB {self.job_id}] Segment {i+1}: "
                f"original_start={original_start:.2f}s, "
                f"final_start={final_start:.2f}s, "
                f"duration={audio_duration:.2f}s, "
                f"pause={self.IDEAL_PAUSE_BETWEEN_SEGMENTS:.2f}s"
            )
        
        return positioned_segments
    
    async def assemble(
        self,
        tts_segments: List[Dict[str, Any]],
        background_path: str
    ) -> str:
        """
        Assemble TTS segments with background audio
        Includes natural pauses, overlap prevention, and smooth transitions
        
        Args:
            tts_segments: List of segments with audio
            background_path: Path to background audio file
            
        Returns:
            Path to final assembled audio file
        """
        try:
            logger.info(f"[JOB {self.job_id}] Assembling audio from {len(tts_segments)} segments")
            
            # Load background
            background = AudioSegment.from_file(background_path)
            background_duration = len(background) / 1000.0
            
            # Step 1: Calculate non-overlapping positions with natural pauses
            positioned_segments = self._calculate_non_overlapping_positions(tts_segments)
            
            # Step 2: Find total duration needed
            max_end_time = 0.0
            for seg in positioned_segments:
                end_time = seg.get("final_end_time", seg.get("end_time", 0))
                max_end_time = max(max_end_time, end_time)
            
            # Create base track (use background duration or max_end_time, whichever is longer)
            total_duration = max(background_duration, max_end_time)
            total_duration_ms = int(total_duration * 1000)
            assembled_audio = AudioSegment.silent(duration=total_duration_ms)
            
            logger.info(f"[JOB {self.job_id}] Total timeline duration: {total_duration:.2f}s")
            
            # Step 3: Overlay background (quieter)
            assembled_audio = assembled_audio.overlay(background, gain_during_overlay=-6)
            
            # Step 4: Place TTS segments with fade effects
            for i, seg in enumerate(positioned_segments):
                if "audio" not in seg:
                    continue
                
                audio = seg["audio"]
                final_start = seg.get("final_start_time", seg.get("start_time", 0))
                
                # Apply fade in/out for smooth transitions
                audio = self._add_fade_effects(audio)
                
                # Place segment at calculated position
                start_ms = int(final_start * 1000)
                
                # Ensure we don't exceed the timeline
                if start_ms + len(audio) > total_duration_ms:
                    # Trim audio if it exceeds timeline
                    max_audio_length = total_duration_ms - start_ms
                    if max_audio_length > 0:
                        audio = audio[:max_audio_length]
                    else:
                        logger.warning(f"[JOB {self.job_id}] Segment {i+1} exceeds timeline, skipping")
                        continue
                
                # Overlay the segment
                assembled_audio = assembled_audio.overlay(
                    audio,
                    position=start_ms,
                    gain_during_overlay=+3
                )
                
                if (i + 1) % 10 == 0:
                    logger.info(f"[JOB {self.job_id}] Placed {i + 1}/{len(positioned_segments)} segments")
            
            # Step 5: Normalize audio levels to prevent clipping
            # Apply gentle normalization (don't over-compress)
            try:
                # Check if audio is too loud
                if assembled_audio.max_dBFS > -3.0:  # If louder than -3dB
                    # Reduce gain to prevent clipping
                    target_dBFS = -6.0  # Target -6dB for headroom
                    gain_reduction = assembled_audio.max_dBFS - target_dBFS
                    if gain_reduction > 0:
                        assembled_audio = assembled_audio.apply_gain(-gain_reduction)
                        logger.info(f"[JOB {self.job_id}] Applied gain reduction: -{gain_reduction:.2f}dB")
            except Exception as e:
                logger.warning(f"[JOB {self.job_id}] Audio normalization skipped: {e}")
            
            # Save final audio
            output_dir = os.path.join(tempfile.gettempdir(), "v2_dubbing", f"job_{self.job_id}")
            os.makedirs(output_dir, exist_ok=True)
            
            final_audio_path = os.path.join(output_dir, "final_audio.mp3")
            assembled_audio.export(final_audio_path, format="mp3", bitrate="320k")
            
            logger.info(f"[JOB {self.job_id}] Audio assembly complete: {final_audio_path}")
            logger.info(f"[JOB {self.job_id}] Final duration: {len(assembled_audio)/1000:.2f}s")
            
            return final_audio_path
            
        except Exception as e:
            logger.error(f"[JOB {self.job_id}] Audio assembly failed: {e}")
            raise

