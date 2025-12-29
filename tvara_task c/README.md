## Embedding-based Similarity Search Demo

This repository contains a minimal example of **embedding-based semantic search** over the contents of a PDF file, using a Sentence Transformers model from Hugging Face.

The main script is `embedding_similarity.py`, which:

- **Loads** a pre-trained embedding model (`intfloat/e5-small-v2`)
- **Extracts text** from a PDF (`sample.pdf`)
- **Generates embeddings** for each sentence/line in the PDF
- **Runs a similarity search** for a given natural-language query
- **Prints the top‑k most relevant sentences** with similarity scores

---

## 1. Requirements

- **Python**: 3.8+ (recommended 3.10 or 3.11)
- **OS**: Works on Windows, macOS, and Linux (example commands below use generic shell syntax)

Python dependencies:

- `sentence-transformers`
- `scikit-learn` (for `cosine_similarity`)
- `pypdf`

You can install them from `pip` as shown below.

---

## 2. Setup

### 2.1. Create and activate a virtual environment (recommended)

```bash
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

### 2.2. Install dependencies

```bash
pip install --upgrade pip
pip install sentence-transformers scikit-learn pypdf
```

If you prefer, you can also create a `requirements.txt` with these packages and run:

```bash
pip install -r requirements.txt
```

---

## 3. Preparing the PDF

Place a PDF named `sample.pdf` in the **same directory** as `embedding_similarity.py`.

- The script will:
  - Open `sample.pdf`
  - Extract text from each page using `pypdf.PdfReader`
  - Split it into **non-empty lines** (treated as “sentences” or passages)

If there is no text (e.g., the PDF is only scanned images), `pypdf` may not extract anything and the script will raise an error indicating that no text was found.

You can change the file name by editing the `PDF_PATH` constant in `main()` inside `embedding_similarity.py`.

---

## 4. Running the script

From the directory containing `embedding_similarity.py` and `sample.pdf`:

```bash
python embedding_similarity.py
```

On the first run, Hugging Face will download the `intfloat/e5-small-v2` model; this may take a minute depending on your connection.

The script will:

1. **Load the model** and print a confirmation message.
2. **Read the PDF** and print how many sentences/lines were extracted.
3. **Print all loaded sentences** with their indices.
4. **Generate embeddings** for each sentence.
5. **Run a semantic search** using the default query defined in `QUERY` (currently `"How do we find related documents?"`).
6. **Display the top‑k results** (default `TOP_K = 3`) with similarity scores.

You can change the query and the number of results by editing `QUERY` and `TOP_K` in `main()`.

---

## 5. Approach and Architecture

### 5.1. Model loading

Function: `load_embedding_model`

- Uses `SentenceTransformer` to load the Hugging Face model `intfloat/e5-small-v2`.
- Prints status messages and exits cleanly if loading fails.

This model follows the **E5 format**, which expects:

- `"passage: ..."` prefix for **documents**
- `"query: ..."` prefix for **queries**

---

### 5.2. PDF text extraction

Function: `load_pdf_sentences`

- Uses `PdfReader(pdf_path)` from `pypdf`.
- Iterates over all pages, concatenating `page.extract_text()`.
- Splits on newline (`"\n"`) and strips whitespace.
- Filters out empty lines and returns a list of clean sentences/lines.
- Handles:
  - Missing file (`FileNotFoundError`)
  - Empty/invalid text (raises a `ValueError`, printed as an error and exits).

---

### 5.3. Embedding sentences

Function: `embed_sentences`

- Takes:
  - The loaded `SentenceTransformer` model
  - A list of text sentences/lines from the PDF
- Prepends each sentence with `"passage: "` to match the E5 model’s expected input format.
- Calls `model.encode(..., normalize_embeddings=True, show_progress_bar=True)`:
  - **`normalize_embeddings=True`** L2-normalizes vectors, making cosine similarity equivalent to dot product.
  - `show_progress_bar=True` gives a visual indication when embedding many sentences.

Returns a matrix/array where each row is the embedding for a sentence.

---

### 5.4. Similarity search

Function: `search_similar_sentences`

- Inputs:
  - Model instance
  - Query string
  - List of sentences
  - Pre-computed sentence embeddings
  - `top_k` (how many results to return)

Steps:

1. **Query embedding**  
   - Uses `model.encode("query: " + query, normalize_embeddings=True)` to produce a single query vector.

2. **Cosine similarity**  
   - Uses `sklearn.metrics.pairwise.cosine_similarity` between the query embedding and sentence embeddings.
   - Produces a similarity score for each sentence.

3. **Ranking**  
   - Zips sentences with scores: `(sentence, score)`.
   - Sorts them in descending order of similarity.
   - Returns the top `top_k` results.

---

### 5.5. Displaying results

Function: `display_results`

- Prints a nicely formatted output:
  - The query string
  - A numbered list of the top results
  - Each item shows:
    - Rank
    - Similarity score (4 decimal places)
    - Sentence text

This gives a quick, human-readable view of which sentences in the PDF are most relevant to the query.

---

## 6. Customization Ideas

- **Change the model**  
  - In `main()`, replace `"intfloat/e5-small-v2"` with another `sentence-transformers` model name.
  - Make sure to respect any special input formatting (e.g., prefixes) required by that model.

- **Different query input**  
  - Hard-code multiple queries and loop over them.
  - Or, read a query from user input:
    ```python
    QUERY = input("Enter your search query: ")
    ```

- **Top‑k results**  
  - Adjust `TOP_K` in `main()` to return more/fewer results.

- **Chunking strategy**  
  - Instead of splitting on newline, you can:
    - Split by sentence using `nltk` or `spacy`.
    - Merge multiple lines into bigger chunks for more context.

---

## 7. Summary

This project is a small, self-contained example of **semantic search over PDF content** using modern **sentence embeddings**. It demonstrates how to:

- Load and use a Hugging Face Sentence Transformer model
- Extract text from PDFs
- Build embeddings for document passages
- Compute cosine similarity and rank results

You can use this as a starting point for building richer retrieval or RAG-style systems on top of your own documents.


