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
├── evaluate_rag.py
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

# Task 3: Retrieval-Augmented Generation (RAG) Pipeline & Evaluation

## Objective

Build an end-to-end RAG system that retrieves relevant complaint excerpts and generates grounded answers to user questions using a language model.

---

## RAG Pipeline Overview

The system follows this workflow:

1. **User Question Input**
2. **Embedding Generation**

   * Uses `all-MiniLM-L6-v2`
3. **Semantic Retrieval**

   * FAISS retrieves top-k similar complaint chunks (k=5)
4. **Context Construction**

   * Retrieved chunks are concatenated into a single context block
5. **Prompt Engineering**

   * Structured prompt instructs model to answer using only retrieved context
6. **Response Generation**

   * FLAN-T5 model generates final answer

---

## Retriever Implementation

* FAISS-based similarity search
* Sentence-transformer embeddings
* Metadata includes complaint text and category
* Top-k retrieval (k=5 default)

---

## Generator Model

Model used:

```text
google/flan-t5-small
```

Rationale:

* Lightweight and fast on CPU
* Suitable for instruction-based QA
* Works well for summarization-style RAG tasks

---

## Prompt Design

The prompt instructs the model to:

* Use only retrieved complaint excerpts
* Avoid hallucination
* Summarize recurring issues when applicable

Example:

```text
Answer the question using only the complaint excerpts.

Complaint Excerpts:
{context}

Question:
{question}

Answer:
```

---

## Evaluation Strategy

A qualitative evaluation was conducted using 5 representative questions covering:

* Credit card disputes
* Mortgage servicing issues
* Debt collection complaints
* Billing issues
* Loan payment concerns

Each output was evaluated based on:

* Relevance of retrieved documents
* Accuracy of generated answer
* Clarity and summarization quality

---

## Evaluation Results Summary

| Metric             | Observation                                      |
| ------------------ | ------------------------------------------------ |
| Retrieval Quality  | Strong relevance across all queries              |
| Answer Accuracy    | Generally good, sometimes overly short           |
| Hallucination Rate | Low (model mostly grounded in context)           |
| Weakness           | Limited summarization ability due to small model |

---

## Example Results

* Credit card disputes → Correctly identifies unrecognized charges
* Billing issues → Successfully identifies late reporting patterns
* Debt collection → Captures customer dissatisfaction themes

---

## Generated Files

```text
evaluate_rag.py
src/rag_pipeline.py
src/generator.py
src/retriever.py
```
# Task 4: Interactive Chat Interface

## Objective

Build a user-friendly web interface that allows users to interact with the Retrieval-Augmented Generation (RAG) system and inspect the source documents used to generate answers.

---

## Interface Framework

The chatbot interface was implemented using **Gradio** to provide a lightweight and interactive web application.

---

## Features Implemented

### Question Input

Users can enter natural language questions about consumer financial complaints through a text input field.

Example questions:

* Why are customers disputing credit card charges?
* What mortgage servicing issues are common?
* Why are customers unhappy with debt collection?
* What billing problems appear frequently?

---

### Answer Generation

The application connects directly to the RAG pipeline developed in Task 3.

Workflow:

1. User submits a question
2. Relevant complaint chunks are retrieved from FAISS
3. Retrieved context is passed to the FLAN-T5 generator
4. A grounded answer is generated and displayed

---

### Source Attribution

To improve transparency and trustworthiness, the interface displays the retrieved complaint chunks used during answer generation.

Features:

* Source documents displayed below answers
* Expandable source panels
* Easy verification of generated responses

This allows users to inspect the evidence supporting each answer.

---

### Clear Functionality

A Clear button was implemented to:

* Reset the question field
* Remove generated answers
* Clear displayed source documents

---

### Example Questions

The interface includes predefined example questions for quick testing and demonstration.

---

## User Interface Design

The Gradio interface includes:

* Responsive layout
* Modern styling
* Dedicated answer display area
* Expandable source document sections
* Clear and intuitive navigation

The design prioritizes usability for non-technical users.

---

## Application Architecture

```text
User Question
      │
      ▼
RAG Pipeline
      │
      ├── Retriever (FAISS)
      │
      ├── Context Construction
      │
      └── Generator (FLAN-T5)
      │
      ▼
Generated Answer
      │
      ▼
Answer + Source Display
```

---

## Generated Files

```text
app.py
```

---

## Running the Application

Launch the Gradio interface:

```bash
python app.py
```

After startup, Gradio provides a local URL similar to:

```text
http://127.0.0.1:7860
```

Open the URL in a web browser to interact with the chatbot.

---

## Deliverables

* Interactive Gradio application
* Answer generation interface
* Source attribution display
* Clear/reset functionality
* Screenshots included in project report

---

## Future Work

* Improve prompt engineering for better summarization
* Upgrade LLM (FLAN-T5-base or Mistral)
* Add reranking for retrieval improvement
* Deploy chatbot UI (Streamlit / Gradio)
* Add automated evaluation metrics (BLEU / ROUGE / faithfulness scoring)

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

## Run Task 3 (RAG Evaluation)

```bash
python evaluate_rag.py
```



