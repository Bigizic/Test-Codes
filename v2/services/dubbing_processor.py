"""
Main dubbing processor for V2
Coordinates all dubbing phases without API dependencies
"""

import os
import logging
import tempfile
import uuid
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class DubbingProcessor:
    """Main processor for video dubbing workflow"""
    
    def __init__(self):
        self.job_id = f"job_{uuid.uuid4().hex[:12]}"
        self.temp_files = []
        
    async def process_video(
        self,
        video_path: str,
        source_language: str,
        target_language: str
    ) -> Dict[str, Any]:
        """
        Process video through complete dubbing pipeline
        
        Args:
            video_path: Path to input video file
            source_language: Source language code
            target_language: Target language code
            
        Returns:
            Dict with success status and output path
        """
        try:
            logger.info(f"[JOB {self.job_id}] Starting dubbing process")
            logger.info(f"[JOB {self.job_id}] Video: {video_path}")
            logger.info(f"[JOB {self.job_id}] Languages: {source_language} → {target_language}")
            
            # Import services
            from v2.services.video_processor import VideoProcessor
            from v2.services.transcription_processor import TranscriptionProcessor
            from v2.services.translation_processor import TranslationProcessor
            from v2.services.tts_processor import TTSProcessor
            from v2.services.audio_assembler import AudioAssembler
            
            # Phase 1: Extract audio from video
            logger.info(f"[JOB {self.job_id}] Phase 1: Extracting audio")
            video_processor = VideoProcessor(self.job_id)
            audio_path = await video_processor.extract_audio(video_path)
            self.temp_files.append(audio_path)
            
            # Phase 2: Separate audio stems
            logger.info(f"[JOB {self.job_id}] Phase 2: Separating audio")
            separated_files = await video_processor.separate_audio(audio_path)
            self.temp_files.extend(separated_files.values())
            
            # Phase 3: Create background track
            logger.info(f"[JOB {self.job_id}] Phase 3: Creating background track")
            background_path = await video_processor.create_background(separated_files)
            self.temp_files.append(background_path)
            
            # Phase 4: Transcribe audio
            logger.info(f"[JOB {self.job_id}] Phase 4: Transcribing audio")
            transcription_processor = TranscriptionProcessor(self.job_id)
            segments = await transcription_processor.transcribe(
                separated_files['vocals'],
                source_language
            )
            
            # Phase 5: Translate segments
            logger.info(f"[JOB {self.job_id}] Phase 5: Translating segments")
            translation_processor = TranslationProcessor(self.job_id)
            translated_segments = await translation_processor.translate(
                segments,
                source_language,
                target_language
            )
            
            # Phase 6: Generate TTS
            logger.info(f"[JOB {self.job_id}] Phase 6: Generating TTS")
            tts_processor = TTSProcessor(self.job_id)
            tts_segments = await tts_processor.generate_tts(
                translated_segments,
                target_language
            )
            
            # Phase 7: Assemble final audio
            logger.info(f"[JOB {self.job_id}] Phase 7: Assembling final audio")
            assembler = AudioAssembler(self.job_id)
            final_audio_path = await assembler.assemble(
                tts_segments,
                background_path
            )
            self.temp_files.append(final_audio_path)
            
            # Phase 8: Replace video audio
            logger.info(f"[JOB {self.job_id}] Phase 8: Replacing video audio")
            output_path = await video_processor.replace_audio(
                video_path,
                final_audio_path
            )
            
            logger.info(f"[JOB {self.job_id}] ✅ Dubbing complete: {output_path}")
            
            return {
                "success": True,
                "output_path": output_path,
                "job_id": self.job_id
            }
            
        except Exception as e:
            logger.error(f"[JOB {self.job_id}] ❌ Dubbing failed: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "job_id": self.job_id
            }
        finally:
            # Cleanup temp files (optional - keep for debugging)
            # self._cleanup_temp_files()
            pass
    
    def _cleanup_temp_files(self):
        """Clean up temporary files"""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                    logger.info(f"Cleaned up: {temp_file}")
            except Exception as e:
                logger.warning(f"Failed to cleanup {temp_file}: {e}")

