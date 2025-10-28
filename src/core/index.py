"""
Indexation plein texte avec SQLite FTS5.
"""
import sqlite3
from datetime import datetime
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
from io import StringIO

DB_SCHEMA = """
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name TEXT NOT NULL,
    file_path TEXT NOT NULL,
    doc_type TEXT,
    entity TEXT,
    doc_date TEXT,
    indexed_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS pages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    document_id INTEGER NOT NULL,
    page_num INTEGER NOT NULL,
    content TEXT NOT NULL,
    FOREIGN KEY (document_id) REFERENCES documents(id)
);

CREATE VIRTUAL TABLE IF NOT EXISTS pages_fts USING fts5(
    content,
    content_rowid=id
);

CREATE TRIGGER IF NOT EXISTS pages_ai AFTER INSERT ON pages BEGIN
    INSERT INTO pages_fts(rowid, content) VALUES (new.id, new.content);
END;

CREATE TRIGGER IF NOT EXISTS pages_ad AFTER DELETE ON pages BEGIN
    DELETE FROM pages_fts WHERE rowid = old.id;
END;

CREATE TRIGGER IF NOT EXISTS pages_au AFTER UPDATE ON pages BEGIN
    UPDATE pages_fts SET content = new.content WHERE rowid = old.id;
END;
"""

def init(db_path: str) -> None:
    """
    Initialise la base SQLite + FTS5.
    """
    conn = sqlite3.connect(db_path)
    conn.executescript(DB_SCHEMA)
    conn.commit()
    conn.close()

def add_document(pdf_path: str, metadata: dict, db_path: str = "data/index.db") -> dict:
    """
    Indexe un document PDF.
    
    Args:
        pdf_path: Chemin du PDF
        metadata: dict avec doc_type, entity, doc_date
        db_path: Chemin DB SQLite
        
    Returns:
        dict avec id, file_name, pages_indexed
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Insérer document
    file_name = pdf_path.split('/')[-1].split('\\')[-1]
    cur.execute("""
        INSERT INTO documents (file_name, file_path, doc_type, entity, doc_date, indexed_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        file_name,
        pdf_path,
        metadata.get("doc_type"),
        metadata.get("entity"),
        metadata.get("doc_date"),
        datetime.now().isoformat()
    ))
    doc_id = cur.lastrowid
    
    # Extraire texte par page
    pages = _extract_text_per_page(pdf_path)
    for page_num, content in enumerate(pages, start=1):
        cur.execute("""
            INSERT INTO pages (document_id, page_num, content)
            VALUES (?, ?, ?)
        """, (doc_id, page_num, content))
    
    conn.commit()
    conn.close()
    
    return {
        "id": doc_id,
        "file_name": file_name,
        "pages_indexed": len(pages)
    }

def search(query: str, db_path: str = "data/index.db", limit: int = 10) -> list:
    """
    Recherche plein texte FTS5.
    
    Args:
        query: Requête utilisateur
        db_path: Chemin DB
        limit: Nombre de résultats max
        
    Returns:
        Liste de dict avec file_name, page_num, snippet, doc_type, entity, doc_date
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    
    results = cur.execute("""
        SELECT 
            d.file_name,
            d.doc_type,
            d.entity,
            d.doc_date,
            p.page_num,
            snippet(pages_fts, 0, '<mark>', '</mark>', '...', 32) as snippet
        FROM pages_fts
        JOIN pages p ON pages_fts.rowid = p.id
        JOIN documents d ON p.document_id = d.id
        WHERE pages_fts MATCH ?
        ORDER BY rank
        LIMIT ?
    """, (query, limit)).fetchall()
    
    conn.close()
    
    return [dict(row) for row in results]

def _extract_text_per_page(pdf_path: str) -> list:
    """
    Extrait texte par page avec pdfminer.six.
    
    Returns:
        Liste de strings (une par page)
    """
    pages = []
    try:
        output = StringIO()
        with open(pdf_path, 'rb') as fp:
            extract_text_to_fp(fp, output, laparams=LAParams())
        
        # Heuristique simple : split sur form feed ou taille
        full_text = output.getvalue()
        
        # Fallback : une seule page si pas de séparation claire
        if '\f' in full_text:
            pages = full_text.split('\f')
        else:
            # Découper par blocs de ~2000 chars (approximatif)
            chunk_size = 2000
            pages = [full_text[i:i+chunk_size] for i in range(0, len(full_text), chunk_size)]
        
        return [p.strip() for p in pages if p.strip()]
    except Exception as e:
        return [f"Erreur extraction: {str(e)}"]
