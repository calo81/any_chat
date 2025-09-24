import os
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI
import json

# Load environment variables
load_dotenv()

class AnyChatAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.resources = os.getenv("RESOURCES", "web_search,file_reader,code_interpreter").split(",")
        self.tools = os.getenv("TOOLS", "search,analyze,generate").split(",")
        
    def chat(self, message, history):
        """Main chat function that processes user messages"""
        try:
            # Prepare context from environment variables
            context = f"""
            You are an AI agent with access to these resources: {', '.join(self.resources)}
            You can use these tools: {', '.join(self.tools)}
            
            Please respond to the user's message in a helpful and informative way.
            """
            
            # Convert history to OpenAI format
            messages = [{"role": "system", "content": context}]
            
            # Add conversation history
            for user_msg, assistant_msg in history:
                messages.append({"role": "user", "content": user_msg})
                if assistant_msg:
                    messages.append({"role": "assistant", "content": assistant_msg})
            
            # Add current message
            messages.append({"role": "user", "content": message})
            
            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def get_system_info(self):
        """Return system information for debugging"""
        return f"""
        System Information:
        - Resources: {', '.join(self.resources)}
        - Tools: {', '.join(self.tools)}
        - OpenAI API Key: {'Set' if os.getenv('OPENAI_API_KEY') else 'Not Set'}
        """

def create_gradio_interface():
    agent = AnyChatAgent()
    
    with gr.Blocks(title="Any Chat - AI Agent", theme=gr.themes.Soft()) as interface:
        gr.Markdown("# 🤖 Any Chat - AI Agent")
        gr.Markdown("Deploy an AI Agent about anything in Kubernetes using OpenAI Agents SDK")
        
        with gr.Tab("Chat"):
            chatbot = gr.Chatbot(
                label="AI Agent",
                height=500,
                show_label=True,
                container=True,
                bubble_full_width=False
            )
            
            msg = gr.Textbox(
                label="Your Message",
                placeholder="Ask me anything...",
                lines=2,
                max_lines=5
            )
            
            with gr.Row():
                submit_btn = gr.Button("Send", variant="primary")
                clear_btn = gr.Button("Clear Chat", variant="secondary")
            
            # Event handlers
            def respond(message, chat_history):
                if not message.strip():
                    return chat_history, ""
                
                bot_message = agent.chat(message, chat_history)
                chat_history.append((message, bot_message))
                return chat_history, ""
            
            def clear_chat():
                return [], ""
            
            submit_btn.click(respond, [msg, chatbot], [chatbot, msg])
            msg.submit(respond, [msg, chatbot], [chatbot, msg])
            clear_btn.click(clear_chat, outputs=[chatbot, msg])
        
        with gr.Tab("System Info"):
            gr.Markdown("## System Configuration")
            system_info = gr.Textbox(
                value=agent.get_system_info(),
                label="Current Configuration",
                lines=10,
                interactive=False
            )
            
            refresh_btn = gr.Button("Refresh")
            refresh_btn.click(
                lambda: agent.get_system_info(),
                outputs=system_info
            )
    
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