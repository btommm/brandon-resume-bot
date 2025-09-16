"""
Brandon Resume Bot - Main Application
Hugging Face Spaces entry point
"""

import gradio as gr
import os
import signal
import sys
from src.brandon_bot.chat_interface_simple import create_interface

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\n👋 Shutting down gracefully...")
    sys.exit(0)

def main():
    """Main function to launch the resume bot"""
    
    print("🚀 Starting Brandon-Bot...")
    
    # Create the Gradio interface
    demo = create_interface()
    
    # Detect if running on Hugging Face or locally
    is_huggingface = os.getenv("SPACE_ID") is not None
    
    if is_huggingface:
        # Hugging Face Spaces settings
        demo.launch(
            server_name="0.0.0.0",   # Required for HF
            server_port=7860,        # HF default port
            share=False,
            show_error=True,
            show_api=False,
            prevent_thread_lock=False
        )
    else:
        # Local development settings
        signal.signal(signal.SIGINT, signal_handler)
        try:
            demo.launch(
                server_name="127.0.0.1",
                server_port=7862,
                share=False,
                show_error=True,
                show_api=False,
                prevent_thread_lock=False
            )
        except KeyboardInterrupt:
            print("\n👋 Received interrupt signal...")
        finally:
            print("🔚 Cleaning up...")
            try:
                demo.close()
            except:
                pass

if __name__ == "__main__":
    main()