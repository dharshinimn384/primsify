import streamlit as st
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import fitz  # PyMuPDF

# Load model directly
tokenizer = AutoTokenizer.from_pretrained("UNIST-Eunchan/Research-Paper-Summarization-Pegasus-x-ArXiv")
summarization_model = AutoModelForSeq2SeqLM.from_pretrained("UNIST-Eunchan/Research-Paper-Summarization-Pegasus-x-ArXiv")

# Load question-answering model
qa_pipeline = pipeline(task="question-answering", model="deepset/bert-large-uncased-whole-word-masking-squad2")

def generate_summary(document):
    # Tokenize the input document
    inputs = tokenizer(document, return_tensors="pt", max_length=1024, truncation=True)

    # Generate summary
    summary_ids = summarization_model.generate(inputs["input_ids"], max_length=150, length_penalty=2.0, num_beams=4, early_stopping=True)
    
    # Decode and return the generated summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_number in range(doc.page_count):
        page = doc[page_number]
        text += page.get_text()

    return text

# Streamlit app
st.title("Research Paper Summary and QA")

# Upload PDF file
pdf_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if pdf_file is not None:
    # Read the PDF file
    research_paper_text = extract_text_from_pdf(pdf_file)

    # Display the original text
    st.subheader("Original Text")
    st.text(research_paper_text)

    # Generate and display the summary
    generated_summary = generate_summary(research_paper_text)
    st.subheader("Generated Summary")
    st.text(generated_summary)

    # Question-Answering
    question = st.text_input("Ask a question:")
    if st.button("Get Answer"):
        answer = qa_pipeline(context=research_paper_text, question=question)
        st.subheader("Answer")
        st.text(answer["answer"])
