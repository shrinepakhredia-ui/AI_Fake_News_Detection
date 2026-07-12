<div align="center">

# 📰 AI Fake News Detection Pro

### AI-Powered Fake News Detection using Machine Learning & Trusted Source Verification

[![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-FF4B4B?logo=streamlit)](https://streamlit.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-F7931E?logo=scikitlearn)](https://scikit-learn.org/)
[![Random Forest](https://img.shields.io/badge/Model-Random_Forest-success)]()
[![TF-IDF](https://img.shields.io/badge/NLP-TF--IDF-blueviolet)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()

> Detect fake news using Machine Learning, verify trusted publishers, analyze article authenticity, and generate AI-powered trust insights.

---

### 🌐 Live Demo _(Coming Soon)_

**GitHub Repository:**  
https://github.com/shrinepakhredia-ui/AI_Fake_News_Detection_Pro

</div>

---

# 📖 Overview

AI Fake News Detection Pro is a Machine Learning-based web application that classifies news articles as **Real** or **Fake** using Natural Language Processing.

Unlike traditional fake news detectors, this application combines **Machine Learning predictions**, **Trusted Publisher Verification**, **Source Reliability Analysis**, and an **Overall Authenticity Score** to provide transparent and explainable predictions.

---

# ✨ Key Features

## 🤖 AI Fake News Detection

- Predicts whether a news article is **Real** or **Fake**
- Random Forest Classifier
- TF-IDF Feature Extraction
- Real-time prediction

---

## 🌐 URL-Based News Analysis

Paste a news URL and the system automatically:

- Extracts article content
- Reads title
- Downloads article
- Cleans text
- Predicts authenticity

---

## 🏢 Trusted Publisher Verification

Detects trusted publishers including:

- Reuters
- BBC
- The Hindu
- The Indian Express
- Hindustan Times
- NDTV
- Times of India
- AP News
- Financial Express
- MoneyControl
- Business Standard
- Livemint

---

## 📊 Source Reliability Score

Every supported publisher is assigned a credibility score.

Example:

| Publisher      | Reliability |
| -------------- | ----------- |
| Reuters        | 99%         |
| BBC            | 99%         |
| The Hindu      | 97%         |
| Indian Express | 95%         |

---

## 🧠 AI Trust Score

Trust Score is calculated using multiple factors:

- ML Confidence
- Trusted Publisher
- Source Reliability
- Article Length
- AI Confidence

---

## ✅ Overall News Authenticity

The final authenticity score combines:

- Model Confidence
- AI Trust Score
- Source Reliability

to provide a single authenticity percentage.

---

## 💡 AI Explanation Panel

Explains why the model predicted the article as Real or Fake.

Example:

✔ Trusted Publisher

✔ High ML Confidence

✔ Detailed Article

✔ Reliable Source

---

## 📈 Interactive Dashboard

The Streamlit dashboard includes:

- Confidence Meter
- Trust Score
- Source Reliability
- Authenticity Score
- Processing Time
- AI Explanation
- Top Keywords
- Prediction History

---

## 📥 Prediction History

- Stores previous predictions
- Download CSV
- View historical analysis

---

# 🧠 Machine Learning Workflow

```text
News Article
      │
      ▼
Text Cleaning
      │
      ▼
TF-IDF Vectorization
      │
      ▼
Random Forest Classifier
      │
      ▼
Prediction
      │
      ▼
Publisher Verification
      │
      ▼
Source Reliability
      │
      ▼
AI Trust Score
      │
      ▼
Overall Authenticity Score
```

---

# 🛠 Tech Stack

| Category            | Technologies   |
| ------------------- | -------------- |
| Programming         | Python         |
| Web Framework       | Streamlit      |
| Machine Learning    | Scikit-Learn   |
| NLP                 | TF-IDF         |
| Model               | Random Forest  |
| Data Processing     | Pandas, NumPy  |
| Visualization       | Plotly         |
| Model Serialization | Joblib         |
| URL Extraction      | Newspaper3k    |
| HTML Parsing        | BeautifulSoup4 |

---

# 📊 Model Performance

| Metric    |      Score |
| --------- | ---------: |
| Accuracy  | **99.83%** |
| Precision | **99.77%** |
| Recall    | **99.88%** |
| F1 Score  | **99.82%** |

---

# 📸 Screenshots

## 🏠 Home Page

<p align="center">
<img src="assets/images/home.png" width="900">
</p>

## 📰 Prediction Result

<p align="center">
<img src="assets/images/prediction-result.png"
width="900">

---

## 🌐 URL Analysis

<p align="center">
<img src="assets/images/url-extraction.png" width="900">
</p>

## 📊 Prediction Dashboard

<p align="center">
<img src="assets/images/charts.png" width="900">

## 🧠 AI Explanation

<p align="center">
<img src="assets/images/AI-explanation.png" width="900">

# 📂 Project Structure

```text
AI_Fake_News_Detection_Pro
│
├── app.py
├── config.py
├── predict.py
├── requirements.txt
│
├── models
│   ├── random_forest.pkl
│   └── tfidf_vectorizer.pkl
│
├── src
│   ├── preprocessing.py
│   ├── trainer.py
│   ├── feature_engineering.py
│   ├── ui.py
│   ├── source_checker.py
│   ├── source_score.py
│   └── url_extractor.py
│
└── README.md
```

---

# ⚙ Installation

### Clone Repository

```bash
git clone https://github.com/shrinepakhredia-ui/AI_Fake_News_Detection_Pro.git
```

### Go to Project Folder

```bash
cd AI_Fake_News_Detection_Pro
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
streamlit run app.py
```

---

# 🚀 Future Improvements

- Live News API Integration
- BERT-based Classification
- Explainable AI (XAI)
- Browser Extension
- Multi-language Support
- AI Chat Assistant for News Verification

---

# 👨‍💻 Author

**Shrine Pakhredia**

B.Tech Artificial Intelligence & Machine Learning

GitHub: https://github.com/shrinepakhredia-ui

---

<div align="center">

### ⭐ If you found this project useful, don't forget to Star the repository!

</div>
