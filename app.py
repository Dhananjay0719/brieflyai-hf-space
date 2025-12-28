import torch
import gradio as gr
from transformers import pipeline

torch.set_grad_enabled(False)

summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn",
    device=-1
)

def summarize(text):
    if not text or len(text.split()) < 30:
        return "Please provide a longer text (at least 30 words)."

    max_len = min(130, len(text.split()) // 2)
    min_len = max(30, max_len // 2)

    result = summarizer(
        text,
        max_length=max_len,
        min_length=min_len,
        do_sample=False,
        truncation=True
    )

    return result[0]["summary_text"]

demo = gr.Interface(
    fn=summarize,
    inputs=gr.Textbox(lines=10, placeholder="Paste text here..."),
    outputs="text",
    title="BrieflyAI",
    description="True abstractive text summarization using a Transformer encoder–decoder model (BART)"
)

demo.launch()