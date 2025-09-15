"""
Deployment version of Brandon-Bot for Hugging Face Spaces
This version includes proper environment setup and error handling for cloud deployment
"""

import gradio as gr
import os
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

# Import after path setup
from brandon_bot.chat_interface_simple import create_interface

def main():
    """Main function for Hugging Face Spaces deployment"""
    
    # Check for required environment variable
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERROR: OPENAI_API_KEY environment variable not set!")
        print("Please set your OpenAI API key in the Hugging Face Spaces secrets.")
        return
    
    print("🚀 Starting Brandon-Bot for Hugging Face Spaces...")
    
    # Create the interface
    demo = create_interface()
    
    # Launch for Hugging Face Spaces
    demo.launch(
        server_name="0.0.0.0",  # Required for Hugging Face
        server_port=7860,       # Default HF port
        share=False,            # Not needed on HF
        show_error=True,        # Show errors for debugging
        show_api=False,         # Disable API docs
        prevent_thread_lock=False
    )

if __name__ == "__main__":
    main()
