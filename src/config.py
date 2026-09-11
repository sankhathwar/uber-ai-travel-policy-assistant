"""
config.py

Central configuration file for the
Uber AI Travel Policy Assistant.
"""

from pathlib import Path

# =====================================================
# PROJECT ROOT
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# =====================================================
# DATA PATHS
# =====================================================

RAW_DATA_DIR = PROJECT_ROOT / "data" / "company_policy"

PROCESSED_DATA_DIR = PROJECT_ROOT / "data" / "processed"

CHUNKS_FILE = PROCESSED_DATA_DIR / "chunks.json"

# =====================================================
# VECTOR DATABASE
# =====================================================

VECTOR_STORE_DIR = PROJECT_ROOT / "vector_store"

FAISS_INDEX_PATH = VECTOR_STORE_DIR / "faiss_index"

# =====================================================
# EMBEDDING MODEL
# =====================================================

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# =====================================================
# CHUNKING
# =====================================================

CHUNK_SIZE = 350

CHUNK_OVERLAP = 75

# =====================================================
# RETRIEVAL
# =====================================================

TOP_K_RESULTS = 3

SIMILARITY_SEARCH_TYPE = "similarity"

# =====================================================
# LLM
# =====================================================

DEFAULT_TEMPERATURE = 0.0

MAX_TOKENS = 512

import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY not found. Please add it to the .env file."
    )

LLM_MODEL = "gemini-3.6-flash"