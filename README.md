# 🤖 Resume Screening App

An AI-powered web application that automates the process of screening resumes using Natural Language Processing (NLP) and Machine Learning. Built with Streamlit, this tool helps HR professionals and recruiters efficiently classify resumes into predefined job roles.

---

## 🚀 Features

- 📄 Upload resumes in `.pdf` or `.txt` format
- 🧹 Clean and preprocess resume text using NLP
- 🔍 Automatically classify resumes into job categories (e.g., Python Developer, Data Scientist)
- 📊 View predicted job role with confidence
- ☁️ Generate word cloud of resume content
- 📈 Visualize model accuracy and training performance

---

## 🛠️ Tech Stack

| Layer       | Tools/Libraries                         |
|-------------|-----------------------------------------|
| Frontend    | [Streamlit](https://streamlit.io/)      |
| Backend     | [Python](https://www.python.org/)       |
| ML/NLP      | `scikit-learn`, `TfidfVectorizer`, `KNeighborsClassifier`, `re` |
| Visualization | `matplotlib`, `wordcloud`             |
| File Parsing | `pdfminer.six`, `PyPDF2`               |

---

## 📁 Project Structure


Resume-Screening-App/
│
├── app.py                   # Main Streamlit frontend
├── train_model.py           # Script to train the ML model
|
│── clf.pkl                  # Trained classifier (KNN)
│── tfidf.pkl                # TF-IDF vectorizer
├── data/
│   └── resumes.csv          # Sample resume dataset
├── utils/
│   └── resume_parser.py     # Custom resume text cleaning and extraction
├── requirements.txt         # Required Python dependencies
└── README.md                # Project documentation



## 📦 Installation
# 🧰 Prerequisites
Python 3.7+

pip (Python package manager)

🔧 Setup Instructions
bash
Copy
Edit
# Step 1: Clone the repository
git clone https://github.com/TerminatorSS24/Resume-Screening-App.git
cd Resume-Screening-App

# Step 2: (Optional) Create a virtual environment
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Step 3: Install dependencies
pip install -r requirements.txt

# Step 4: Run the Streamlit app
streamlit run app.py
🧪 Model Training
If you want to retrain the model with your own data:

bash
Copy
Edit
# Run the training script
python train_model.py
Make sure your dataset is in the format:

csv
Copy
Edit
Resume,Category
"Experienced in Python and Django...", "Python Developer"
...
After training, it will generate:

model/clf.pkl — The trained KNN model

model/tfidf.pkl — The TF-IDF vectorizer

🧾 Sample Output
Input: A resume mentioning skills like Python, Pandas, TensorFlow, Deep Learning

Predicted Role: Data Scientist

Display: Cleaned text preview, word cloud, and predicted label

📄 Sample Dataset
A dataset named resumes.csv is used for training. Example format:

csv
Copy
Edit
Resume,Category
"Skilled in HTML, CSS, JavaScript and React", "Web Developer"
"Worked on SQL, Tableau, PowerBI, Excel", "Data Analyst"
...
