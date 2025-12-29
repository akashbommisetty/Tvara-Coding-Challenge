"""
Embedding-based Similarity Search using Sentence Transformers

This script demonstrates:
1. Loading a pre-trained embedding model from Hugging Face
2. Extracting text from a PDF document
3. Generating embeddings for document sentences
4. Performing similarity search using cosine similarity

Model: intfloat/e5-small-v2 (via sentence-transformers)
"""

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from pypdf import PdfReader
import sys
from typing import List, Tuple


def load_embedding_model(model_name: str = "intfloat/e5-small-v2") -> SentenceTransformer:
    """
    Load and return a SentenceTransformer model from Hugging Face.
    
    Args:
        model_name: Name of the model to load (default: intfloat/e5-small-v2)
    
    Returns:
        Loaded SentenceTransformer model
    """
    print(f"Loading embedding model: {model_name}...")
    try:
        model = SentenceTransformer(model_name)
        print("✓ Model loaded successfully!\n")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        sys.exit(1)


def load_pdf_sentences(pdf_path: str) -> List[str]:
    """
    Extract text from a PDF file and split into sentences/lines.
    
    Args:
        pdf_path: Path to the PDF file
    
    Returns:
        List of cleaned sentences extracted from the PDF
    
    Raises:
        FileNotFoundError: If the PDF file doesn't exist
        Exception: If PDF reading fails
    """
    try:
        print(f"Reading PDF: {pdf_path}...")
        reader = PdfReader(pdf_path)
        text = ""

        for page in reader.pages:
            text += page.extract_text() + "\n"

        # Split into clean sentences/lines
        sentences = [line.strip() for line in text.split("\n") if line.strip()]
        
        if not sentences:
            raise ValueError("No text found in PDF. The PDF might be empty or contain only images.")
        
        print(f"✓ Extracted {len(sentences)} sentences from PDF\n")
        return sentences
    
    except FileNotFoundError:
        print(f"Error: PDF file '{pdf_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading PDF: {e}")
        sys.exit(1)


def embed_sentences(model: SentenceTransformer, sentences: List[str]) -> List:
    """
    Generate embeddings for a list of sentences using the E5 model format.
    
    Note: E5 models require "passage:" prefix for document sentences.
    
    Args:
        model: SentenceTransformer model instance
        sentences: List of sentences to embed
    
    Returns:
        Array of sentence embeddings
    """
    print("Generating embeddings for sentences...")
    # E5 models expect "passage:" prefix for documents
    passages = [f"passage: {s}" for s in sentences]
    embeddings = model.encode(passages, normalize_embeddings=True, show_progress_bar=True)
    print("✓ Embeddings generated successfully!\n")
    return embeddings


def search_similar_sentences(
    model: SentenceTransformer,
    query: str,
    sentences: List[str],
    sentence_embeddings: List,
    top_k: int = 3
) -> List[Tuple[str, float]]:
    """
    Perform similarity search: find the most relevant sentences for a query.
    
    Args:
        model: SentenceTransformer model instance
        query: Query string to search for
        sentences: List of candidate sentences
        sentence_embeddings: Pre-computed embeddings for the sentences
        top_k: Number of top results to return (default: 3)
    
    Returns:
        List of tuples (sentence, similarity_score) sorted by relevance
    """
    print(f"Searching for: '{query}'...")
    
    # E5 models expect "query:" prefix for queries
    query_embedding = model.encode(
        f"query: {query}",
        normalize_embeddings=True
    )
    
    # Compute cosine similarity
    scores = cosine_similarity([query_embedding], sentence_embeddings)[0]
    
    # Sort results by similarity score (descending)
    ranked_results = sorted(
        zip(sentences, scores),
        key=lambda x: x[1],
        reverse=True
    )
    
    print(f"✓ Found {len(ranked_results)} results\n")
    return ranked_results[:top_k]


def display_results(query: str, results: List[Tuple[str, float]]):
    """
    Display search results in a formatted way.
    
    Args:
        query: The search query
        results: List of (sentence, score) tuples
    """
    print("=" * 80)
    print(f"QUERY: {query}")
    print("=" * 80)
    print(f"\nTop {len(results)} most relevant sentences:\n")
    
    for idx, (sentence, score) in enumerate(results, 1):
        print(f"{idx}. [Similarity: {score:.4f}]")
        print(f"   {sentence}\n")


def main():
    """Main function to run the embedding similarity search pipeline."""
    # Configuration
    PDF_PATH = "sample.pdf"
    QUERY = "How do we find related documents?"
    TOP_K = 3
    
    # Step 1: Load embedding model
    model = load_embedding_model("intfloat/e5-small-v2")
    
    # Step 2: Extract sentences from PDF
    sentences = load_pdf_sentences(PDF_PATH)
    
    # Display loaded sentences
    print("Loaded sentences from PDF:")
    print("-" * 80)
    for i, s in enumerate(sentences, 1):
        print(f"{i}. {s}")
    print("-" * 80)
    print()
    
    # Step 3: Generate embeddings
    sentence_embeddings = embed_sentences(model, sentences)
    
    # Step 4: Perform similarity search
    results = search_similar_sentences(
        model, 
        QUERY, 
        sentences, 
        sentence_embeddings, 
        top_k=TOP_K
    )
    
    # Step 5: Display results
    display_results(QUERY, results)


if __name__ == "__main__":
    main()
