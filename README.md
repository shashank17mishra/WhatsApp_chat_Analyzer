# 📊 WhatsApp Chat Analyzer

> Transform your WhatsApp chats into powerful insights with interactive visualizations, sentiment analysis, and downloadable reports.

---
### Demo : https://whatsappchatanalyzer-byshashank.streamlit.app/
---

## 🚀 Overview

WhatsApp Chat Analyzer is a data-driven dashboard built using **Python** and **Streamlit** that converts raw WhatsApp chat exports into meaningful analytics.

Upload your chat `.txt` file and explore:

- 📈 Activity patterns
- 😊 Sentiment trends
- 🔥 Heatmaps & animated graphs
- ☁️ WordCloud & emoji insights
- 📄 Downloadable PDF reports

---

## ✨ Features

### 📊 Core Analytics
- Total Messages
- Total Words
- Media Shared
- Links Shared
- Most Active User

### 📅 Time-Based Analysis
- Daily Timeline
- Monthly Timeline
- Most Active Day of the Week
- Most Active Month
- Activity Heatmap (Day vs Hour)
- Animated Time Slider (Monthly progression)

### 😊 Sentiment Analysis
- Positive / Negative / Neutral classification
- Sentiment distribution charts
- User-level sentiment comparison

### 🔥 Text Insights
- Most Common Words (Stopwords removed)
- WordCloud Visualization
- Emoji Analysis

### 🎨 UI Features
- Dark Mode Toggle
- Interactive Plotly Charts
- Clean & Responsive Layout

### 📄 Export
- Download Complete PDF Report

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|----------|
| Streamlit | Web App Framework |
| Pandas | Data Processing |
| NumPy | Data Handling |
| Plotly | Interactive Visualizations |
| Matplotlib | WordCloud Rendering |
| TextBlob | Sentiment Analysis |
| URLEXTRACT | Link Extraction |
| Emoji | Emoji Processing |
| ReportLab | PDF Report Generation |

---

## 📂 Project Structure

```
WhatsApp-Chat-Analyzer/
│
├── app.py              # Main Streamlit application
├── helper.py           # Data processing & analysis functions
├── requirements.txt    # Project dependencies
├── README.md           # Project documentation
└── sample_chat.txt     # Sample WhatsApp chat file
```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
https://github.com/shashank17mishra/WhatsApp_chat_Analyzer.git
```
### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate   # Windows
```
### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 4️⃣ Run the App
```bash
streamlit run app.py
```
## 📌 How to Use

1. Open **WhatsApp**
2. Export chat (**Without Media**)
3. Upload the `.txt` file in the app
4. Select a user or view overall analysis
5. Explore insights & download the report

---

## 🧠 Learning Outcomes

- Data Cleaning & Regex Parsing  
- DateTime Feature Engineering  
- Interactive Dashboard Development  
- Sentiment Analysis Implementation  
- Deployment Optimization  
- Production-ready Dependency Management  

---

## 🌍 Deployment

This app can be deployed easily on:

- **Streamlit Cloud**
- **Render**
- **Railway**

---

## 📈 Future Improvements

- AI-based Chat Summary  
- NLP Keyword Extraction  
- Chat Trend Prediction  
- Multi-language Sentiment Support  
- Database Integration  

---

## 👨‍💻 Author

**Shashank Mishra**  
B.Tech – Data Science  
Passionate about turning data into impactful insights 🚀
