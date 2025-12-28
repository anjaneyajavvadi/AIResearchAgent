import os
import json
import arxiv
import fitz
import time
import uuid
import urllib.error
from tqdm import tqdm
from sentence_transformers import SentenceTransformer
from rank_bm25 import BM25Okapi
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance

TARGET_PAPER_COUNT=120
RESULTS_PER_TOPIC=20

DATA_DIR = "data"
PDF_DIR = os.path.join(DATA_DIR, "pdfs")
META_DIR = os.path.join(DATA_DIR, "metadata")

COLLECTION_NAME = "arxiv_ai_research_papers"
EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

TOPICS = {
    "computer_vision": "computer vision",
    "nlp": "natural language processing",
    "deep_learning": "deep learning",
    "transformers": "transformer models",
    "diffusion": "diffusion models",
    "reinforcement_learning": "reinforcement learning"
}

os.makedirs(PDF_DIR, exist_ok=True)
os.makedirs(META_DIR, exist_ok=True)

embedder = SentenceTransformer(EMBED_MODEL)

qdrant = QdrantClient(path='./qdrant_data')

if COLLECTION_NAME not in [c.name for c in qdrant.get_collections().collections]:
    qdrant.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=embedder.get_sentence_embedding_dimension(),
            distance=Distance.COSINE
        )
    )

def extract_text(pdf_path: str) -> str:
    try:
        doc = fitz.open(pdf_path)
        return "\n".join(page.get_text() for page in doc)
    except Exception:
        return ""

def safe_download(paper, pdf_path, retries=3):
    for attempt in range(retries):
        try:
            paper.download_pdf(filename=pdf_path)
            return True
        except (urllib.error.HTTPError, urllib.error.URLError) as e:
            time.sleep(2)
        except Exception:
            return False
    return False

points = []
bm25_corpus = []
bm25_ids = []
seen_ids = set()

successful_papers = 0

for topic, query in TOPICS.items():
    if successful_papers >= TARGET_PAPER_COUNT:
        break

    search = arxiv.Search(
        query=query,
        max_results=RESULTS_PER_TOPIC,
        sort_by=arxiv.SortCriterion.Relevance
    )

    for paper in tqdm(search.results(), desc=f"Ingesting {topic}"):
        if successful_papers >= TARGET_PAPER_COUNT:
            break

        arxiv_id = paper.get_short_id()
        if arxiv_id in seen_ids:
            continue

        seen_ids.add(arxiv_id)

        pdf_path = os.path.join(PDF_DIR, f"{arxiv_id}.pdf")
        meta_path = os.path.join(META_DIR, f"{arxiv_id}.json")

    
        downloaded = safe_download(paper, pdf_path)
        if not downloaded:
            continue

    
        metadata = {
            "arxiv_id": arxiv_id,
            "title": paper.title,
            "authors": [a.name for a in paper.authors],
            "summary": paper.summary,
            "published": paper.published.isoformat(),
            "updated": paper.updated.isoformat(),
            "categories": paper.categories,
            "topic": topic,
            "pdf_path": pdf_path,
            "arxiv_url": paper.entry_id
        }

        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)

    
        text = extract_text(pdf_path)
        if len(text.strip()) < 500:
            continue 

    
        embedding = embedder.encode(text, normalize_embeddings=True)

        tokens = text.lower().split()
        bm25_corpus.append(tokens)
        bm25_ids.append(arxiv_id)

        point_id = uuid.uuid5(
            uuid.NAMESPACE_URL,
            f"https://arxiv.org/abs/{arxiv_id}"
        )

        points.append(
            PointStruct(
                id=str(point_id), 
                vector=embedding.tolist(),
                payload=metadata 
            )
        )


        successful_papers += 1

qdrant.upsert(
    collection_name=COLLECTION_NAME,
    points=points
)

with open(os.path.join(DATA_DIR, "bm25.json"), "w") as f:
    json.dump({"ids": bm25_ids, "corpus": bm25_corpus}, f)

print(f"SUCCESS: Downloaded and indexed {successful_papers} papers.")
