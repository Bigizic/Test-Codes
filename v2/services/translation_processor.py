"""
Translation processor for V2
Handles text translation with language-specific models
"""

import os
import logging
from typing import List, Dict, Any

try:
    from google.cloud import translate_v2
    GOOGLE_TRANSLATE_AVAILABLE = True
except ImportError:
    GOOGLE_TRANSLATE_AVAILABLE = False

try:
    # Try to import Hugging Face NLLB translator
    import sys
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    from v2.tools.huggingface_translation import NLLBTranslator
    HUGGINGFACE_TRANSLATE_AVAILABLE = True
except ImportError:
    HUGGINGFACE_TRANSLATE_AVAILABLE = False

logger = logging.getLogger(__name__)

if not HUGGINGFACE_TRANSLATE_AVAILABLE:
    logger.warning("Hugging Face translation tools not available")


class TranslationProcessor:
    """Text translation service using Hugging Face NLLB models and Google Translate"""

    def __init__(self, job_id: str):
        self.job_id = job_id
        self._google_client = None
        self._init_clients()
    
    def _init_clients(self):
        """Initialize translation clients"""
        # Google Translate (fallback)
        if GOOGLE_TRANSLATE_AVAILABLE:
            try:
                self._google_client = translate_v2.Client()
                logger.info(f"[JOB {self.job_id}] Google Translate client initialized")
            except Exception as e:
                logger.warning(f"[JOB {self.job_id}] Google Translate init failed: {e}")
    
    async def translate(
        self,
        segments: List[Dict[str, Any]],
        source_language: str,
        target_language: str
    ) -> List[Dict[str, Any]]:
        """
        Translate segments using Hugging Face NLLB models
        
        Args:
            segments: List of segments with transcription
            source_language: Source language code
            target_language: Target language code
            
        Returns:
            List of segments with translated_text added
        """
        try:
            logger.info(f"[JOB {self.job_id}] Translating {len(segments)} segments")
            logger.info(f"[JOB {self.job_id}] {source_language} → {target_language}")
            
            # Check for language-specific translation (Hugging Face models for Nigerian languages)
            lang_processor = self._get_language_processor(target_language)
            if lang_processor:
                logger.info(f"[JOB {self.job_id}] Using language-specific translator for {target_language}")
                return await lang_processor.translate(segments, source_language, target_language)
            
            # Use Hugging Face NLLB-200 as primary, fallback to Google
            translated_segments = []
            for seg in segments:
                text = seg.get("transcription", "")
                if not text:
                    seg["translated_text"] = ""
                    translated_segments.append(seg)
                    continue
                
                # Choose translation service
                if target_language in ['yo', 'ig', 'ha'] and HUGGINGFACE_TRANSLATE_AVAILABLE:
                    try:
                        translated_text = NLLBTranslator.translate(
                            text, source_language, target_language
                        )
                    except Exception as e:
                        logger.warning(f"[JOB {self.job_id}] Hugging Face translation failed: {e}, falling back to Google")
                        if self._google_client:
                            translated_text = self._translate_with_google(text, source_language, target_language)
                        else:
                            translated_text = text
                elif self._google_client:
                    translated_text = self._translate_with_google(
                        text, source_language, target_language
                    )
                else:
                    logger.warning(f"[JOB {self.job_id}] No translation service available, using original")
                    translated_text = text
                
                seg["translated_text"] = translated_text
                translated_segments.append(seg)
            
            logger.info(f"[JOB {self.job_id}] Translation complete")
            return translated_segments
            
        except Exception as e:
            logger.error(f"[JOB {self.job_id}] Translation failed: {e}")
            raise
    
    def _translate_with_google(self, text: str, source: str, target: str) -> str:
        """Translate using Google Translate"""
        try:
            result = self._google_client.translate(
                text,
                source_language=source,
                target_language=target,
                format_="text"
            )
            return result['translatedText'].strip()
        except Exception as e:
            logger.error(f"Google translation failed: {e}")
            return text
    
    def _get_language_processor(self, language: str):
        """Get language-specific translation processor if available"""
        try:
            lang_code = language.lower()
            module_path = f"v2.languages.{lang_code}.translation"
            processor_module = __import__(module_path, fromlist=["TranslationProcessor"])
            if hasattr(processor_module, "TranslationProcessor"):
                return processor_module.TranslationProcessor(self.job_id)
        except ImportError:
            pass
        except Exception as e:
            logger.warning(f"Failed to load language translator for {language}: {e}")
        
        return None

