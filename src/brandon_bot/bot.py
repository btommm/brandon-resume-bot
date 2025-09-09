"""
Core bot logic for Brandon Resume Bot
Handles OpenAI Agents SDK integration and response generation

This module contains the main ResumeBot class that:
- Manages conversations using OpenAI's Agents SDK
- Integrates with document processing for context-aware responses
- Handles conversation memory and context management
- Tracks interactions using built-in SDK tracing
"""

import asyncio
import time
import uuid
from typing import List, Dict, Optional
from agents import Agent, Runner, trace
from .config import config
from .document_processor import document_processor


class ResumeBot:
    """Main bot class for handling conversations about Brandon's resume using OpenAI Agents SDK"""
    
    def __init__(self):
        self.agent = None
        self.conversation_history = []
        self.session_id = None
        self.conversation_trace = None
        self.trace_context = None
        self._load_documents()
        self._initialize_agent()
    
    def _initialize_agent(self):
        """Initialize OpenAI Agent"""
        try:
            config.validate()
            
            # Build the system instructions with document context
            instructions = self._build_system_instructions()
            
            # Create the agent with OpenAI Agents SDK
            self.agent = Agent(
                name=config.BOT_NAME,
                instructions=instructions,
                model=config.MODEL_NAME,
                # SDK handles API key automatically from OPENAI_API_KEY env var
            )
            
        except Exception as e:
            print(f"Error initializing OpenAI Agent: {e}")
            self.agent = None
    
    def _load_documents(self):
        """Load all resume documents"""
        try:
            documents = document_processor.load_all_documents()
            print(f"Loaded documents: {list(documents.keys())}")
        except Exception as e:
            print(f"Error loading documents: {e}")
    
    def _build_system_instructions(self) -> str:
        """Build the system instructions with document context"""
        base_instructions = config.SYSTEM_PROMPT
        
        # Add document context
        context = document_processor.processed_content
        if context:
            print(f"📄 Adding resume content to prompt ({len(context)} characters)")
            base_instructions += f"\n\nHere is Brandon's resume and professional information:\n\n{context}"
        else:
            print("⚠️  WARNING: No resume content found to add to prompt!")
        
        print(f"🤖 Final prompt length: {len(base_instructions)} characters")
        return base_instructions
    
    async def _generate_response_async(self, user_message: str) -> str:
        """
        Generate a response to the user's message using OpenAI Agents SDK
        
        This method:
        1. Validates the input message
        2. Uses the Agent/Runner pattern to generate response
        3. Leverages built-in SDK tracing
        4. Updates conversation history
        
        Args:
            user_message: The user's question or comment
            
        Returns:
            The bot's response string
        """
        # Validate agent initialization
        if not self.agent:
            return "I'm sorry, but I'm having trouble connecting to my AI service. Please try again later."
        
        # Validate user input
        if not user_message.strip():
            return "Please ask me a question about Brandon's background, experience, or skills!"
        
        try:
            # Ensure we have a session and trace context
            if not self.session_id or not self.trace_context:
                self.start_new_conversation()
            
            # Use Runner within the existing trace context (no new trace created)
            result = await Runner.run(
                self.agent,
                user_message,
                # The SDK automatically handles conversation context and tracing
            )
            
            # Extract the response
            bot_response = result.final_output.strip()
            
            # Update conversation history for analytics
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": bot_response})
            
            return bot_response
                
        except Exception as e:
            # Handle any errors that occur during response generation
            error_msg = f"Error generating response: {e}"
            print(error_msg)
            return "I apologize, but I encountered an error while processing your question. Please try rephrasing or ask something else about Brandon's background."
    
    def generate_response(self, user_message: str) -> str:
        """
        Synchronous wrapper for the async response generation
        
        This method provides backward compatibility with the existing chat interface
        while using the async Agent/Runner pattern internally.
        """
        # Record start time for performance tracking
        start_time = time.time()
        
        try:
            # Run the async method in the current event loop or create a new one
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If we're already in an async context, we need to handle this differently
                    # For now, we'll use asyncio.create_task for compatibility
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(asyncio.run, self._generate_response_async(user_message))
                        response = future.result()
                else:
                    response = loop.run_until_complete(self._generate_response_async(user_message))
            except RuntimeError:
                # No event loop running, create a new one
                response = asyncio.run(self._generate_response_async(user_message))
            
            # Calculate response time for performance tracking
            response_time_ms = (time.time() - start_time) * 1000
            
            if config.ENABLE_TRACING:
                print(f"[TRACE] Response Time: {response_time_ms:.2f}ms")
            
            return response
            
        except Exception as e:
            error_msg = f"Error in sync wrapper: {e}"
            print(error_msg)
            return "I apologize, but I encountered an error while processing your question. Please try rephrasing or ask something else about Brandon's background."
    
    async def generate_response_with_trace(self, user_message: str, trace_name: str = None) -> str:
        """
        Generate a response with custom trace name - useful for different interaction types
        
        Args:
            user_message: The user's question or comment
            trace_name: Custom name for the trace (if None, uses session-based tracing)
            
        Returns:
            The bot's response string
        """
        if not self.agent:
            return "I'm sorry, but I'm having trouble connecting to my AI service. Please try again later."
        
        if not user_message.strip():
            return "Please ask me a question about Brandon's background, experience, or skills!"
        
        try:
            # Use session-based tracing if no custom trace name provided
            if trace_name is None:
                # Ensure we have a session and trace context
                if not self.session_id or not self.trace_context:
                    self.start_new_conversation()
                
                # Use existing trace context
                result = await Runner.run(
                    self.agent,
                    user_message,
                )
            else:
                # Use custom trace name
                with trace(trace_name):
                    result = await Runner.run(
                        self.agent,
                        user_message,
                    )
                
                bot_response = result.final_output.strip()
                
                # Update conversation history
                self.conversation_history.append({"role": "user", "content": user_message})
                self.conversation_history.append({"role": "assistant", "content": bot_response})
                
                return bot_response
                
        except Exception as e:
            error_msg = f"Error generating response: {e}"
            print(error_msg)
            return "I apologize, but I encountered an error while processing your question. Please try rephrasing or ask something else about Brandon's background."
    
    def get_suggested_questions(self) -> List[str]:
        """Get a list of suggested questions for users"""
        return [
            "What is Brandon's professional background?",
            "What programming languages does Brandon know?",
            "Tell me about Brandon's work experience",
            "What projects has Brandon worked on?",
            "What are Brandon's technical skills?",
            "What education does Brandon have?",
            "Has Brandon worked with machine learning?",
            "What frameworks and tools does Brandon use?"
        ]
    
    def start_new_conversation(self):
        """Start a new conversation session with a unique trace"""
        # Close previous trace if exists
        if self.trace_context:
            try:
                self.trace_context.__exit__(None, None, None)
            except:
                pass
        
        self.session_id = str(uuid.uuid4())
        self.conversation_history = []
        
        # Create a persistent trace context for the entire session
        session_trace_name = f"Brandon Resume Bot - Session {self.session_id[:8]}"
        self.trace_context = trace(session_trace_name)
        self.trace_context.__enter__()
        
        print(f"🆕 Started new conversation session: {self.session_id[:8]}...")
        return self.session_id
    
    def reset_conversation(self):
        """Reset the conversation history but keep the same session"""
        self.conversation_history = []
        # Note: The Agent SDK handles its own conversation context automatically
        # This method mainly affects our local tracking
    
    def get_conversation_summary(self) -> str:
        """Get a summary of the current conversation"""
        if not self.conversation_history:
            return "No conversation yet."
        
        message_count = len(self.conversation_history) // 2
        return f"Conversation with {message_count} exchanges"
    
    def end_conversation(self):
        """End the current conversation and close the trace context"""
        if self.trace_context:
            try:
                self.trace_context.__exit__(None, None, None)
                self.trace_context = None
                print(f"🔚 Ended conversation session: {self.session_id[:8] if self.session_id else 'Unknown'}...")
            except:
                pass
        self.session_id = None
    
    def reinitialize_agent(self):
        """Reinitialize the agent (useful if documents change)"""
        self._load_documents()
        self._initialize_agent()


# Global bot instance
resume_bot = ResumeBot()