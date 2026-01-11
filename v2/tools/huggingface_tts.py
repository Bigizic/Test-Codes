"""
Hugging Face TTS tools using Coqui XTTS-v2 or MMS TTS
Best models for multilingual TTS including Hausa, Igbo, and Yoruba
"""

import os
import logging
import io
import torch
import numpy as np
from typing import Optional
from pydub import AudioSegment

try:
    from transformers import AutoProcessor, AutoModel
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

try:
    import TTS
    from TTS.api import TTS as CoquiTTS
    COQUI_TTS_AVAILABLE = True
except ImportError:
    COQUI_TTS_AVAILABLE = False

logger = logging.getLogger(__name__)

# Language code mapping for TTS models
TTS_LANGUAGE_MAP = {
    'en': 'en',
    'ha': 'ha',  # Hausa
    'ig': 'ig',  # Igbo
    'yo': 'yo',  # Yoruba
    'fr': 'fr',
    'es': 'es',
    'de': 'de',
    'ru': 'ru',
    'zh': 'zh',
    'sw': 'sw',
}

# Primary TTS model - Coqui XTTS-v2 (multilingual, high quality)
COQUI_XTTS_MODEL = "tts_models/multilingual/multi-dataset/xtts_v2"

# Language-specific TTS models from Hugging Face (best quality for each language)
LANGUAGE_SPECIFIC_MODELS = {
    'ha': 'CLEAR-Global/TWB-Voice-Hausa-TTS-1.0',  # Best Hausa TTS model
    'ig': 'facebook/mms-tts-ibo',  # Facebook MMS for Igbo (if available)
    'yo': 'facebook/mms-tts-yor',  # Facebook MMS for Yoruba (if available)
    'en': 'facebook/mms-tts-eng',
}

# Fallback - Facebook MMS TTS models (if language-specific not available)
MMS_TTS_MODELS = {
    'en': 'facebook/mms-tts-eng',
    'ha': 'facebook/mms-tts-hau',  # Fallback for Hausa
    'ig': 'facebook/mms-tts-ibo',  # Fallback for Igbo
    'yo': 'facebook/mms-tts-yor',  # Fallback for Yoruba
}


class CoquiXTTS:
    """Text-to-speech using Coqui XTTS-v2 (multilingual, best quality)"""
    
    _tts_model = None
    _device = None
    
    @classmethod
    def _get_device(cls):
        """Get the best available device"""
        if cls._device:
            return cls._device
        
        if torch.cuda.is_available():
            cls._device = "cuda"
            logger.info("Using CUDA device for Coqui TTS")
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            cls._device = "mps"
            logger.info("Using MPS device for Coqui TTS")
        else:
            cls._device = "cpu"
            logger.info("Using CPU device for Coqui TTS")
        
        return cls._device
    
    @classmethod
    def _load_model(cls):
        """Load Coqui XTTS-v2 model"""
        if cls._tts_model is not None:
            return cls._tts_model
        
        if not COQUI_TTS_AVAILABLE:
            raise ImportError("Coqui TTS not available. Install with: pip install TTS")
        
        try:
            logger.info(f"Loading Coqui XTTS-v2 model")
            device = cls._get_device()
            
            cls._tts_model = CoquiTTS(model_name=COQUI_XTTS_MODEL, progress_bar=False)
            cls._tts_model.to(device)
            
            logger.info("Coqui XTTS-v2 model loaded successfully")
            return cls._tts_model
            
        except Exception as e:
            logger.error(f"Failed to load Coqui XTTS-v2 model: {e}")
            raise
    
    @classmethod
    def synthesize(
        cls,
        text: str,
        language: str,
        speaker_wav: Optional[str] = None
    ) -> AudioSegment:
        """
        Synthesize speech using Coqui XTTS-v2
        
        Args:
            text: Text to convert to speech
            language: Language code (e.g., 'en', 'ha', 'ig', 'yo')
            speaker_wav: Optional path to speaker reference audio for voice cloning
            
        Returns:
            AudioSegment with synthesized speech
        """
        try:
            if not text or not text.strip():
                raise ValueError("Empty text provided")
            
            tts_model = cls._load_model()
            device = cls._get_device()
            
            # Normalize language code
            lang_code = TTS_LANGUAGE_MAP.get(language.lower(), 'en')
            
            # Generate speech
            logger.info(f"Generating speech with Coqui XTTS-v2: lang={lang_code}, text='{text[:50]}...'")
            
            # Use TTS API to generate audio
            output_path = os.path.join(
                os.path.expanduser("~"),
                ".cache",
                "tts",
                f"temp_output_{hash(text) % 10000}.wav"
            )
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # Generate with language specification
            # XTTS-v2 API: tts_to_file(text, file_path, language=lang, speaker_wav=wav_path)
            # Note: XTTS-v2 might not support all languages directly, will use closest match
            try:
                if speaker_wav and os.path.exists(speaker_wav):
                    # Voice cloning mode
                    tts_model.tts_to_file(
                        text=text,
                        file_path=output_path,
                        language=lang_code,
                        speaker_wav=speaker_wav
                    )
                else:
                    # Default voice mode
                    # Try with language, if not supported will use default
                    try:
                        tts_model.tts_to_file(
                            text=text,
                            file_path=output_path,
                            language=lang_code
                        )
                    except:
                        # If language not supported, use without language parameter
                        logger.warning(f"Language {lang_code} not supported by XTTS-v2, using default")
                        tts_model.tts_to_file(
                            text=text,
                            file_path=output_path
                        )
            except Exception as api_error:
                logger.error(f"Coqui TTS API error: {api_error}")
                raise
            
            # Load generated audio
            audio = AudioSegment.from_wav(output_path)
            
            # Cleanup temp file
            try:
                os.remove(output_path)
            except:
                pass
            
            logger.info(f"Generated {len(audio)/1000:.2f}s of audio")
            return audio
            
        except Exception as e:
            logger.error(f"Coqui TTS synthesis failed: {e}")
            raise


