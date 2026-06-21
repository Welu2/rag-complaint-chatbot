# RAG Complaint Chatbot

## Project Overview

This project builds a Retrieval-Augmented Generation (RAG) system for consumer financial complaints. The system processes complaint narratives, converts them into vector embeddings, stores them in a FAISS vector database, and enables semantic retrieval for downstream chatbot applications.

---

## Project Structure

```text
rag-complaint-chatbot/

├── data/
│   ├── raw/
│   └── processed/
│
├── vector_store/
│
├── notebooks/
│
├── src/
│
├── tests/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Task 1: Data Exploration and Preprocessing

## Dataset Summary

Original dataset:

* Records: 9,609,797
* Features: 18

After preprocessing:

* Records: 335,412

Selected product categories:

1. Checking or savings account
2. Money transfer, virtual currency, or money service
3. Credit card
4. Payday loan, title loan, or personal loan

## Preprocessing Steps

* Loaded CFPB complaint dataset
* Performed exploratory data analysis
* Examined missing values
* Analyzed complaint narrative lengths
* Removed records without narratives
* Removed low-information records
* Filtered dataset to selected complaint categories
* Generated visualization reports

## Output

Processed dataset:

```text
data/processed/filtered_complaints.csv
```

---

# Task 2: Text Chunking, Embedding, and Vector Store Indexing

## Sampling Strategy

A stratified sample of 12,000 complaints was created from the cleaned dataset.

Stratification was performed using the Product category to preserve the original class distribution and avoid over-representation of larger categories.

## Chunking Strategy

Long complaint narratives were divided into smaller chunks using LangChain's RecursiveCharacterTextSplitter.

Configuration:

* chunk_size = 500
* chunk_overlap = 100

This configuration preserves semantic context while improving retrieval quality.

## Embedding Model

Model used:

```text
sentence-transformers/all-MiniLM-L6-v2
```

Reasons for selection:

* Fast inference
* Low memory usage
* Strong semantic search performance
* Widely adopted for RAG systems

## Vector Store

FAISS was used as the vector database.

Stored metadata for each chunk:

* Complaint ID
* Product Category
* Chunk ID

## Results

* Sample size: 12,000 complaints
* Total indexed chunks: 39,609
* Embedding dimension: 384
* Vector store backend: FAISS

## Generated Files

```text
vector_store/
├── complaints.index
├── metadata.pkl
```

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Run Task 1

```bash
python src/data_preprocessing.py
```

---

## Run Task 2

```bash
python src/build_vector_store.py
```

---

## Future Work

* Retrieval pipeline
* RAG integration
* LLM response generation
* Streamlit/Gradio chatbot interface
* Evaluation and benchmarking
