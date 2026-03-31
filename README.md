# HireMatch

Two-Stage Job Title Identification System for Online Job Advertisements

HireMatch is an NLP-based intelligent system that automatically identifies the job sector and the most relevant job role from unstructured online job advertisements.
The system follows a two-stage architecture inspired by recent research, enabling accurate job title identification even with small datasets.

📌 Problem Statement

Online job advertisements often contain noisy, unstructured text where job titles are ambiguous or missing. Traditional classification systems require large labeled datasets and are often domain-specific.

HireMatch addresses this challenge by:

First identifying the job sector using supervised learning

Then identifying the exact job role using semantic similarity techniques

🧠 Proposed Solution (Two-Stage Architecture)
Job Advertisement Text
        ↓
Stage-1: Sector Classification (BERT)
        ↓
Stage-2: Job Role Identification (Sentence-BERT + Cosine Similarity)
        ↓
Final Job Title

✨ Features

🔍 BERT-based Sector Classification

🧠 Semantic Job Role Identification using Sentence-BERT

🏥 Supports multiple sectors (IT, Healthcare)

📊 Handles small and imbalanced datasets

🖥️ Interactive Streamlit Web Application

🔄 Easily extensible to new sectors

🏗️ System Architecture
Stage-1: Sector Classification

Input: Job description text

Model: Fine-tuned BERT

Output: Predicted job sector
(e.g., Information Technology, Healthcare)

Stage-2: Job Role Identification

Input: Job description + predicted sector

Model: Sentence-BERT

Technique: Cosine similarity

Output: Most semantically relevant job title within the sector

🛠️ Tech Stack

Programming Language: Python

NLP Models:

BERT (Transformers)

Sentence-BERT

Libraries:

PyTorch

HuggingFace Transformers

scikit-learn

pandas, numpy

UI Framework: Streamlit

Version Control: GitHub

📂 Project Structure 
HireMatch/
│
├── datasets/
│   ├── job_ads_stage1_balanced.csv
│   ├── it_jobs.csv
│   └── healthcare_jobs.csv
│
├── models/
│   └── stage1_bert_sector_model/
│
├── src/
│   ├── stage1_sector_classifier.py
│   ├── stage2_role_identifier.py
│   └── pipeline.py
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
