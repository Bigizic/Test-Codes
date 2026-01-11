#!/usr/bin/env python3
"""
Console-based GUI application for video dubbing
Provides file selection dialog and language input prompts
"""

import os
import sys
import logging
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Optional, Tuple
from pathlib import Path
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DubbingConsole:
    """Main console application with GUI for video dubbing"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Video Dubbing Service V2")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Variables
        self.video_path = tk.StringVar()
        self.source_language = tk.StringVar(value="English")
        self.target_language = tk.StringVar()
        
        # Supported languages from languages directory
        self.supported_languages = self._get_supported_languages()
        self.language_display_map = {name: code for code, name in self.supported_languages.items()}
        
        self._setup_ui()
        
    def _get_supported_languages(self) -> dict:
        """Get supported languages from languages directory"""
        languages_dir = Path(__file__).parent / "languages"
        supported = {}
        
        if languages_dir.exists():
            for lang_dir in languages_dir.iterdir():
                if lang_dir.is_dir() and (lang_dir / "__init__.py").exists():
                    lang_code = lang_dir.name
                    # Try to get display name from language module
                    try:
                        lang_module = __import__(f"v2.languages.{lang_code}.language", fromlist=["DISPLAY_NAME"])
                        display_name = getattr(lang_module, "DISPLAY_NAME", lang_code.upper())
                        supported[lang_code] = display_name
                    except (ImportError, AttributeError):
                        # Fallback to __init__.py or default
                        try:
                            init_module = __import__(f"v2.languages.{lang_code}", fromlist=["DISPLAY_NAME"])
                            display_name = getattr(init_module, "DISPLAY_NAME", lang_code.upper())
                            supported[lang_code] = display_name
                        except:
                            supported[lang_code] = lang_code.upper()
        
        # Add common languages if no language directories exist yet
        if not supported:
            supported = {
                "en": "English",
                "es": "Spanish",
                "fr": "French",
                "de": "German",
                "ru": "Russian",
                "zh": "Chinese",
                "sw": "Swahili",
                "yo": "Yoruba",
                "ha": "Hausa",
                "ig": "Igbo"
            }
        
        return supported
    
    def _setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Video Dubbing Service V2",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Video selection section
        video_frame = ttk.LabelFrame(main_frame, text="1. Select Video File", padding="15")
        video_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(video_frame, text="Video File:").pack(anchor=tk.W)
        
        file_frame = ttk.Frame(video_frame)
        file_frame.pack(fill=tk.X, pady=5)
        
        self.file_entry = ttk.Entry(file_frame, textvariable=self.video_path, state="readonly", width=50)
        self.file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        ttk.Button(
            file_frame,
            text="Browse...",
            command=self._browse_video
        ).pack(side=tk.LEFT)
        
        # Source language section
        source_frame = ttk.LabelFrame(main_frame, text="2. Source Language", padding="15")
        source_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(source_frame, text="Language spoken in the video:").pack(anchor=tk.W)
        
        self.source_combo = ttk.Combobox(
            source_frame,
            textvariable=self.source_language,
            values=list(self.supported_languages.values()),
            state="readonly",
            width=50
        )
        self.source_combo.pack(fill=tk.X, pady=5)
        
        # Target language section
        target_frame = ttk.LabelFrame(main_frame, text="3. Target Language", padding="15")
        target_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(target_frame, text="Language for dubbing:").pack(anchor=tk.W)
        
        self.target_combo = ttk.Combobox(
            target_frame,
            textvariable=self.target_language,
            values=list(self.supported_languages.values()),
            state="readonly",
            width=50
        )
        self.target_combo.pack(fill=tk.X, pady=5)
        
        # Process button - make it prominent
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        # Create a larger, more prominent button
        self.process_button = tk.Button(
            button_frame,
            text="▶ Start Dubbing",
            command=self._start_dubbing,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12, "bold"),
            relief=tk.RAISED,
            bd=3,
            padx=30,
            pady=12,
            cursor="hand2",
            activebackground="#45a049",
            activeforeground="white"
        )
        self.process_button.pack(side=tk.LEFT, padx=5)
        
        # Hint label
        hint_label = ttk.Label(
            button_frame,
            text="(Press Enter to start)",
            font=("Arial", 9),
            foreground="gray"
        )
        hint_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        ttk.Button(
            button_frame,
            text="Exit",
            command=self.root.quit
        ).pack(side=tk.LEFT, padx=5)
        
        # Bind Enter key to start dubbing (works globally)
        self.root.bind('<Return>', lambda event: self._start_dubbing())
        self.root.bind('<KP_Enter>', lambda event: self._start_dubbing())  # Numeric keypad Enter
        
        # Bind Enter key on comboboxes as well
        self.source_combo.bind('<Return>', lambda event: self._start_dubbing())
        self.target_combo.bind('<Return>', lambda event: self._start_dubbing())
        
        # Also bind to file entry
        self.file_entry.bind('<Return>', lambda event: self._start_dubbing())
        
        # Status/progress area
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.status_text = tk.Text(status_frame, height=8, wrap=tk.WORD, state=tk.DISABLED)
        self.status_text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(status_frame, command=self.status_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.status_text.config(yscrollcommand=scrollbar.set)
    
    def _browse_video(self):
        """Open file dialog to select video file"""
        file_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[
                ("Video files", "*.mp4 *.avi *.mov *.mkv *.webm"),
                ("Audio files", "*.mp3 *.wav *.flac *.ogg *.aac *.m4a"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.video_path.set(file_path)
            self._log_status(f"Selected file: {os.path.basename(file_path)}")
    
    def _log_status(self, message: str):
        """Log message to status text area"""
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)
        self.root.update()
    
    def _get_language_code(self, display_name: str) -> Optional[str]:
        """Convert display name to language code"""
        return self.language_display_map.get(display_name)
    
    def _validate_inputs(self) -> Tuple[bool, str]:
        """Validate user inputs"""
        if not self.video_path.get():
            return False, "Please select a video file"
        
        if not os.path.exists(self.video_path.get()):
            return False, "Selected file does not exist"
        
        if not self.source_language.get():
            return False, "Please select source language"
        
        if not self.target_language.get():
            return False, "Please select target language"
        
        source_code = self._get_language_code(self.source_language.get())
        target_code = self._get_language_code(self.target_language.get())
        
        if not source_code:
            return False, "Invalid source language"
        
        if not target_code:
            return False, "Invalid target language"
        
        if source_code == target_code:
            return False, "Source and target languages must be different"
        
        return True, ""
    
    def _start_dubbing(self):
        """Start the dubbing process"""
        # Validate inputs
        is_valid, error_msg = self._validate_inputs()
        if not is_valid:
            messagebox.showerror("Validation Error", error_msg)
            return
        
        # Get language codes
        source_code = self._get_language_code(self.source_language.get())
        target_code = self._get_language_code(self.target_language.get())
        
        video_file = self.video_path.get()
        
        # Disable process button
        self.process_button.config(state=tk.DISABLED)
        
        # Log start
        self._log_status("=" * 60)
        self._log_status("Starting dubbing process...")
        self._log_status(f"Video: {os.path.basename(video_file)}")
        self._log_status(f"Source Language: {self.source_language.get()} ({source_code})")
        self._log_status(f"Target Language: {self.target_language.get()} ({target_code})")
        self._log_status("=" * 60)
        
        # Run dubbing process in async context
        try:
            # Import dubbing processor
            from v2.services.dubbing_processor import DubbingProcessor
            
            processor = DubbingProcessor()
            
            # Run async dubbing process
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            try:
                result = loop.run_until_complete(
                    processor.process_video(
                        video_path=video_file,
                        source_language=source_code,
                        target_language=target_code
                    )
                )
                
                if result.get("success"):
                    self._log_status("\n✅ Dubbing completed successfully!")
                    self._log_status(f"Output file: {result.get('output_path', 'N/A')}")
                    messagebox.showinfo(
                        "Success",
                        f"Dubbing completed!\n\nOutput: {os.path.basename(result.get('output_path', ''))}"
                    )
                else:
                    error = result.get("error", "Unknown error")
                    self._log_status(f"\n❌ Dubbing failed: {error}")
                    messagebox.showerror("Error", f"Dubbing failed:\n{error}")
                    
            finally:
                loop.close()
                
        except Exception as e:
            logger.error(f"Dubbing process error: {e}", exc_info=True)
            self._log_status(f"\n❌ Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
        
        finally:
            # Re-enable process button
            self.process_button.config(state=tk.NORMAL)
    
    def run(self):
        """Run the console application"""
        self.root.mainloop()


def main():
    """Main entry point for console application"""
    try:
        app = DubbingConsole()
        app.run()
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        messagebox.showerror("Fatal Error", f"Application failed to start:\n{str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

