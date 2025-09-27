import os
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI
import json
from cac_agents import PersonaAgent

# Load environment variables
load_dotenv()

agents = []

if os.getenv("CV_AGENT") == "true":
    agents.append(PersonaAgent())

CHAT_TITLE = os.getenv("CHAT_TITLE", "Any Cjjjhat")
CHAT_IMAGE_URL = os.getenv("CHAT_IMAGE_URL", "https://cdn.theorg.com/f4672ad5-4913-4279-9ddf-54c18d2f0f95_thumb.jpg")

class AnyChatAgent:
    def __init__(self):
        
        self.agents = agents
        
    async def chat(self, message, history):
        """Main chat function that processes user messages"""
        try:
            # Build conversation context from history
            conversation_context = ""
            if history:
                for user_msg, assistant_msg in history:
                    conversation_context += f"User: {user_msg}\n"
                    if assistant_msg:
                        conversation_context += f"Assistant: {assistant_msg}\n"
            
            # Add current message
            conversation_context += f"User: {message}\n"
            
            # Use the persona agent to generate a response with full context
            result = await self.agents[0].run(conversation_context)
            return result.final_output if hasattr(result, 'final_output') else str(result)
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    
    def get_system_info(self):
        """Return system information for debugging"""
        return f"""
        System Information:
        - OpenAI API Key: {'Set' if os.getenv('OPENAI_API_KEY') else 'Not Set'}
        """

def create_gradio_interface():
    agent = AnyChatAgent()
    
    # Create Google-themed interface with CSS
    google_theme = gr.themes.Soft(
        primary_hue="blue",
        neutral_hue="gray",
        font=gr.themes.GoogleFont("Roboto"),
    )
    
    # Load CSS from external file
    css_file_path = os.path.join(os.path.dirname(__file__), "styles.css")
    with open(css_file_path, "r") as f:
        custom_css = f.read()
    
    with gr.Blocks(title=CHAT_TITLE, theme=google_theme, css=custom_css) as interface:
        # Professional ChatGPT-style header
        with gr.Row():
            gr.HTML("""
            <div style="display: flex; align-items: center; padding: 20px 0; border-bottom: 1px solid #565869; background: #171717;">
                <div style="display: flex; align-items: center; gap: 16px; width: 100%;">
                    <div><img src=" """+ CHAT_IMAGE_URL + """ "/></div>
                    <div style="flex: 1;">
                        <h1 style="margin: 0; color: #ececf1; font-size: 24px; font-weight: 600; letter-spacing: -0.5px;">""" + CHAT_TITLE + """</h1>
                        <p style="margin: 4px 0 0 0; color: #8e8ea0; font-size: 14px; font-weight: 400;">Professional AI Assistant powered by OpenAI</p>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <div style="width: 8px; height: 8px; background: #10a37f; border-radius: 50%; animation: pulse 2s infinite;"></div>
                        <span style="color: #8e8ea0; font-size: 12px; font-weight: 500;">Online</span>
                    </div>
                </div>
            </div>
            <style>
                @keyframes pulse {
                    0%, 100% { opacity: 1; }
                    50% { opacity: 0.5; }
                }
            </style>
            """)
        
        with gr.Tab("💬 Chat"):
            chatbot = gr.Chatbot(
                label="",
                height=500,
                show_label=False,
                container=True,
                bubble_full_width=False,
                avatar_images=("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", "https://cdn-icons-png.flaticon.com/512/4712/4712027.png")
            )
            
            with gr.Row():
                with gr.Column(scale=1):
                    with gr.Row():
                        msg = gr.Textbox(
                            label="",
                            placeholder="Message Any Chat...",
                            lines=1,
                            max_lines=5,
                            container=False,
                            show_label=False
                        )
                    # submit_btn = gr.Button("Send", variant="primary", size="sm")
                    # clear_btn = gr.Button("Clear Chat", variant="secondary", size="sm")
            
            # Event handlers
            async def respond(message, chat_history):
                if not message.strip():
                    return chat_history, ""
                
                bot_message = await agent.chat(message, chat_history)
                chat_history.append((message, bot_message))
                return chat_history, ""
            
            def clear_chat():
                return [], ""
            
            # submit_btn.click(respond, [msg, chatbot], [chatbot, msg])
            msg.submit(respond, [msg, chatbot], [chatbot, msg])
            # clear_btn.click(clear_chat, outputs=[chatbot, msg])
        
        with gr.Tab("⚙️ System Info"):
            with gr.Column():
                gr.HTML("""
                <div style="padding: 20px 0;">
                    <h2 style="color: #ececf1; margin: 0 0 8px 0; font-size: 20px; font-weight: 600;">System Configuration</h2>
                    <p style="color: #8e8ea0; margin: 0; font-size: 14px; font-weight: 400;">Current agent configuration and status</p>
                </div>
                """)
                
                system_info = gr.Textbox(
                    value=agent.get_system_info(),
                    label="",
                    lines=12,
                    interactive=False,
                    show_label=False,
                    container=True
                )
                
                with gr.Row():
                    refresh_btn = gr.Button("🔄 Refresh", variant="primary")
                    gr.HTML("<div></div>")  # Spacer
    
    return interface

if __name__ == "__main__":
    # Get server configuration from environment
    server_name = os.getenv("GRADIO_SERVER_NAME", "0.0.0.0")
    server_port = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
    
    # Create and launch the interface
    interface = create_gradio_interface()
    interface.launch(
        server_name=server_name,
        server_port=server_port,
        share=False,
        debug=False
    )