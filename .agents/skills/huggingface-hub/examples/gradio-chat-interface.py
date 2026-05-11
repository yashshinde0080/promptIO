"""
Gradio Chat Interface Example

A complete example of a chat application using Hugging Face
Inference Client with Gradio's ChatInterface.

Requirements (requirements.txt):
    huggingface_hub
    gradio

README.md header:
---
title: Chat with AI
emoji: 💬
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.0.0
app_file: app.py
pinned: false
models:
  - meta-llama/Llama-3.1-8B-Instruct
tags:
  - chat
  - llm
  - conversational
---

Environment Variables (set in Space Settings):
    HF_TOKEN: Your Hugging Face API token
"""

import os
import gradio as gr
from huggingface_hub import InferenceClient

# Initialize the Inference Client
# Token is read from HF_TOKEN environment variable
client = InferenceClient(
    api_key=os.environ.get("HF_TOKEN")
)

# Model to use for chat
MODEL_ID = "meta-llama/Llama-3.1-8B-Instruct"

# System prompt for the assistant
SYSTEM_PROMPT = """You are a helpful, friendly AI assistant. You provide clear,
accurate, and concise responses. If you're not sure about something, you say so
rather than making up information."""


def chat(
    message: str,
    history: list[tuple[str, str]],
    system_prompt: str = SYSTEM_PROMPT,
    max_tokens: int = 512,
    temperature: float = 0.7,
    top_p: float = 0.9,
) -> str:
    """
    Generate a response to a chat message.

    Args:
        message: The user's message
        history: List of (user_message, assistant_message) tuples
        system_prompt: System instructions for the model
        max_tokens: Maximum tokens to generate
        temperature: Sampling temperature (0-1)
        top_p: Nucleus sampling parameter

    Returns:
        The assistant's response
    """
    # Build messages list for chat API
    messages = [{"role": "system", "content": system_prompt}]

    # Add conversation history
    for user_msg, assistant_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": assistant_msg})

    # Add current message
    messages.append({"role": "user", "content": message})

    # Generate response
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
    )

    return response.choices[0].message.content


def chat_stream(
    message: str,
    history: list[tuple[str, str]],
    system_prompt: str = SYSTEM_PROMPT,
    max_tokens: int = 512,
    temperature: float = 0.7,
    top_p: float = 0.9,
):
    """
    Generate a streaming response to a chat message.

    Yields partial responses for real-time display.
    """
    # Build messages list
    messages = [{"role": "system", "content": system_prompt}]

    for user_msg, assistant_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": assistant_msg})

    messages.append({"role": "user", "content": message})

    # Stream response
    response_text = ""
    for chunk in client.chat.completions.create(
        model=MODEL_ID,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
        top_p=top_p,
        stream=True,
    ):
        if chunk.choices[0].delta.content:
            response_text += chunk.choices[0].delta.content
            yield response_text


# Simple ChatInterface (easiest approach)
simple_demo = gr.ChatInterface(
    fn=chat_stream,
    title="💬 Chat with Llama 3.1",
    description="Chat with Meta's Llama 3.1 8B Instruct model.",
    examples=[
        "What is machine learning?",
        "Write a haiku about programming.",
        "Explain quantum computing in simple terms.",
    ],
    additional_inputs=[
        gr.Textbox(
            value=SYSTEM_PROMPT,
            label="System Prompt",
            lines=3,
        ),
        gr.Slider(
            minimum=64,
            maximum=2048,
            value=512,
            step=64,
            label="Max Tokens",
        ),
        gr.Slider(
            minimum=0.1,
            maximum=1.0,
            value=0.7,
            step=0.1,
            label="Temperature",
        ),
        gr.Slider(
            minimum=0.1,
            maximum=1.0,
            value=0.9,
            step=0.1,
            label="Top P",
        ),
    ],
    additional_inputs_accordion=gr.Accordion(
        label="Advanced Settings",
        open=False,
    ),
)


# Advanced demo with Blocks for more control
def create_advanced_demo():
    """Create an advanced chat demo with custom UI."""

    with gr.Blocks(title="Advanced Chat") as demo:
        gr.Markdown("""
        # 💬 Advanced Chat Interface

        Chat with Llama 3.1 8B Instruct using Hugging Face Inference API.
        """)

        chatbot = gr.Chatbot(
            label="Conversation",
            height=400,
            show_copy_button=True,
        )

        with gr.Row():
            msg = gr.Textbox(
                label="Your Message",
                placeholder="Type your message here...",
                scale=4,
                show_label=False,
            )
            submit = gr.Button("Send", variant="primary", scale=1)

        with gr.Accordion("Settings", open=False):
            system_prompt = gr.Textbox(
                value=SYSTEM_PROMPT,
                label="System Prompt",
                lines=3,
            )
            with gr.Row():
                max_tokens = gr.Slider(64, 2048, 512, step=64, label="Max Tokens")
                temperature = gr.Slider(0.1, 1.0, 0.7, step=0.1, label="Temperature")
                top_p = gr.Slider(0.1, 1.0, 0.9, step=0.1, label="Top P")

        clear = gr.Button("Clear Chat")

        def respond(message, chat_history, sys_prompt, max_tok, temp, tp):
            """Handle chat response."""
            # Get streaming response
            bot_message = ""
            for partial in chat_stream(
                message,
                chat_history,
                sys_prompt,
                max_tok,
                temp,
                tp
            ):
                bot_message = partial
                yield "", chat_history + [(message, bot_message)]

        # Event handlers
        submit.click(
            respond,
            [msg, chatbot, system_prompt, max_tokens, temperature, top_p],
            [msg, chatbot],
        )

        msg.submit(
            respond,
            [msg, chatbot, system_prompt, max_tokens, temperature, top_p],
            [msg, chatbot],
        )

        clear.click(lambda: [], outputs=[chatbot])

        gr.Markdown("""
        ---
        **Model:** [meta-llama/Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct)

        Powered by [Hugging Face Inference Providers](https://huggingface.co/docs/inference-providers)
        """)

    return demo


advanced_demo = create_advanced_demo()

# Launch
if __name__ == "__main__":
    # Use simple_demo for basic chat, advanced_demo for full features
    simple_demo.launch()
