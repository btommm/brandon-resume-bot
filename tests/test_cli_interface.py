#!/usr/bin/env python3
"""
Command Line Test Interface for Brandon Resume Bot

This script provides a simple command line interface to test the bot functionality
without launching the full Gradio web interface.

Usage:
    poetry run python tests/test_cli_interface.py
"""

import os
import sys

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from brandon_bot.bot import resume_bot
from brandon_bot.config import config
from brandon_bot.document_processor import document_processor

def print_banner():
    """Print a welcome banner"""
    print("=" * 60)
    print(f"🤖 {config.BOT_NAME} - Command Line Test Interface")
    print("=" * 60)
    print("Commands:")
    print("  'help'    - Show suggested questions")
    print("  'docs'    - Show loaded documents")
    print("  'debug'   - Show raw resume content")
    print("  'reload'  - Reload documents from data folder")
    print("  'reset'   - Clear conversation history")
    print("  'test'    - Run automated tests")
    print("  'quit'    - Exit")
    print("-" * 60)

def print_help():
    """Print suggested questions"""
    print("\n💡 Suggested questions:")
    questions = resume_bot.get_suggested_questions()
    for i, question in enumerate(questions, 1):
        print(f"  {i}. {question}")
    print()

def check_environment():
    """Check if the environment is properly configured"""
    try:
        config.validate()
        print("✅ Environment configuration is valid")
        return True
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\nTo fix this:")
        print("1. Copy env.example to .env")
        print("2. Edit .env and add your OpenAI API key")
        print("3. Run this script again")
        return False

def show_loaded_documents():
    """Show information about loaded documents"""
    print("\n📄 Document Status:")
    print("-" * 40)
    
    # Show document summary
    summary = document_processor.get_document_summary()
    print(summary)
    
    # Show specific details about each document
    if document_processor.documents:
        print("\nDocument Details:")
        for doc_name, content in document_processor.documents.items():
            content_preview = content[:100].replace('\n', ' ')
            if len(content) > 100:
                content_preview += "..."
            print(f"  📄 {doc_name}: {len(content)} chars - {content_preview}")
    else:
        print("\n⚠️  No documents loaded!")
        print("Place your resume files in: data/")
        print("Supported formats: PDF, DOCX, TXT, MD")
    print()

def reload_documents():
    """Reload documents and reinitialize the bot"""
    print("\n🔄 Reloading documents...")
    
    # Reload documents
    documents = document_processor.load_all_documents()
    
    # Reinitialize the bot with new documents
    resume_bot.reinitialize_agent()
    
    print(f"✅ Reloaded {len(documents)} documents")
    show_loaded_documents()

def show_debug_info():
    """Show debug information about the resume content"""
    print("\n🔍 DEBUG: Raw Resume Content")
    print("=" * 60)
    
    if document_processor.processed_content:
        content = document_processor.processed_content
        print(f"Content length: {len(content)} characters")
        print("\nFirst 500 characters:")
        print("-" * 40)
        print(content[:500])
        print("-" * 40)
        
        print(f"\nLast 500 characters:")
        print("-" * 40)
        print(content[-500:])
        print("-" * 40)
        
        # Check for key resume sections
        content_lower = content.lower()
        print(f"\nContent analysis:")
        print(f"  Contains 'education': {'✅' if 'education' in content_lower else '❌'}")
        print(f"  Contains 'experience': {'✅' if 'experience' in content_lower else '❌'}")
        print(f"  Contains 'skills': {'✅' if 'skills' in content_lower else '❌'}")
        print(f"  Contains 'university' or 'college': {'✅' if ('university' in content_lower or 'college' in content_lower) else '❌'}")
        
    else:
        print("❌ No content loaded!")
    
    print("\n" + "=" * 60)

def run_automated_tests():
    """Run some basic automated tests"""
    print("\n🧪 Running automated tests...")
    
    # Test 1: Check if bot initializes
    print("Test 1: Bot initialization...", end=" ")
    if resume_bot.agent is not None:
        print("✅ PASS")
    else:
        print("❌ FAIL - Bot not initialized")
        return False
    
    # Test 2: Check suggested questions
    print("Test 2: Suggested questions...", end=" ")
    questions = resume_bot.get_suggested_questions()
    if len(questions) > 0:
        print("✅ PASS")
    else:
        print("❌ FAIL - No suggested questions")
        return False
    
    # Test 3: Try to get a response (if API key is available)
    print("Test 3: Bot response generation...", end=" ")
    try:
        if config.OPENAI_API_KEY:
            response = resume_bot.generate_response("What is your name?")
            if response and len(response) > 0:
                print("✅ PASS")
            else:
                print("❌ FAIL - Empty response")
                return False
        else:
            print("⚠️  SKIP - No API key configured")
    except Exception as e:
        print(f"❌ FAIL - Error: {e}")
        return False
    
    print("✅ All tests completed successfully!")
    return True

def main():
    """Main command line interface"""
    print_banner()
    
    # Check environment configuration
    env_ok = check_environment()
    
    # Check if bot initialized successfully
    if not resume_bot.agent:
        print("⚠️  Bot failed to initialize. This might be due to missing API key.")
        if not env_ok:
            print("Please configure your environment first.")
            return
    else:
        print("✅ Bot initialized successfully!")
    
    print("\nYou can now ask questions about Brandon's resume and background.")
    print("The bot will respond just like in the web interface.\n")
    
    conversation_count = 0
    
    while True:
        try:
            # Get user input
            user_input = input("👤 You: ").strip()
            
            # Handle special commands
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            elif user_input.lower() == 'help':
                print_help()
                continue
            elif user_input.lower() == 'debug':
                show_debug_info()
                continue
            elif user_input.lower() == 'test':
                run_automated_tests()
                continue
            elif user_input.lower() == 'reset':
                resume_bot.reset_conversation()
                conversation_count = 0
                print("🔄 Conversation history cleared!")
                continue
            elif not user_input:
                print("Please enter a question or type 'help' for suggestions.")
                continue
            
            # Generate bot response
            if not resume_bot.agent:
                print("❌ Bot is not properly initialized. Please check your configuration.")
                continue
                
            print("🤖 Thinking...")
            bot_response = resume_bot.generate_response(user_input)
            
            # Display response
            print(f"🤖 {config.BOT_NAME}: {bot_response}\n")
            
            conversation_count += 1
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Please try again or type 'quit' to exit.\n")

if __name__ == "__main__":
    main()
