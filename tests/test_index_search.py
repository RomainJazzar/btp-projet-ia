"""
Tests pour index.py (SQLite FTS5)
"""
import pytest
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core import index

def test_init_db(temp_dir):
    """Test création DB + tables."""
    db_path = f"{temp_dir}/test.db"
    index.init(db_path)
    
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Vérifier tables
    tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    table_names = [t[0] for t in tables]
    
    assert "documents" in table_names
    assert "pages" in table_names
    assert "pages_fts" in table_names
    
    conn.close()

def test_search_empty(temp_dir):
    """Test recherche sur DB vide."""
    db_path = f"{temp_dir}/test.db"
    index.init(db_path)
    
    results = index.search("facture", db_path)
    assert results == []

def test_add_and_search_mock(temp_dir):
    """Test ajout doc mock + recherche."""
    db_path = f"{temp_dir}/test.db"
    index.init(db_path)
    
    # Insérer manuellement un doc de test
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    cur.execute("""
        INSERT INTO documents (file_name, file_path, doc_type, indexed_at)
        VALUES (?, ?, ?, datetime('now'))
    """, ("facture_test.pdf", "/tmp/facture.pdf", "FACTURE"))
    doc_id = cur.lastrowid
    
    cur.execute("""
        INSERT INTO pages (document_id, page_num, content)
        VALUES (?, ?, ?)
    """, (doc_id, 1, "Facture n° F2024-001 du 15/03/2024. Montant total : 1500 EUR TTC."))
    
    conn.commit()
    conn.close()
    
    # Rechercher
    results = index.search("facture montant", db_path)
    
    assert len(results) > 0
    assert "facture_test.pdf" in results[0]["file_name"]
    assert "1500 EUR" in results[0]["snippet"]