class MMS_TTS:
    """Text-to-speech using Facebook MMS TTS (fallback option)"""
    
    _models = {}
    _processors = {}
    _device = None
    
    @classmethod
    def _get_device(cls):
        """Get the best available device"""
        if cls._device:
            return cls._device
        
        if torch.cuda.is_available():
            cls._device = torch.device("cuda")
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            cls._device = torch.device("mps")
        else:
            cls._device = torch.device("cpu")
        
        return cls._device
    
    @classmethod
    def _load_model_for_language(cls, language: str):
        """Load MMS TTS model for specific language"""
        if language in cls._models:
            return cls._models[language], cls._processors[language]
        
        if not TRANSFORMERS_AVAILABLE:
            raise ImportError("transformers library not available")
        
        try:
            model_name = MMS_TTS_MODELS.get(language)
            if not model_name:
                raise ValueError(f"No MMS TTS model available for language: {language}")
            
            logger.info(f"Loading MMS TTS model: {model_name}")
            device = cls._get_device()
            
            processor = AutoProcessor.from_pretrained(model_name)
            model = AutoModel.from_pretrained(model_name).to(device)
            model.eval()
            
            cls._models[language] = model
            cls._processors[language] = processor
            
            logger.info(f"MMS TTS model loaded for {language}")
            return model, processor
            
        except Exception as e:
            logger.error(f"Failed to load MMS TTS model for {language}: {e}")
            raise
    
    @classmethod
    def synthesize(cls, text: str, language: str) -> AudioSegment:
        """
        Synthesize speech using MMS TTS
        
        Args:
            text: Text to convert to speech
            language: Language code
            
        Returns:
            AudioSegment with synthesized speech
        """
        try:
            if not text or not text.strip():
                raise ValueError("Empty text provided")
            
            lang_code = TTS_LANGUAGE_MAP.get(language.lower(), 'en')
            model, processor = cls._load_model_for_language(lang_code)
            device = cls._get_device()
            
            # Process text
            inputs = processor(text=text, return_tensors="pt")
            inputs = {k: v.to(device) for k, v in inputs.items()}
            
            # Generate
            with torch.no_grad():
                outputs = model(**inputs)
            
            # Extract audio array
            audio_array = outputs.audio_values[0].cpu().numpy()
            
            # Convert to AudioSegment
            # MMS TTS typically outputs at 16kHz
            sample_rate = 16000
            audio_int16 = (audio_array * 32767).astype(np.int16)
            audio = AudioSegment(
                audio_int16.tobytes(),
                frame_rate=sample_rate,
                sample_width=2,
                channels=1
            )
            
            logger.info(f"Generated {len(audio)/1000:.2f}s of audio with MMS TTS")
            return audio
            
        except Exception as e:
            logger.error(f"MMS TTS synthesis failed: {e}")
            raise


def generate_tts_huggingface(text: str, language: str, prefer_coqui: bool = True) -> AudioSegment:
    """
    Generate TTS using best available Hugging Face model
    
    Strategy for Nigerian languages:
    1. Hausa: Try TWB Voice Hausa model (CLEAR-Global) if available
    2. Igbo/Yoruba: Use Coqui XTTS-v2 (best multilingual option)
    3. Fallback: Try MMS TTS if Coqui not available
    
    Args:
        text: Text to convert to speech
        language: Language code (e.g., 'ha', 'ig', 'yo')
        prefer_coqui: Prefer Coqui XTTS-v2 over MMS TTS
        
    Returns:
        AudioSegment with synthesized speech
    """
    try:
        lang = language.lower()
        
        # For Hausa, try language-specific TWB Voice model first
        if lang == 'ha' and TRANSFORMERS_AVAILABLE:
            try:
                from v2.tools.huggingface_language_tts import LanguageSpecificTTS
                logger.info(f"Attempting Hausa-specific TTS model (TWB Voice)")
                return LanguageSpecificTTS.synthesize_hausa(text)
            except (ImportError, NotImplementedError) as e:
                logger.info(f"Hausa-specific model not available: {e}, using Coqui XTTS")
            except Exception as e:
                logger.warning(f"Hausa-specific model failed: {e}, using Coqui XTTS fallback")
        
        # Use Coqui XTTS-v2 as primary choice for all languages (including Igbo/Yoruba)
        # XTTS-v2 is multilingual and works well even if language not explicitly supported
        if prefer_coqui and COQUI_TTS_AVAILABLE:
            logger.info(f"Using Coqui XTTS-v2 for {language} (multilingual model)")
            # XTTS-v2 will handle the language best it can
            # If language not directly supported, it will use closest match
            return CoquiXTTS.synthesize(text, language)
        
        # Fallback to MMS TTS if Coqui not available
        elif TRANSFORMERS_AVAILABLE:
            logger.info(f"Using MMS TTS for {language} (fallback)")
            try:
                return MMS_TTS.synthesize(text, language)
            except Exception as mms_error:
                logger.error(f"MMS TTS also failed: {mms_error}")
                raise
        else:
            raise ImportError(
                "No TTS models available. Install dependencies:\n"
                "  pip install TTS transformers torch torchaudio"
            )
            
    except Exception as e:
        logger.error(f"Hugging Face TTS generation failed for {language}: {e}")
        raise

