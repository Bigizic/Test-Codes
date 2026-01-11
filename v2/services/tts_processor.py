"""
TTS processor for V2
Handles text-to-speech generation with language-specific voices
"""

import os
import logging
import io
from typing import List, Dict, Any
import dotenv

dotenv.load_dotenv()

try:
    from elevenlabs import ElevenLabs
    ELEVENLABS_AVAILABLE = True
except ImportError:
    ELEVENLABS_AVAILABLE = False

from pydub import AudioSegment

logger = logging.getLogger(__name__)

try:
    # Try to import Hugging Face TTS as fallback
    import sys
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    from v2.tools.huggingface_tts import generate_tts_huggingface
    HUGGINGFACE_TTS_AVAILABLE = True
except ImportError:
    HUGGINGFACE_TTS_AVAILABLE = False
    logger.warning("Hugging Face TTS tools not available")


class TTSProcessor:
    """Text-to-speech service using Hugging Face models and ElevenLabs"""
    
    def __init__(self, job_id: str):
        self.job_id = job_id
        self._elevenlabs_client = None
        self._init_clients()
    
    def _init_clients(self):
        """Initialize TTS clients"""
        # ElevenLabs
        if ELEVENLABS_AVAILABLE:
            try:
                api_key = os.getenv("ELEVENLABS_API_KEY")
                if api_key:
                    self._elevenlabs_client = ElevenLabs(api_key=api_key)
                    logger.info(f"[JOB {self.job_id}] ElevenLabs client initialized")
            except Exception as e:
                logger.warning(f"[JOB {self.job_id}] ElevenLabs init failed: {e}")
    
    async def generate_tts(
        self,
        segments: List[Dict[str, Any]],
        target_language: str
    ) -> List[Dict[str, Any]]:
        """
        Generate TTS audio for segments
        
        Args:
            segments: List of segments with translated_text
            target_language: Target language code
            
        Returns:
            List of segments with audio added
        """
        try:
            logger.info(f"[JOB {self.job_id}] Generating TTS for {len(segments)} segments")
            
            # Check for language-specific TTS (Hugging Face models for Nigerian languages)
            lang_processor = self._get_language_processor(target_language)
            if lang_processor:
                logger.info(f"[JOB {self.job_id}] Using language-specific TTS for {target_language}")
                return await lang_processor.generate_tts(segments, target_language)
            
            # Use appropriate service as fallback
            tts_segments = []
            for i, seg in enumerate(segments):
                text = seg.get("translated_text", "")
                if not text:
                    seg["audio"] = AudioSegment.silent(duration=int(seg.get("duration", 0) * 1000))
                    tts_segments.append(seg)
                    continue
                
                # Choose TTS service
                # Nigerian languages: Use Hugging Face models if available
                if target_language in ['yo', 'ig', 'ha'] and HUGGINGFACE_TTS_AVAILABLE:
                    try:
                        audio = generate_tts_huggingface(text, target_language, prefer_coqui=True)
                    except Exception as e:
                        logger.warning(f"[JOB {self.job_id}] Hugging Face TTS failed: {e}, falling back to ElevenLabs")
                        if self._elevenlabs_client:
                            audio = self._generate_with_elevenlabs(text)
                        else:
                            audio = AudioSegment.silent(duration=int(seg.get("duration", 0) * 1000))
                elif self._elevenlabs_client:
                    audio = self._generate_with_elevenlabs(text)
                else:
                    logger.warning(f"[JOB {self.job_id}] No TTS service available, using silence")
                    audio = AudioSegment.silent(duration=int(seg.get("duration", 0) * 1000))
                
                seg["audio"] = audio
                tts_segments.append(seg)
                
                if (i + 1) % 10 == 0:
                    logger.info(f"[JOB {self.job_id}] Generated TTS for {i + 1}/{len(segments)} segments")
            
            logger.info(f"[JOB {self.job_id}] TTS generation complete")
            return tts_segments
            
        except Exception as e:
            logger.error(f"[JOB {self.job_id}] TTS generation failed: {e}")
            raise
    
    def _generate_with_elevenlabs(self, text: str) -> AudioSegment:
        """Generate TTS using ElevenLabs"""
        try:
            # Use default voice
            voice_id = "pNInz6obpgDQGcFmaJgB"  # Adam - multilingual
            
            audio_response = self._elevenlabs_client.text_to_speech.convert(
                voice_id=voice_id,
                text=text,
                model_id="eleven_multilingual_v2",
                voice_settings={
                    "stability": 0.5,
                    "similarity_boost": 0.8,
                    "style": 0.0,
                    "use_speaker_boost": True
                },
                output_format="mp3_22050_32"
            )
            
            audio_data = b""
            for chunk in audio_response:
                audio_data += chunk
            
            return AudioSegment.from_mp3(io.BytesIO(audio_data))
            
        except Exception as e:
            logger.error(f"ElevenLabs TTS failed: {e}")
            raise
    
    def _get_language_processor(self, language: str):
        """Get language-specific TTS processor if available"""
        try:
            lang_code = language.lower()
            module_path = f"v2.languages.{lang_code}.tts"
            processor_module = __import__(module_path, fromlist=["TTSProcessor"])
            if hasattr(processor_module, "TTSProcessor"):
                return processor_module.TTSProcessor(self.job_id)
        except ImportError:
            pass
        except Exception as e:
            logger.warning(f"Failed to load language TTS for {language}: {e}")
        
        return None

