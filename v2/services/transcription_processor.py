"""
Transcription processor for V2
Handles audio transcription with language-specific models
"""

import os
import logging
import tempfile
import uuid
from typing import List, Dict, Any
from pydub import AudioSegment

try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False

logger = logging.getLogger(__name__)


class TranscriptionProcessor:
    """Audio transcription service"""
    
    def __init__(self, job_id: str):
        self.job_id = job_id
        self._whisper_model = None
    
    async def transcribe(self, audio_path: str, language: str) -> List[Dict[str, Any]]:
        """
        Transcribe audio file
        
        Args:
            audio_path: Path to audio file
            language: Source language code
            
        Returns:
            List of segments with transcription
        """
        try:
            logger.info(f"[JOB {self.job_id}] Transcribing audio: {audio_path}")
            
            # Check for language-specific transcription
            lang_processor = self._get_language_processor(language)
            if lang_processor:
                logger.info(f"[JOB {self.job_id}] Using language-specific processor for {language}")
                return await lang_processor.transcribe(audio_path, language)
            
            # Use Whisper as default
            if not WHISPER_AVAILABLE:
                raise Exception("Whisper not available for transcription")
            
            # Load Whisper model
            if self._whisper_model is None:
                logger.info(f"[JOB {self.job_id}] Loading Whisper model...")
                self._whisper_model = whisper.load_model("base")
            
            # Transcribe
            result = self._whisper_model.transcribe(
                audio_path,
                language=language if language != "en" else None,
                task="transcribe",
                fp16=False
            )
            
            # Convert to segment format
            segments = []
            for seg in result.get("segments", []):
                segments.append({
                    "start_time": seg.get("start", 0),
                    "end_time": seg.get("end", 0),
                    "duration": seg.get("end", 0) - seg.get("start", 0),
                    "transcription": seg.get("text", "").strip()
                })
            
            logger.info(f"[JOB {self.job_id}] Transcribed {len(segments)} segments")
            return segments
            
        except Exception as e:
            logger.error(f"[JOB {self.job_id}] Transcription failed: {e}")
            raise

    def _get_language_processor(self, language: str):
        """Get language-specific processor if available"""
        try:
            # Try to import language-specific module
            lang_code = language.lower()
            module_path = f"v2.languages.{lang_code}.transcription"
            processor_module = __import__(module_path, fromlist=["TranscriptionProcessor"])
            if hasattr(processor_module, "TranscriptionProcessor"):
                return processor_module.TranscriptionProcessor(self.job_id)
        except ImportError:
            # Language-specific processor not available
            pass
        except Exception as e:
            logger.warning(f"Failed to load language processor for {language}: {e}")
        
        return None

