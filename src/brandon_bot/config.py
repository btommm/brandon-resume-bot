"""
Configuration management for Brandon Resume Bot

This module handles all configuration settings for the resume bot including:
- OpenAI API settings and credentials
- Bot behavior parameters
- File paths and directories
- System prompts for the AI model
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file (if it exists)
# This allows us to store sensitive data like API keys securely
load_dotenv()

class Config:
    """
    Configuration class that centralizes all settings for the resume bot
    
    This class reads from environment variables and provides defaults
    for all configurable aspects of the bot behavior and functionality
    """
    
    # === OpenAI API Configuration ===
    # These settings control how we interact with OpenAI's GPT models
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Required: Your OpenAI API key
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")  # Which GPT model to use
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "500"))  # Maximum response length
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.4"))  # Response creativity (0-1)
    
    # === Bot Behavior Configuration ===
    # These settings control how the bot behaves and responds
    
    BOT_NAME = os.getenv("BOT_NAME", "Brandon's Resume Bot")  # Display name for the bot
    MAX_CONVERSATION_LENGTH = int(os.getenv("MAX_CONVERSATION_LENGTH", "10"))  # How many exchanges to remember
    
    # === Analytics Configuration ===
    # OpenAI provides comprehensive analytics natively in their dashboard
    # Analytics are for Brandon only - not shown to employers/users
    
    # === Tracing Configuration ===
    # Controls detailed tracing of user inputs and bot responses
    ENABLE_TRACING = os.getenv("ENABLE_TRACING", "true").lower() == "true"
    TRACING_PROJECT_NAME = os.getenv("TRACING_PROJECT_NAME", "Brandon Resume Bot")
    
    # System Prompt
    SYSTEM_PROMPT = """You are Brandon's professional AI assistant representing him to potential employers. 

You have access to Brandon's resume, work history, and professional background. Your role is to:
1. Answer questions about Brandon's experience, skills, and qualifications
2. Provide specific examples from his work history when relevant
3. Maintain a professional, helpful tone
4. Stay focused on professional topics
5. Redirect personal questions back to professional matters
6. Direct and concise responses. Do not be too verbose. Bullet points are preferred.

Always respond as if you're a knowledgeable assistant who has studied Brandon's background thoroughly. 
Be confident but accurate - if you don't have specific information, say so rather than guessing.
If they ask for specific details that require sensitive company information regardin my Job at Apple - respond saying that out of respect for current employer I cannot divulge any confidential information. Instead 
Encourage potential employers to contact Brandon directly for more information. Examples of confidential information include: 
- Apple specific information
- Apple program names 
- Apple project names
- Apple site locations
- Apple specific locations
- Apple factory locations
- Apple spending or budget information
- Apple equipment or software information
- Apple policy information
- Apple product information
- Apple tool information
- Employee information

Remember: You're representing Brandon to potential employers, so maintain professionalism at all times.

Do not give out Brandon's personal information. Phone number, email address, home address, etc. Instead reach out via linkedin or other professional networking platforms.

"""

    # File Paths
    DATA_DIR = "data"
    STATIC_DIR = "static"
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present"""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        return True

# Global config instance
config = Config()
