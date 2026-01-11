"""
Video processing service for V2
Handles audio extraction, separation, and video assembly
"""

import os
import logging
import tempfile
from typing import Dict, Any, Optional
from moviepy import VideoFileClip
from pydub import AudioSegment
import soundfile as sf
import numpy as np

try:
    import torch
    import torchaudio
    from demucs import pretrained
    from demucs.apply import apply_model
    DEMUCS_AVAILABLE = True
except ImportError:
    DEMUCS_AVAILABLE = False
    logger.warning("Demucs not available - audio separation will not work")

logger = logging.getLogger(__name__)


class VideoProcessor:
    """Video and audio processing service"""
    
    def __init__(self, job_id: str):
        self.job_id = job_id
        self._demucs_model = None
    
    async def extract_audio(self, video_path: str) -> str:
        """Extract audio from video file"""
        try:
            logger.info(f"[JOB {self.job_id}] Extracting audio from video")
            
            output_dir = os.path.join(tempfile.gettempdir(), "v2_dubbing", f"job_{self.job_id}")
            os.makedirs(output_dir, exist_ok=True)
            
            video = VideoFileClip(video_path)
            audio = video.audio
            
            if audio is None:
                raise Exception("No audio track found in video file")
            
            audio_path = os.path.join(output_dir, "original_audio.wav")
            audio.write_audiofile(
                audio_path,
                fps=22050,
                nbytes=2,
                logger=None
            )
            
            # Ensure stereo for Demucs
            test_audio = AudioSegment.from_file(audio_path)
            if test_audio.channels == 1:
                logger.info(f"[JOB {self.job_id}] Converting mono to stereo")
                stereo_audio = test_audio.set_channels(2)
                stereo_audio.export(audio_path, format="wav")
            
            audio.close()
            video.close()
            
            logger.info(f"[JOB {self.job_id}] Audio extracted: {audio_path}")
            return audio_path
            
        except Exception as e:
            logger.error(f"[JOB {self.job_id}] Audio extraction failed: {e}")
            raise
    
    async def separate_audio(self, audio_path: str) -> Dict[str, str]:
        """Separate audio into stems using Demucs"""
        if not DEMUCS_AVAILABLE:
            raise Exception("Demucs not available - cannot separate audio")
        
        try:
            logger.info(f"[JOB {self.job_id}] Separating audio with Demucs")
            
            # Load model
            if self._demucs_model is None:
                logger.info(f"[JOB {self.job_id}] Loading Demucs model...")
                self._demucs_model = pretrained.get_model('htdemucs')
                self._demucs_model.eval()
            
            # Load audio
            wav, sr = torchaudio.load(audio_path)
            logger.info(f"[JOB {self.job_id}] Audio loaded: {wav.shape}, sample rate: {sr}")
            
            # Resample if needed
            if sr != self._demucs_model.samplerate:
                wav = torchaudio.functional.resample(wav, sr, self._demucs_model.samplerate)
                sr = self._demucs_model.samplerate
            
            # Add batch dimension
            if wav.dim() == 2:
                wav = wav.unsqueeze(0)
            elif wav.dim() == 1:
                wav = wav.unsqueeze(0).unsqueeze(0)
            
            # Separate
            with torch.no_grad():
                sources = apply_model(self._demucs_model, wav, device='cpu', progress=True)
            
            # Save separated stems
            source_names = ['drums', 'bass', 'other', 'vocals']
            separated_files = {}
            output_dir = os.path.dirname(audio_path)
            
            for i, name in enumerate(source_names):
                output_path = os.path.join(output_dir, f"{name}.wav")
                source_audio = sources[0, i].cpu().numpy()
                
                # Ensure stereo
                if len(source_audio.shape) == 1:
                    source_audio = np.stack([source_audio, source_audio])
                
                sf.write(output_path, source_audio.T, sr)
                separated_files[name] = output_path
                logger.info(f"[JOB {self.job_id}] Saved {name} stem: {output_path}")
            
            return separated_files
            
        except Exception as e:
            logger.error(f"[JOB {self.job_id}] Audio separation failed: {e}")
            raise
    
    async def create_background(self, separated_files: Dict[str, str]) -> str:
        """Combine background stems into single track"""
        try:
            logger.info(f"[JOB {self.job_id}] Creating background track")
            
            output_dir = os.path.dirname(separated_files['drums'])
            background_path = os.path.join(output_dir, "background.wav")
            
            drums, sr = sf.read(separated_files['drums'])
            bass, _ = sf.read(separated_files['bass'])
            other, _ = sf.read(separated_files['other'])
            
            background = drums + bass + other
            sf.write(background_path, background, sr)
            
            logger.info(f"[JOB {self.job_id}] Background track created: {background_path}")
            return background_path
            
        except Exception as e:
            logger.error(f"[JOB {self.job_id}] Background creation failed: {e}")
            raise
    
    async def replace_audio(self, video_path: str, audio_path: str) -> str:
        """Replace video audio with new audio track"""
        try:
            logger.info(f"[JOB {self.job_id}] Replacing video audio")
            
            output_dir = os.path.join(tempfile.gettempdir(), "v2_dubbing", f"job_{self.job_id}")
            os.makedirs(output_dir, exist_ok=True)
            
            output_path = os.path.join(output_dir, "dubbed_video.mp4")
            
            # Use moviepy to replace audio
            from moviepy import AudioFileClip
            video = VideoFileClip(video_path)
            audio = AudioFileClip(audio_path)

            
            # Match durations
            if audio.duration < video.duration:
                audio = audio.set_duration(video.duration)
            elif audio.duration > video.duration:
                # audio = audio.subclip(0, video.duration)
                audio = audio.subclipped(0, video.duration)
            
            # final_video = video.set_audio(audio)
            final_video = video.with_audio(audio)
            final_video.write_videofile(
                output_path,
                codec='libx264',
                audio_codec='aac',
                logger=None
            )
            
            video.close()
            audio.close()
            final_video.close()
            
            logger.info(f"[JOB {self.job_id}] Video audio replaced: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"[JOB {self.job_id}] Audio replacement failed: {e}")
            raise

