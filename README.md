# 📊 Retention Intelligence & Cohort Analytics Platform

---

# 📖 Overview

The **Retention Intelligence & Cohort Analytics Platform** is a production-ready analytics application designed to help organizations understand, measure, and improve customer retention through advanced cohort analysis, behavioral analytics, churn measurement, and predictive machine learning.

Modern digital businesses generate enormous volumes of user interaction data, but transforming those events into actionable retention insights remains a significant challenge. This platform addresses that challenge by providing a unified analytics environment that combines interactive dashboards, statistical modeling, and machine learning to reveal how users behave over time, which behaviors lead to long-term engagement, and where churn risks emerge.

Built using **Python**, **Streamlit**, **SQLAlchemy**, **SQLite**, **Pandas**, **Plotly**, and **Scikit-learn**, the platform delivers enterprise-grade analytics while maintaining a clean, modular, and scalable architecture. Every metric is traceable back to its source, enabling confident business decisions supported by transparent analytical workflows.

Whether the goal is improving onboarding, reducing churn, optimizing user engagement, or identifying the characteristics of highly retained users, the platform provides the tools required to monitor performance, detect trends, and make data-driven product decisions.

---

# 🚀 Live Application

**Live Demo**

https://retention-intelligence-platform.onrender.com

---

# 🎯 Project Objectives

The platform enables organizations to:

* Analyze user retention across multiple cohorts
* Measure churn using configurable business definitions
* Discover behaviors that predict long-term retention
* Build machine learning models for retention prediction
* Generate executive dashboards with actionable KPIs
* Export analytical reports for stakeholders
* Monitor user engagement through interactive visualizations
* Support strategic product and growth decisions with reliable analytics

---

# 🏗️ System Architecture

The application follows a modular enterprise architecture to ensure maintainability, scalability, and separation of responsibilities.

| Layer            | Technology           | Responsibility                                                  |
| ---------------- | -------------------- | --------------------------------------------------------------- |
| Presentation     | Streamlit            | Interactive dashboards and user interface                       |
| Analytics        | Pandas, NumPy, SciPy | Cohort analysis, statistical calculations, behavioral analytics |
| Machine Learning | Scikit-learn         | Retention prediction and churn modeling                         |
| Visualization    | Plotly, Altair       | Interactive charts, heatmaps, KPI dashboards                    |
| Data Access      | SQLAlchemy           | Database abstraction and ORM                                    |
| Storage          | SQLite / PostgreSQL  | User events, retention metrics, activity logs                   |
| Reporting        | OpenPyXL, FPDF       | CSV, Excel, and PDF exports                                     |
| Deployment       | Render               | Cloud hosting with automated deployment                         |

---

# ✨ Key Features

## 📈 Executive KPI Dashboard

Monitor business-critical metrics including:

* Total Users
* Active Users
* Returning Users
* Weekly Retention
* Monthly Retention
* Candidate Retention
* Company Retention
* Churn Rate
* User Lifetime Value
* Growth Rate
* Retention Score
* Customer Health Indicators

---

## 📊 Cohort Retention Analysis

Perform detailed cohort analysis with:

* Weekly Cohorts
* Monthly Cohorts
* Retention Curves
* Retention Matrix
* Cohort Heatmaps
* Survival Analysis
* Time-based Cohort Comparison
* Interactive Filtering

These visualizations help identify how retention changes across acquisition periods and user segments.

---

## 📉 Churn Analytics

Analyze user attrition through configurable churn definitions.

Features include:

* Churn Rate Calculation
* User Inactivity Analysis
* High-Risk User Detection
* Churn Trend Analysis
* User-Type Segmentation
* Win-Back Opportunity Identification
* Actionable Retention Recommendations

---

## 🧠 Behavioral Analytics

Understand which behaviors influence long-term retention.

Behavioral metrics include:

* Profile Completion
* Session Frequency
* Session Duration
* First Activity Time
* Applications Submitted
* Searches Performed
* Messages Sent
* Saved Opportunities
* Active Days
* Feature Utilization

The platform highlights statistically significant behaviors associated with retained users.

---

## 🤖 Predictive Analytics

Machine learning models estimate retention probability using historical behavioral data.

Supported models include:

* Logistic Regression
* Decision Tree
* Random Forest

Performance metrics include:

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC
* Confusion Matrix

The platform also displays feature importance rankings and retention probability for individual users.

---

## 📄 Reporting

Generate downloadable reports in multiple formats:

* CSV
* Excel
* PDF

Reports are suitable for business reviews, stakeholder presentations, and executive decision-making.

---

# 📁 Project Structure

```text
retention-intelligence-platform/

├── app.py
├── requirements.txt
├── README.md
├── Procfile
├── runtime.txt
├── setup.sh
├── .gitignore
│
├── config/
├── database/
├── analytics/
├── models/
├── dashboard/
├── utils/
├── reports/
├── data/
├── assets/
└── screenshots/
```

Each module has a dedicated responsibility, promoting maintainability and simplifying future enhancements.

---

# 📊 Dashboard Modules

The application contains dedicated analytical dashboards:

* 🏠 Overview
* 📊 Executive Dashboard
* 📈 Cohort Analysis
* 📉 Churn Analytics
* 👥 User Analytics
* 🧠 Behavioral Insights
* 🤖 Predictive Analytics
* 📄 Reports & Export

---

# 📦 Installation

## Clone Repository

```bash
git clone https://github.com/gokulakb/retention-intelligence-platform.git
cd retention-intelligence-platform
```

## Create Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Seed the Database

```bash
python -m database.seed
```

---

## Run the Application

```bash
streamlit run app.py
```

Open:

```
http://localhost:8501
```

---

# ☁️ Deployment

The project is deployment-ready for Render.

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
sh setup.sh && streamlit run app.py --server.port=$PORT --server.enableCORS=false
```

Recommended Environment Variable

```
PYTHON_VERSION=3.11.11
```

---

# 📊 Technologies Used

### Programming

* Python

### Dashboard

* Streamlit

### Database

* SQLite
* PostgreSQL (Supported)

### Data Processing

* Pandas
* NumPy

### Machine Learning

* Scikit-learn
* SciPy

### Visualization

* Plotly
* Altair

### ORM

* SQLAlchemy

### Reporting

* OpenPyXL
* FPDF

### Deployment

* Render

---

# 🔮 Future Enhancements

The platform has been designed with extensibility in mind. Future improvements include:

* PostgreSQL and MySQL production integration
* Real-time event streaming using Apache Kafka
* Automated ETL pipelines
* User segmentation powered by clustering algorithms
* Deep learning retention prediction models
* A/B testing framework
* Scheduled report generation
* Role-based authentication
* REST API integration
* Cloud-native data warehouse support

---

# 📄 License

This project is proprietary software intended for educational, research, demonstration, and internal organizational use.

---

# 🙏 Acknowledgements

This project was built using the outstanding open-source Python ecosystem.

Special thanks to the communities behind:

* Python
* Streamlit
* Pandas
* NumPy
* Plotly
* SQLAlchemy
* Scikit-learn
* SciPy
* OpenPyXL

Their contributions make modern data analytics and machine learning accessible to developers worldwide.

---
