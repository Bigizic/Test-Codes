"""
Yoruba translation processor using Hugging Face NLLB-200 model
"""

import logging
from typing import List, Dict, Any
import sys
import os

# Add parent directories to path
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from v2.tools.huggingface_translation import NLLBTranslator

logger = logging.getLogger(__name__)


class TranslationProcessor:
    """Yoruba translation processor using NLLB-200"""
    
    def __init__(self, job_id: str):
        self.job_id = job_id
        logger.info(f"[JOB {self.job_id}] Initialized Yoruba translation processor (NLLB-200)")
    
    async def translate(
        self,
        segments: List[Dict[str, Any]],
        source_language: str,
        target_language: str
    ) -> List[Dict[str, Any]]:
        """
        Translate segments to Yoruba using NLLB-200
        
        Args:
            segments: List of segments with transcription
            source_language: Source language code
            target_language: Target language code (should be 'yo')
            
        Returns:
            List of segments with translated_text added
        """
        try:
            logger.info(f"[JOB {self.job_id}] Translating {len(segments)} segments to Yoruba using NLLB-200")
            
            translated_segments = []
            for i, seg in enumerate(segments):
                text = seg.get("transcription", "")
                if not text:
                    seg["translated_text"] = ""
                    translated_segments.append(seg)
                    continue
                
                try:
                    # Use NLLB-200 for translation
                    translated_text = NLLBTranslator.translate(
                        text=text,
                        source_language=source_language,
                        target_language='yo'  # Yoruba
                    )
                    seg["translated_text"] = translated_text
                    
                    if (i + 1) % 10 == 0:
                        logger.info(f"[JOB {self.job_id}] Translated {i + 1}/{len(segments)} segments")
                        
                except Exception as e:
                    logger.error(f"[JOB {self.job_id}] Translation failed for segment {i+1}: {e}")
                    seg["translated_text"] = text
                
                translated_segments.append(seg)
            
            logger.info(f"[JOB {self.job_id}] Yoruba translation complete")
            return translated_segments
            
        except Exception as e:
            logger.error(f"[JOB {self.job_id}] Yoruba translation failed: {e}")
            raise

