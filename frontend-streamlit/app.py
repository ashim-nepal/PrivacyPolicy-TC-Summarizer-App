import streamlit as st
from transformers import AutoTokenizer, TFT5ForConditionalGeneration
import os


# Loading the modle and tokenizer
model_path = os.path.join(os.path.dirname(__file__), '..', 'model_')

# Loading Tokenizer ad tf model from model folder
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = TFT5ForConditionalGeneration.from_pretrained(model_path, from_pt=False)
    

def get_summary(text: str, max_len: int = 150, min_len: int=40):
    inputs = tokenizer("Summary: "+ text , return_tensors= "tf", max_length = 512, truncation = True)
    
    outputs = model.generate(inputs["input_ids"], max_length = max_len, min_length = min_len, num_beams = 4, early_stopping = True)
    
    
    summary = tokenizer.decode(outputs[0], skip_special_tokens = True)
    
    return summary

# Streamlit page

st.markdown("""
    <style>
        body {
            background: linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d);
            background-attachment: fixed;
            color: white;
        }
        .main {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(12px);
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.25);
        }
        textarea {
            border-radius: 12px !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
            background: rgba(0,0,0,0.35) !important;
            color: white !important;
        }
        textarea::placeholder {
            background: linear-gradient(90deg, #00c6ff, #0072ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-style: italic;
            font-weight: 500;
        }
    </style>
""", unsafe_allow_html=True)


st.title("Privacy & Policy (Text) Summarizer - Ashim Nepal")
st.markdown("## Privacy & Policy (Text) Summarizer AI")

st.markdown('Paste any privacy terms or text below and get an instant summary!')

user_input = st.text_area("Paste your text here", placeholder="Paste your privacy policy or terms of service here...", height=200)


if st.button("Summarize"):
    if user_input.strip():
        with st.spinner("Analysing text and generating the summary..."):
            summary = get_summary(user_input)
        st.subheader("✨ Summary")
        st.success(summary)
    else:
        st.warning("Add some text in the text field first!")
        
st.markdown("--")
st.markdown("<div style='text-align:center; opacity:0.7;'>Built with ❤️ using Streamlit + Transformers</div>", unsafe_allow_html=True)