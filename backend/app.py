# import streamlit as st
# import pickle
# import re
# import nltk
# from PIL import Image

# nltk.download("punkt")
# nltk.download("stopwords")

# # Load model and vectorizer
# clf = pickle.load(open("clf.pkl", "rb"))
# tfidf = pickle.load(open("tfidf.pkl", "rb"))
# label_encoder = pickle.load(open("label_encoder.pkl", "rb"))

# # App Styling
# st.set_page_config(page_title="Resume Screening", layout="wide")
# st.markdown(
#     """
#     <style>
#     .main {
#         background-color: #f5f7fa;
#         padding: 20px;
#     }
#     .stButton>button {
#         color: white;
#         background: linear-gradient(to right, #667eea, #764ba2);
#         border: none;
#         border-radius: 8px;
#         padding: 10px 20px;
#     }
#     .stFileUploader {
#         background-color: #ffffff;
#         padding: 10px;
#         border-radius: 10px;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# def cleanResume(resume_text):
#     resume_text = re.sub(r"http\S+\s", " ", resume_text)
#     resume_text = re.sub(r"RT|cc", " ", resume_text)
#     resume_text = re.sub(r"#\S+\s", " ", resume_text)
#     resume_text = re.sub(r"@\S+", " ", resume_text)
#     resume_text = re.sub(r"[%s]" % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), " ", resume_text)
#     resume_text = re.sub(r"[^\x00-\x7f]", " ", resume_text)
#     resume_text = re.sub(r"\s+", " ", resume_text)
#     return resume_text


# def main():
#     st.title("📄 AI-Powered Resume Screening Tool")
#     st.markdown("Upload your resume and get a prediction for the best career category.")

#     st.markdown("---")

#     upload_file = st.file_uploader("📤 Upload your resume", type=["pdf", "docx", "txt"])

#     if upload_file is not None:
#         try:
#             resume_bytes = upload_file.read()
#             resume_text = resume_bytes.decode("utf-8")
#         except UnicodeDecodeError:
#             resume_text = resume_bytes.decode("latin-1")

#         cleaned_resume = cleanResume(resume_text)
#         input_features = tfidf.transform([cleaned_resume])
#         prediction_id = clf.predict(input_features)[0]
#         prediction_label = label_encoder.inverse_transform([prediction_id])[0]

#         st.success("✅ Resume analyzed successfully!")
#         st.write("**Predicted Category:**", f"`{prediction_label}`")

#         st.markdown("---")
#         st.subheader("📊 How it works")
#         st.markdown(
#             """
#             - The resume is cleaned using NLP techniques.
#             - It is transformed using TF-IDF vectorization.
#             - A machine learning model predicts your job category.
#             """
#         )


# if __name__ == "__main__":
#     main()

from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import re
import os
import fitz  # PyMuPDF for PDFs
import docx  # python-docx

app = Flask(__name__)
CORS(app)

# Load model components
clf = pickle.load(open("clf.pkl", "rb"))
tfidf = pickle.load(open("tfidf.pkl", "rb"))
le = pickle.load(open("label_encoder.pkl", "rb"))

def clean_resume(text):
    text = re.sub(r"http\S+\s", " ", text)
    text = re.sub(r"RT|cc", " ", text)
    text = re.sub(r"#\S+\s", " ", text)
    text = re.sub(r"@\S+", " ", text)
    text = re.sub(r"[^\x00-\x7f]", " ", text)
    text = re.sub("[%s]" % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), " ", text)
    text = re.sub(r"\s+", " ", text)
    return text

def extract_text(file_storage):
    filename = file_storage.filename
    if filename.endswith(".pdf"):
        doc = fitz.open(stream=file_storage.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    elif filename.endswith(".docx"):
        doc = docx.Document(file_storage)
        return "\n".join([para.text for para in doc.paragraphs])
    elif filename.endswith(".txt"):
        return file_storage.read().decode("utf-8")
    else:
        return ""

@app.route('/predict', methods=['POST'])
def predict():
    file = request.files.get("resume")
    if file is None:
        return jsonify({"error": "No file uploaded"}), 400

    raw_text = extract_text(file)
    cleaned = clean_resume(raw_text)
    vector = tfidf.transform([cleaned])
    pred_id = clf.predict(vector)[0]
    label = le.inverse_transform([pred_id])[0]
    return jsonify({"category": label})

if __name__ == '__main__':
    app.run(debug=True)
