"""
Hugging Face translation tools using NLLB-200 model
Best model for Hausa, Igbo, and Yoruba translation
"""

import os
import logging
from typing import Optional
import torch

try:
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

logger = logging.getLogger(__name__)

# NLLB-200 language code mapping
NLLB_LANGUAGE_MAP = {
    'en': 'eng_Latn',      # English
    'ha': 'hau_Latn',      # Hausa
    'ig': 'ibo_Latn',      # Igbo
    'yo': 'yor_Latn',      # Yoruba
    'fr': 'fra_Latn',      # French
    'es': 'spa_Latn',      # Spanish
    'de': 'deu_Latn',      # German
    'ru': 'rus_Cyrl',      # Russian
    'zh': 'zho_Hans',      # Chinese (Simplified)
    'sw': 'swh_Latn',      # Swahili
}

# Use smaller model for faster inference, can upgrade to 3.3B for better quality
NLLB_MODEL_NAME = "facebook/nllb-200-distilled-600M"


class NLLBTranslator:
    """Translation service using Facebook NLLB-200 model"""
    
    _model = None
    _tokenizer = None
    _device = None
    
    @classmethod
    def _get_device(cls):
        """Get the best available device"""
        if cls._device:
            return cls._device
        
        if torch.cuda.is_available():
            cls._device = torch.device("cuda")
            logger.info("Using CUDA device for NLLB translation")
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            cls._device = torch.device("mps")
            logger.info("Using MPS device for NLLB translation")
        else:
            cls._device = torch.device("cpu")
            logger.info("Using CPU device for NLLB translation")
        
        return cls._device
    
    @classmethod
    def _load_model(cls):
        """Load NLLB-200 model (lazy loading)"""
        if cls._model is not None and cls._tokenizer is not None:
            return cls._model, cls._tokenizer
        
        if not TRANSFORMERS_AVAILABLE:
            raise ImportError("transformers library not available. Install with: pip install transformers")
        
        try:
            logger.info(f"Loading NLLB-200 model: {NLLB_MODEL_NAME}")
            device = cls._get_device()
            
            # Load tokenizer
            cls._tokenizer = AutoTokenizer.from_pretrained(
                NLLB_MODEL_NAME,
                src_lang="eng_Latn"  # Default source
            )
            
            # Load model
            cls._model = AutoModelForSeq2SeqLM.from_pretrained(
                NLLB_MODEL_NAME
            )
            cls._model = cls._model.to(device)
            cls._model.eval()
            
            logger.info("NLLB-200 model loaded successfully")
            return cls._model, cls._tokenizer
            
        except Exception as e:
            logger.error(f"Failed to load NLLB-200 model: {e}")
            raise
    
    @classmethod
    def translate(
        cls,
        text: str,
        source_language: str,
        target_language: str,
        max_length: int = 512
    ) -> str:
        """
        Translate text using NLLB-200 model
        
        Args:
            text: Text to translate
            source_language: Source language code (e.g., 'en', 'ha', 'ig', 'yo')
            target_language: Target language code
            max_length: Maximum sequence length
            
        Returns:
            Translated text
        """
        try:
            if not text or not text.strip():
                return text
            
            # Load model if not loaded
            model, tokenizer = cls._load_model()
            device = cls._get_device()
            
            # Get NLLB language codes
            src_lang_code = NLLB_LANGUAGE_MAP.get(source_language.lower(), 'eng_Latn')
            tgt_lang_code = NLLB_LANGUAGE_MAP.get(target_language.lower(), 'eng_Latn')
            
            # Set source language in tokenizer
            tokenizer.src_lang = src_lang_code
            
            # Tokenize
            inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=max_length)
            inputs = {k: v.to(device) for k, v in inputs.items()}
            
            # Translate
            with torch.no_grad():
                generated_tokens = model.generate(
                    **inputs,
                    forced_bos_token_id=tokenizer.lang_code_to_id[tgt_lang_code],
                    max_length=max_length,
                    num_beams=4,
                    early_stopping=True
                )
            
            # Decode
            translated_text = tokenizer.batch_decode(generated_tokens, skip_special_tokens=True)[0]
            
            logger.debug(f"NLLB translation: '{text[:50]}...' -> '{translated_text[:50]}...'")
            return translated_text.strip()
            
        except Exception as e:
            logger.error(f"NLLB translation failed: {e}")
            raise

