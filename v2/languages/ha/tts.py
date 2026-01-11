"""
Hausa TTS processor using Hugging Face models (Coqui XTTS-v2 or MMS TTS)
"""

import logging
from typing import List, Dict, Any
from pydub import AudioSegment
import sys
import os

# Add parent directories to path
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from v2.tools.huggingface_tts import generate_tts_huggingface

logger = logging.getLogger(__name__)


class TTSProcessor:
    """Hausa TTS processor using Hugging Face models"""
    
    def __init__(self, job_id: str):
        self.job_id = job_id
        logger.info(f"[JOB {self.job_id}] Initialized Hausa TTS processor (Hugging Face)")
    
    async def generate_tts(
        self,
        segments: List[Dict[str, Any]],
        target_language: str
    ) -> List[Dict[str, Any]]:
        """
        Generate TTS audio for Hausa segments
        
        Args:
            segments: List of segments with translated_text
            target_language: Target language code (should be 'ha')
            
        Returns:
            List of segments with audio added
        """
        try:
            logger.info(f"[JOB {self.job_id}] Generating Hausa TTS for {len(segments)} segments")
            
            tts_segments = []
            for i, seg in enumerate(segments):
                text = seg.get("translated_text", "")
                if not text:
                    seg["audio"] = AudioSegment.silent(duration=int(seg.get("duration", 0) * 1000))
                    tts_segments.append(seg)
                    continue
                
                try:
                    # Use Hugging Face TTS for Hausa
                    audio = generate_tts_huggingface(text, 'ha', prefer_coqui=True)
                    seg["audio"] = audio
                    
                    if (i + 1) % 10 == 0:
                        logger.info(f"[JOB {self.job_id}] Generated TTS for {i + 1}/{len(segments)} segments")
                        
                except Exception as e:
                    logger.error(f"[JOB {self.job_id}] TTS generation failed for segment {i+1}: {e}")
                    # Fallback to silence
                    seg["audio"] = AudioSegment.silent(duration=int(seg.get("duration", 0) * 1000))
                
                tts_segments.append(seg)
            
            logger.info(f"[JOB {self.job_id}] Hausa TTS generation complete")
            return tts_segments
            
        except Exception as e:
            logger.error(f"[JOB {self.job_id}] Hausa TTS generation failed: {e}")
            raise

