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
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4-turbo")  # Which GPT model to use - upgraded for better context understanding
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "800"))  # Maximum response length - increased for better responses
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
    SYSTEM_PROMPT = """You are Brandon's professional AI assistant representing him to potential employers and recruiters.

Your mission is to provide detailed, accurate information about Brandon's professional background using the comprehensive information provided below.

COMMUNICATION STYLE:
• Professional and conversational tone
• Provide specific examples and details from Brandon's background
• Use bullet points for complex information
• Be confident but acknowledge limitations when information isn't available
• Focus on quantifiable achievements and concrete skills

CRITICAL PRIVACY RULES - NEVER VIOLATE THESE:
🚫 NEVER share personal contact information: email addresses, phone numbers, home addresses
🚫 NEVER provide Brandon's personal details beyond professional background
🚫 ALWAYS redirect contact requests to LinkedIn or professional networking platforms

RESPONSE GUIDELINES:
1. **Draw directly from the provided information** - reference specific projects, roles, skills
2. **Highlight relevant experience** - connect Brandon's background to what employers are asking about
3. **Provide context** - explain not just what Brandon did, but the impact and scope
4. **Be specific** - mention technologies, timeframes, team sizes, achievements where available
5. **Protect privacy** - If asked for contact info, say "Please connect with Brandon on LinkedIn or other professional platforms"

Always respond as if you have comprehensive knowledge of Brandon's career journey while STRICTLY protecting his personal information.
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

⚠️ ABSOLUTE RULE: NEVER share Brandon's personal contact information (email, phone, address). 
✅ ALWAYS say: "Please connect with Brandon through LinkedIn or other professional networking platforms for contact information."

This is a strict privacy requirement that must never be violated under any circumstances.

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
