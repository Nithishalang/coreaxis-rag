# CoreAxis Knowledge Base

This directory contains the synthetic enterprise policy documents used as the knowledge base for the **CoreAxis AI Assistant**, an enterprise-style Retrieval-Augmented Generation (RAG) system.

## About the Data

CoreAxis is a **fictional organization** created specifically for this project. The documents in this directory were generated for development and demonstration purposes to simulate realistic enterprise knowledge sources.

The knowledge base contains policy documents covering different organizational domains, such as:

* Employee and organizational policies
* Human Resources
* Information Technology
* Finance
* Other internal company guidelines

These documents are designed to provide realistic context for testing and demonstrating the system's document ingestion, retrieval, routing, reranking, and grounded response generation capabilities.

## How the Documents Are Used

The documents in this directory serve as the source knowledge for the RAG pipeline:

1. PDF documents are loaded and processed.
2. Text is extracted and divided into smaller chunks.
3. The chunks are prepared for retrieval.
4. Dense semantic retrieval and BM25 lexical retrieval are used to find relevant information.
5. Reciprocal Rank Fusion (RRF) combines retrieval results.
6. A cross-encoder reranker selects the most relevant context.
7. The retrieved context is provided to the LLM for grounded response generation.

## Data Privacy and Disclaimer

All documents in this directory are **synthetic and fictional**. They were created specifically for this project and do not represent the policies, procedures, or internal documents of any real organization.

No real company confidential information, employee data, customer data, or proprietary organizational documents are intended to be included in this dataset.

The documents are provided solely for **educational, development, testing, and demonstration purposes**.

## Reproducibility

The raw PDF documents are included in this repository so that the document processing and RAG pipeline can be reproduced using the same source knowledge base.

Any processed or serialized data generated from these documents, such as document chunks or embeddings, may be generated locally using the project's data processing and ingestion pipeline.
