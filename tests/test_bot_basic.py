"""
Basic tests for Brandon Resume Bot functionality

These tests can run with or without an API key to verify basic functionality.
"""

import os
import sys

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from brandon_bot.bot import resume_bot
from brandon_bot.config import config

def test_bot_import():
    """Test that the bot can be imported successfully"""
    assert resume_bot is not None
    print("✅ Bot import successful")

def test_config_loading():
    """Test that config loads properly"""
    assert config is not None
    assert config.BOT_NAME is not None
    assert config.MODEL_NAME is not None
    print("✅ Config loading successful")

def test_suggested_questions():
    """Test that suggested questions are available"""
    questions = resume_bot.get_suggested_questions()
    assert isinstance(questions, list)
    assert len(questions) > 0
    print(f"✅ Found {len(questions)} suggested questions")

def test_conversation_reset():
    """Test conversation reset functionality"""
    # Add some fake history
    resume_bot.conversation_history = [{"role": "user", "content": "test"}]
    assert len(resume_bot.conversation_history) > 0
    
    # Reset conversation
    resume_bot.reset_conversation()
    assert len(resume_bot.conversation_history) == 0
    print("✅ Conversation reset works")

def test_environment_check():
    """Test environment configuration check"""
    try:
        config.validate()
        print("✅ Environment validation passed")
        return True
    except ValueError as e:
        print(f"⚠️  Environment validation failed: {e}")
        return False

def run_all_tests():
    """Run all basic tests"""
    print("🧪 Running basic bot tests...\n")
    
    try:
        test_bot_import()
        test_config_loading()
        test_suggested_questions()
        test_conversation_reset()
        has_api_key = test_environment_check()
        
        print(f"\n✅ All basic tests passed!")
        
        if has_api_key:
            print("🔑 API key is configured - you can test live responses")
        else:
            print("⚠️  No API key configured - add OPENAI_API_KEY to .env for live testing")
            
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
