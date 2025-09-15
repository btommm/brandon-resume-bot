import gradio as gr
from typing import List
from .bot import resume_bot

def create_interface():
    """Create a clean, Grok-inspired chat interface with wider/taller input and smaller send button"""
    
    custom_css = """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    
    /* Global reset */
    .gradio-container {
        font-family: "Inter", -apple-system, BlinkMacSystemFont, sans-serif !important;
        background: #1A1A1A !important;
        margin: 0 !important;
        padding: 0 !important;
        height: 100vh !important;
        overflow: hidden !important;
        color: #E0E0E0 !important;
    }
    
    /* Main container - compact, centered */
    .chat-app {
        display: flex;
        flex-direction: column;
        min-height: 100vh;
        background: #1A1A1A;
        color: #E0E0E0;
        align-items: center;
        justify-content: center;
        padding: 20px;
    }
    
    /* Header */
    .header {
        background: linear-gradient(180deg, #2A2A2A 0%, #1A1A1A 100%);
        padding: 20px;
        text-align: center;
        border-bottom: 1px solid #333333;
        width: 100%;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .title {
        color: #FFFFFF;
        font-size: 28px;
        font-weight: 600;
        margin: 0;
    }
    
    .subtitle {
        color: #A0A0A0;
        font-size: 14px;
        font-weight: 400;
        margin: 4px 0 0 0;
        opacity: 0.7;
    }
    
    /* Chat area - centered, compact */
    .chat-area {
        display: flex;
        flex-direction: column;
        max-width: 1600px;
        width: 100%;
        padding: 20px;
        box-sizing: border-box;
        margin: 0 auto;
        align-items: center;
        justify-content: center;
        min-height: 0;
    }
    
    /* Chatbot messages */
    .chatbot-container {
        background: transparent !important;
        border-radius: 12px;
        padding: 10px;
    }
    
    .chatbot-interface {
        background: transparent !important;
        color: #E0E0E0 !important;
        font-size: 16px !important;
        line-height: 1.5 !important;
    }
    
    /* Message bubbles */
    .gr-chatbot .message.user {
        background: #0A84FF !important;
        color: #FFFFFF !important;
        border-radius: 12px 12px 0 12px !important;
        padding: 10px 14px !important;
        margin: 8px 0 !important;
        max-width: 80% !important;
        align-self: flex-end !important;
    }
    
    .gr-chatbot .message.assistant {
        background: #2A2A2A !important;
        color: #E0E0E0 !important;
        border-radius: 12px 12px 12px 0 !important;
        padding: 10px 14px !important;
        margin: 8px 0 !important;
        max-width: 80% !important;
        align-self: flex-start !important;
    }
    
    /* Input area - centered, higher, wider */
    .input-area {
        background: #1A1A1A !important;
        padding: 12px 20px !important;
        border-top: 1px solid #333333 !important;
        width: 100%;
        max-width: 1600px;
        box-sizing: border-box;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        gap: 10px;
    }
    
    /* Text input - taller and wider */
    .gr-textbox {
        background: #2A2A2A !important;
        border: 1px solid #404040 !important;
        border-radius: 12px !important;
        color: #E0E0E0 !important;
        padding: 16px 20px !important;
        font-size: 16px !important;
        resize: none !important;
        flex: 4;
        min-height: 60px;
        box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.2);
        transition: border-color 0.2s, box-shadow 0.2s;
    }
    
    .gr-textbox:focus {
        border-color: #0A84FF !important;
        outline: none !important;
        box-shadow: 0 0 0 3px rgba(10, 132, 255, 0.3) !important;
    }
    
    .gr-textbox::placeholder {
        color: #808080 !important;
    }
    
    /* Send button - much smaller */
    .gr-button {
        background: #0A84FF !important;
        border: none !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
        font-weight: 500 !important;
        padding: 8px 12px !important;
        transition: background 0.2s ease !important;
        min-width: auto !important;
        font-size: 14px !important;
        flex: 0 0 auto;
    }
    
    .gr-button:hover {
        background: #0066CC !important;
    }
    
    .clear-btn {
        background: #333333 !important;
        margin-top: 12px !important;
        width: fit-content !important;
        display: block !important;
        margin-left: auto !important;
        margin-right: 20px !important;
    }
    
    .clear-btn:hover {
        background: #444444 !important;
    }
    
    /* Hide Gradio footer */
    .gr-footer {
        display: none !important;
    }
    
    /* Scrollbar styling */
    .chat-area::-webkit-scrollbar {
        width: 8px;
    }
    
    .chat-area::-webkit-scrollbar-track {
        background: #1A1A1A;
    }
    
    .chat-area::-webkit-scrollbar-thumb {
        background: #404040;
        border-radius: 4px;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .chat-area {
            padding: 10px;
            max-width: 100%;
        }
        
        .input-area {
            padding: 12px !important;
            max-width: 100%;
            flex-direction: column;
            gap: 8px;
        }
        
        .gr-textbox {
            font-size: 14px !important;
            padding: 12px 16px !important;
            min-height: 48px;
            flex: 1;
        }
        
        .gr-button {
            padding: 6px 10px !important;
            font-size: 13px !important;
        }
        
        .title {
            font-size: 24px;
        }
    }
    """
    
    def chat_function(message: str, history: List) -> tuple[List, str]:
        """Handle chat interactions with Gradio 5.x message format"""
        if not message.strip():
            return history, ""
        
        if not history:
            resume_bot.start_new_conversation()
        
        try:
            bot_response = resume_bot.generate_response(message)
        except Exception as e:
            bot_response = f"Error: Unable to generate response. {str(e)}"
        
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": bot_response})
        return history, ""
    
    def reset_chat():
        """Reset the chat conversation"""
        resume_bot.reset_conversation()
        return [{
            "role": "assistant", 
            "content": "👋 Hi! I'm Brandon-Bot, your AI assistant for learning about Brandon's professional background. Ask me about his skills, experience, projects, or anything else related to his career!"
        }], ""
    
    with gr.Blocks(
        css=custom_css, 
        title="Brandon-Bot | AI Career Assistant",
        head="<meta name='viewport' content='width=device-width, initial-scale=1.0'>"
    ) as demo:
        with gr.Column(elem_classes="chat-app"):
            gr.HTML("""
                <div class="header">
                    <h1 class="title">Brandon-Bot</h1>
                    <p class="subtitle">Your AI assistant for exploring Brandon's career and skills</p>
                </div>
            """)
            
            with gr.Column(elem_classes="chat-area"):
                 chatbot = gr.Chatbot(
                     value=[{
                         "role": "assistant", 
                         "content": "👋 Hi! I'm Brandon-Bot, your AI assistant for learning about Brandon's professional background. Ask me about his skills, experience, projects, or anything else related to his career!"
                     }],
                     height=780,
                     show_label=False,
                     container=True,
                     elem_classes="chatbot-interface",
                     type="messages",
                     autoscroll=True
                 )
                 
                 with gr.Row(elem_classes="input-area"):
                     msg = gr.Textbox(
                         placeholder="Ask about Brandon's skills, projects, or experience...",
                         container=False,
                         show_label=False,
                         lines=1,
                         max_lines=1,
                         scale=8
                     )
                     send_btn = gr.Button("Send", scale=1)
                 
                 clear_btn = gr.Button("Clear Chat", elem_classes="clear-btn", size="sm")
        
        msg.submit(chat_function, [msg, chatbot], [chatbot, msg])
        send_btn.click(chat_function, [msg, chatbot], [chatbot, msg])
        clear_btn.click(reset_chat, outputs=[chatbot, msg])
    
    return demo