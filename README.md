# 📊 Automatic Data Analyzer

Automatic Data Analyzer is a **Streamlit web application** that performs **complete, end-to-end data analysis in a single frame**. Just upload your CSV file, and the app automatically generates **data previews, summary statistics, visualizations, missing value analysis, and correlation heatmaps** — all on one interactive page. This makes data exploration **fast, simple, and user-friendly** without writing a single line of code.

---

## 🗂 Table of Contents
- [✨ Features](#features)
- [🛠 Technologies Used](#technologies-used)
- [⚙️ How It Works](#how-it-works)
- [💻 Installation](#installation)
- [📧 Contact](#contact)

---

## ✨ Features
- 🖥 **Single-Frame Analysis:** All insights appear on one scrollable page.  
- 👀 **Data Preview:** View the first few rows of your dataset instantly.  
- 📊 **Summary Statistics:** Automatic computation of mean, median, standard deviation, min, max, quartiles.  
- ❗ **Missing Values Detection:** Identify null or missing values in your dataset.  
- 🔗 **Correlation Analysis:** Correlation heatmaps for numeric columns.  
- 📈 **Visualizations:** Automatically generated histograms with KDE for numeric columns.  
- 🛠 **No Coding Required:** Fully interactive interface using Streamlit.  

---

## 🛠 Technologies Used
- **Python Libraries:**
  - `numpy` – numerical computations
  - `pandas` – data manipulation and analysis
  - `matplotlib` – plotting charts
  - `seaborn` – statistical visualizations
  - `streamlit` – web app interface
- **Version Control:** Git & GitHub  
- **Deployment Platform:** Streamlit Community Cloud  

---

## ⚙️ How It Works
1. 📂 Upload your CSV file via the Streamlit interface.  
2. 🐼 The app reads the dataset using **Pandas**.  
3. ⚡ Automatic analysis is performed:  
   - Data preview  
   - Summary statistics  
   - Missing values detection  
   - Correlation matrix and heatmap  
   - Histograms for all numeric columns  
4. 🖼 All results are displayed on **a single scrollable page**.  

## ✨ Contact
6392505818
---

## 💻 Installation
1. Clone the repository:
```bash
git clone https://github.com/your-username/my-streamlit-app.git
cd my-streamlit-app
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
