# NLP_mid_proj

This project focuses on exploring two different methods — TF-IDF and GloVe — for paper abstract similarity matching and model comparison in the field of Natural Language Processing (NLP).

## Project Structure

- `TFIDF_main.py`: Main script for TF-IDF based text matching.
- `TFIDF_utils.py`: Utility functions for TF-IDF processing.
- `GLOVE_model.py`: GloVe-based similarity calculation model.
- `GLOVE_runner.py`: Runner script for the GloVe model.
- `arxivData.py`: Script for crawling papers from arXiv.
- `arxivDataPreProcess.py`: Preprocessing script for arXiv data.
- `model_comparison.py`: Script to compare TF-IDF and GloVe models.
- `requirements.txt`: Python package requirements.
- `data/`: Directory for raw and processed data.
- `glove_embeddings_results.pkl`: Saved GloVe model results.

## Installation

Install the required Python libraries:

```bash
pip install -r requirements.txt
