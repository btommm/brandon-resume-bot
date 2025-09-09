"""
Gradio chat interface for Brandon Resume Bot
"""

import gradio as gr
import os
from typing import List, Tuple
from .bot import resume_bot
from .config import config
# No custom logging needed - OpenAI provides comprehensive tracking

def create_interface():
    """Create and return the Gradio interface"""
    
    # Custom CSS for professional styling
    custom_css = """
    .gradio-container {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        max-width: 1000px;
        margin: 0 auto;
    }
    
    .header-text {
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    
    .chat-message {
        padding: 10px;
        margin: 5px 0;
        border-radius: 8px;
        line-height: 1.5;
    }
    
    .suggested-questions {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #007bff;
    }
    """
    
    def chat_function(message: str, history: List[Tuple[str, str]]) -> Tuple[List[Tuple[str, str]], str]:
        """Handle chat interactions"""
        if not message.strip():
            return history, ""
        
        # Generate bot response
        bot_response = resume_bot.generate_response(message)
        
        # Update history
        history.append((message, bot_response))
        
        return history, ""
    
    def reset_chat():
        """Reset the chat conversation"""
        resume_bot.reset_conversation()
        return [], ""
    
# Analytics removed - employers don't need to see tracking information
    
    def handle_suggested_question(question: str, history: List[Tuple[str, str]]) -> Tuple[List[Tuple[str, str]], str]:
        """Handle clicks on suggested questions"""
        return chat_function(question, history)
    
    # Create the interface with tabs
    with gr.Blocks(css=custom_css, title="Brandon's Resume Bot") as demo:
        
        # Header
        gr.HTML(f"""
        <div class="header-text">
            <h1>🤖 {config.BOT_NAME}</h1>
            <p>Ask me anything about Brandon's professional background, experience, and skills!</p>
        </div>
        """)
        
        # Create tabs for chat and analytics
        with gr.Tabs():
            
            # Main Chat Tab
            with gr.Tab("💬 Chat with Brandon's Bot"):
                
                # Main chat interface
                chatbot = gr.Chatbot(
                    value=[],
                    height=400,
                    show_label=False,
                    container=True,
                    bubble_full_width=False
                )
                
                # Message input
                msg = gr.Textbox(
                    placeholder="Ask me about Brandon's experience, skills, projects, or background...",
                    show_label=False,
                    container=False,
                    scale=7
                )
                
                # Control buttons
                with gr.Row():
                    submit_btn = gr.Button("Send", variant="primary", scale=1)
                    clear_btn = gr.Button("Clear Chat", variant="secondary", scale=1)
                
                # Suggested questions
                with gr.Row():
                    gr.HTML("""
                    <div class="suggested-questions">
                        <h3>💡 Try asking:</h3>
                        <p><em>Click any question below to get started!</em></p>
                    </div>
                    """)
                
                # Create buttons for suggested questions
                suggested_questions = resume_bot.get_suggested_questions()
                suggestion_buttons = []
                
                with gr.Row():
                    for i, question in enumerate(suggested_questions[:4]):  # First 4 questions
                        btn = gr.Button(question, size="sm", scale=1)
                        suggestion_buttons.append(btn)
                
                with gr.Row():
                    for i, question in enumerate(suggested_questions[4:8]):  # Next 4 questions
                        if i + 4 < len(suggested_questions):
                            btn = gr.Button(suggested_questions[i + 4], size="sm", scale=1)
                            suggestion_buttons.append(btn)
                
                # Footer info for chat tab
                gr.HTML("""
                <div style="margin-top: 30px; padding: 20px; background: #f8f9fa; border-radius: 8px; text-align: center;">
                    <p><strong>About this bot:</strong> I'm an AI assistant trained on Brandon's resume and professional background. 
                    I can answer questions about his experience, skills, projects, and qualifications.</p>
                    <p><em>This bot is designed for potential employers and professional inquiries.</em></p>
                </div>
                """)
            
# No analytics tab for public users - keep interface focused on chatting
        
        # Event handlers
        msg.submit(chat_function, inputs=[msg, chatbot], outputs=[chatbot, msg])
        submit_btn.click(chat_function, inputs=[msg, chatbot], outputs=[chatbot, msg])
        clear_btn.click(reset_chat, outputs=[chatbot, msg])
        
        # Handle suggested question clicks
        for btn in suggestion_buttons:
            btn.click(
                lambda question=btn.value: handle_suggested_question(question, chatbot.value),
                outputs=[chatbot, msg]
            )
    
    return demo

# Example usage
if __name__ == "__main__":
    demo = create_interface()
    demo.launch()
