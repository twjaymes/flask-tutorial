from transformers import pipeline

# Load the summarization pipeline
summarizer = pipeline("summarization")

def summarize_text(text):
    # Perform summarization
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']