"""
Language-specific TTS models for Nigerian languages
Uses best available models for Hausa, Igbo, and Yoruba
"""

import os
import logging
import torch
import numpy as np
import tempfile
from typing import Optional
from pydub import AudioSegment

try:
    from transformers import AutoProcessor, AutoModel, AutoTokenizer, AutoModelForCausalLM
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

try:
    from TTS.api import TTS as CoquiTTS
    COQUI_TTS_AVAILABLE = True
except ImportError:
    COQUI_TTS_AVAILABLE = False

logger = logging.getLogger(__name__)

# Best models for each Nigerian language from Hugging Face
# Hausa: TWB Voice Hausa (specific TTS model)
HAUSA_TTS_MODEL = "CLEAR-Global/TWB-Voice-Hausa-TTS-1.0"

# For Igbo and Yoruba, we'll use Coqui XTTS-v2 (multilingual)
# MMS TTS models may not be available, so XTTS-v2 is the best fallback
# Note: XTTS-v2 supports many languages but may need speaker reference for best quality


class LanguageSpecificTTS:
    """Language-specific TTS using best available models for each language"""
    
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
            logger.info("Using CUDA device for language-specific TTS")
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            cls._device = torch.device("mps")
            logger.info("Using MPS device for language-specific TTS")
        else:
            cls._device = torch.device("cpu")
            logger.info("Using CPU device for language-specific TTS")
        
        return cls._device
    
    @classmethod
    def _load_model_for_language(cls, language: str):
        """Load language-specific TTS model"""
        if language in cls._models:
            return cls._models[language], cls._processors.get(language)
        
        if not TRANSFORMERS_AVAILABLE:
            raise ImportError("transformers library not available")
        
        try:
            model_map = {
                'ha': HAUSA_TTS_MODEL,
                'ig': IGBO_TTS_MODEL,
                'yo': YORUBA_TTS_MODEL,
            }
            
            model_name = model_map.get(language.lower())
            if not model_name:
                raise ValueError(f"No specific model available for language: {language}")
            
            logger.info(f"Loading language-specific TTS model: {model_name} for {language}")
            device = cls._get_device()
            
            # Try different model loading approaches
            try:
                # Try as TTS model with processor
                processor = AutoProcessor.from_pretrained(model_name)
                model = AutoModel.from_pretrained(model_name).to(device)
                model.eval()
                cls._processors[language] = processor
            except:
                # If that fails, might be a different model type
                # For Hausa TTS model, might need different loading
                try:
                    tokenizer = AutoTokenizer.from_pretrained(model_name)
                    model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
                    model.eval()
                    cls._processors[language] = tokenizer
                except Exception as e:
                    logger.warning(f"Standard loading failed for {model_name}: {e}")
                    raise
            
            cls._models[language] = model
            logger.info(f"Language-specific TTS model loaded for {language}")
            return model, cls._processors.get(language)
            
        except Exception as e:
            logger.error(f"Failed to load language-specific TTS model for {language}: {e}")
            raise
    
    @classmethod
    def synthesize_hausa(cls, text: str) -> AudioSegment:
        """Generate Hausa TTS using CLEAR-Global/TWB-Voice-Hausa-TTS-1.0"""
        try:
            if not text or not text.strip():
                raise ValueError("Empty text provided")
            
            logger.info(f"Generating Hausa TTS: '{text[:50]}...'")
            model, processor = cls._load_model_for_language('ha')
            device = cls._get_device()
            
            # Process text - model-specific implementation
            if isinstance(processor, AutoProcessor):
                # Standard TTS processor
                inputs = processor(text=text, return_tensors="pt")
                inputs = {k: v.to(device) for k, v in inputs.items()}
                
                with torch.no_grad():
                    outputs = model(**inputs)
                
                # Extract audio - structure depends on model
                if hasattr(outputs, 'audio_values'):
                    audio_array = outputs.audio_values[0].cpu().numpy()
                elif hasattr(outputs, 'waveform'):
                    audio_array = outputs.waveform[0].cpu().numpy()
                elif hasattr(outputs, 'audio'):
                    audio_array = outputs.audio[0].cpu().numpy()
                else:
                    # Try to get first tensor
                    audio_array = outputs[0][0].cpu().numpy() if len(outputs) > 0 else None
                    if audio_array is None:
                        raise ValueError("Could not extract audio from model output")
                
            else:
                # Tokenizer-based model (might need vocoder)
                tokenizer = processor
                inputs = tokenizer(text, return_tensors="pt")
                inputs = {k: v.to(device) for k, v in inputs.items()}
                
                with torch.no_grad():
                    outputs = model.generate(**inputs, max_length=512)
                
                # For causal models, we need a vocoder to convert to audio
                # This is a simplified approach - may need vocoder integration
                raise NotImplementedError("Vocoder-based TTS not yet implemented. Use Coqui XTTS instead.")
            
            # Convert to AudioSegment (assume 16kHz, mono)
            sample_rate = 16000
            if len(audio_array.shape) > 1:
                audio_array = audio_array.flatten()
            
            # Normalize to [-1, 1] range if needed
            if audio_array.max() > 1.0 or audio_array.min() < -1.0:
                audio_array = audio_array / np.abs(audio_array).max()
            
            # Convert to int16
            audio_int16 = (audio_array * 32767).astype(np.int16)
            
            audio = AudioSegment(
                audio_int16.tobytes(),
                frame_rate=sample_rate,
                sample_width=2,
                channels=1
            )
            
            logger.info(f"Generated {len(audio)/1000:.2f}s of Hausa audio")
            return audio
            
        except Exception as e:
            logger.error(f"Hausa TTS synthesis failed: {e}")
            raise
    
    @classmethod
    def synthesize(cls, text: str, language: str) -> AudioSegment:
        """
        Synthesize speech using language-specific model
        
        Args:
            text: Text to convert to speech
            language: Language code ('ha', 'ig', 'yo')
            
        Returns:
            AudioSegment with synthesized speech
        """
        lang = language.lower()
        
        if lang == 'ha':
            return cls.synthesize_hausa(text)
        elif lang in ['ig', 'yo']:
            # For Igbo and Yoruba, try MMS TTS, fallback handled by caller
            raise NotImplementedError(f"Direct synthesis for {lang} not yet implemented. Use Coqui XTTS fallback.")
        else:
            raise ValueError(f"Unsupported language for language-specific TTS: {language}")


# Note: generate_tts_huggingface is defined in huggingface_tts.py
# This module provides language-specific implementations

