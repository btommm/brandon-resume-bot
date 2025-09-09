"""
Brandon Resume Bot - Main Application
Hugging Face Spaces entry point
"""

import gradio as gr
import os
from src.brandon_bot.chat_interface import create_interface

def main():
    """Main function to launch the resume bot"""
    # Create the Gradio interface
    demo = create_interface()
    
    # Launch with appropriate settings for HF Spaces
    demo.launch(
        server_name="0.0.0.0",  # Required for HF Spaces
        server_port=7860,       # HF Spaces default port
        share=False,            # Not needed on HF Spaces
        show_error=True,        # Show errors for debugging
        favicon_path="static/favicon.ico" if os.path.exists("static/favicon.ico") else None
    )

if __name__ == "__main__":
    main()

