"""
brandon-bot: AI chat interface for interviews using OpenAI and Gradio
"""

__version__ = "0.1.0"

from .bot import resume_bot
from .document_processor import document_processor
from .chat_interface_simple import create_interface
from .config import config
# All analytics handled by OpenAI natively

__all__ = ["resume_bot", "document_processor", "create_interface", "config"]
