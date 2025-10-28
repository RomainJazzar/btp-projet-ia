"""
Script to create all project files for DOCin-Lite.
Run this after creating the directory structure with setup.bat
"""
import os

FILES = {
    "tools/gen.py": '''#!/usr/bin/env python3
"""
Mini-CLI IA (Anthropic) pour générer du code ou des prompts.
Usage: python tools/gen.py "votre demande"
"""
import sys
import os
from anthropic import Anthropic

def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/gen.py \\"votre demande\\"")
        sys.exit(1)
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Erreur: ANTHROPIC_API_KEY non définie")
        sys.exit(1)
    
    client = Anthropic(api_key=api_key)
    prompt = " ".join(sys.argv[1:])
    
    print(f"🤖 Requête: {prompt}\\n")
    
    message = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )
    
    print(message.content[0].text)

if __name__ == "__main__":
    main()
''',

    "src/core/extract.py": '''"""
Extraction de métadonnées depuis le texte PDF (regex FR basiques).
"""
import re
from datetime import datetime

def parse(text: str) -> dict:
    """
    Extrait métadonnées du texte PDF (date, montant, numéro, entité).
    
    Args:
        text: Texte complet du PDF
        
    Returns:
        dict avec clés: date, amount, doc_number, entity (None si non trouvés)
    """
    meta = {
        "date": None,
        "amount": None,
        "doc_number": None,
        "entity": None
    }
    
    # Date FR (JJ/MM/AAAA ou AAAA-MM-JJ)
    date_patterns = [
        r'\\b(\\d{2})/(\\d{2})/(\\d{4})\\b',  # 15/03/2024
        r'\\b(\\d{4})-(\\d{2})-(\\d{2})\\b'   # 2024-03-15
    ]
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            if '/' in pattern:
                day, month, year = match.groups()
                meta["date"] = f"{year}-{month}-{day}"
            else:
                meta["date"] = match.group(0)
            break
    
    # Montant (EUR, €, euros)
    amount_match = re.search(r'\\b(\\d+[,.]?\\d*)\\s*(€|EUR|euros?)\\b', text, re.IGNORECASE)
    if amount_match:
        meta["amount"] = amount_match.group(1).replace(',', '.')
    
    # Numéro de document (Facture n°, Devis n°, N°, etc.)
    num_match = re.search(r'(?:facture|devis|contrat|n°|num(?:ero)?)[:\\s]*([A-Z0-9-]+)', text, re.IGNORECASE)
    if num_match:
        meta["doc_number"] = num_match.group(1).upper()
    
    # Entité (simple heuristique : ligne après "Entreprise", "Société", "Fournisseur")
    entity_match = re.search(r'(?:entreprise|société|fournisseur|client)[:\\s]*([A-ZÀ-ÖØ-öø-ÿ][A-Za-zÀ-ÖØ-öø-ÿ\\s&-]{2,50})', text, re.IGNORECASE)
    if entity_match:
        meta["entity"] = entity_match.group(1).strip()
    
    return meta
''',

    "src/core/rename_rule.py": '''"""
Règle de renommage : YYYY-MM-DD_TYPE_ENTITE_NUM.pdf
"""
import re
import unicodedata

def format_name(meta: dict, basename: str) -> str:
    """
    Génère nom de fichier selon convention : YYYY-MM-DD_TYPE_ENTITE_NUM.pdf
    
    Args:
        meta: dict avec clés date, doc_type, entity, doc_number
        basename: nom original du fichier (pour extension)
        
    Returns:
        Nom formaté
        
    Raises:
        ValueError: si date ou doc_type manquants
    """
    if not meta.get("date"):
        raise ValueError("date manquante dans meta")
    if not meta.get("doc_type"):
        raise ValueError("doc_type manquant dans meta")
    
    date = meta["date"]
    doc_type = _slugify(meta["doc_type"])
    entity = _slugify(meta.get("entity", ""))
    doc_number = _slugify(meta.get("doc_number", ""))
    
    # Extension
    ext = ".pdf"
    if "." in basename:
        ext = "." + basename.rsplit(".", 1)[1]
    
    # Assemblage
    parts = [date, doc_type]
    if entity:
        parts.append(entity)
    if doc_number:
        parts.append(doc_number)
    
    return "_".join(parts) + ext

def _slugify(text: str) -> str:
    """
    Convertit texte en slug sûr : majuscules, underscores, pas d'accents.
    """
    if not text:
        return ""
    
    # Normaliser unicode et retirer accents
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    # Majuscules, remplacer espaces/tirets par underscore
    text = text.upper()
    text = re.sub(r'[^\\w]+', '_', text)
    text = re.sub(r'_+', '_', text)
    text = text.strip('_')
    
    return text
''',

    "src/core/classify.py": '''"""
Classification simple par mots-clés.
"""

def from_text(text: str) -> str:
    """
    Classifie type de document par mots-clés.
    
    Args:
        text: Contenu textuel du document
        
    Returns:
        Type: FACTURE, DEVIS, RIB, CONTRAT, ou UNKNOWN
    """
    text_lower = text.lower()
    
    keywords = {
        "FACTURE": ["facture", "invoice", "montant total", "ttc"],
        "DEVIS": ["devis", "quote", "estimation"],
        "RIB": ["rib", "iban", "bic", "relevé d'identité bancaire"],
        "CONTRAT": ["contrat", "contract", "accord", "convention"]
    }
    
    scores = {}
    for doc_type, words in keywords.items():
        score = sum(text_lower.count(word) for word in words)
        if score > 0:
            scores[doc_type] = score
    
    if not scores:
        return "UNKNOWN"
    
    return max(scores, key=scores.get)
''',

    "src/core/index.py": '''"""
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
    file_name = pdf_path.split('/')[-1].split('\\\\')[-1]
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
        if '\\f' in full_text:
            pages = full_text.split('\\f')
        else:
            # Découper par blocs de ~2000 chars (approximatif)
            chunk_size = 2000
            pages = [full_text[i:i+chunk_size] for i in range(0, len(full_text), chunk_size)]
        
        return [p.strip() for p in pages if p.strip()]
    except Exception as e:
        return [f"Erreur extraction: {str(e)}"]
''',

    "src/core/qa_template.py": '''"""
Q/R light avec snippets et citations.
"""

def answer(question: str, hits: list) -> dict:
    """
    Génère réponse simple à partir des snippets de recherche.
    
    Args:
        question: Question utilisateur
        hits: Résultats de index.search()
        
    Returns:
        dict avec answer, sources
    """
    if not hits:
        return {
            "answer": "Aucun document trouvé pour répondre à cette question.",
            "sources": []
        }
    
    # Assembler 2-3 premiers snippets
    snippets = []
    sources = []
    for i, hit in enumerate(hits[:3], start=1):
        snippet = hit.get("snippet", "")
        file_name = hit.get("file_name", "?")
        page_num = hit.get("page_num", "?")
        
        snippets.append(snippet)
        sources.append(f"{file_name}#page{page_num}")
    
    # Réponse simple
    answer_text = "Voici les extraits pertinents :\\n\\n"
    for i, snip in enumerate(snippets, start=1):
        answer_text += f"{i}. {snip}\\n\\n"
    
    return {
        "answer": answer_text.strip(),
        "sources": sources
    }
''',

    "src/app_web/app.py": '''"""
Streamlit UI : Inbox + Recherche
"""
import streamlit as st
import os
import sys
from pathlib import Path

# Ajouter src au path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core import extract, rename_rule, classify, index, qa_template
from pdfminer.high_level import extract_text

# Config
DATA_INBOX = "data/inbox"
DATA_PROCESSED = "data/processed"
DB_PATH = "data/index.db"

# Init DB
if not os.path.exists(DB_PATH):
    index.init(DB_PATH)

st.set_page_config(page_title="DOCin-Lite", page_icon="📄", layout="wide")
st.title("📄 DOCin-Lite")

tab1, tab2 = st.tabs(["📥 Inbox", "🔍 Recherche"])

# TAB 1: INBOX
with tab1:
    st.header("Inbox — Traitement PDF")
    
    uploaded_file = st.file_uploader("Déposer un PDF", type=["pdf"])
    
    if uploaded_file:
        # Sauver temporairement
        temp_path = os.path.join(DATA_INBOX, uploaded_file.name)
        os.makedirs(DATA_INBOX, exist_ok=True)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())
        
        st.success(f"✅ Fichier reçu : {uploaded_file.name}")
        
        # Extraire texte
        with st.spinner("Extraction du texte..."):
            text = extract_text(temp_path)
        
        st.text_area("Texte extrait (preview)", text[:500] + "...", height=150)
        
        # Métadonnées
        with st.spinner("Extraction métadonnées..."):
            meta = extract.parse(text)
            doc_type = classify.from_text(text)
            meta["doc_type"] = doc_type
        
        st.subheader("Métadonnées détectées")
        col1, col2 = st.columns(2)
        with col1:
            meta["date"] = st.text_input("Date (YYYY-MM-DD)", meta.get("date") or "")
            meta["doc_type"] = st.text_input("Type", meta.get("doc_type") or "")
        with col2:
            meta["entity"] = st.text_input("Entité", meta.get("entity") or "")
            meta["doc_number"] = st.text_input("Numéro", meta.get("doc_number") or "")
        
        # Renommage
        if st.button("✨ Renommer & Indexer"):
            try:
                new_name = rename_rule.format_name(meta, uploaded_file.name)
                os.makedirs(DATA_PROCESSED, exist_ok=True)
                new_path = os.path.join(DATA_PROCESSED, new_name)
                
                # Déplacer
                os.rename(temp_path, new_path)
                
                # Indexer
                result = index.add_document(
                    new_path, 
                    {
                        "doc_type": meta["doc_type"],
                        "entity": meta.get("entity"),
                        "doc_date": meta.get("date")
                    },
                    DB_PATH
                )
                
                st.success(f"✅ Renommé : {new_name}")
                st.info(f"📚 Indexé : {result['pages_indexed']} pages")
                
            except ValueError as e:
                st.error(f"❌ Erreur : {e}")

# TAB 2: RECHERCHE
with tab2:
    st.header("Recherche plein texte")
    
    query = st.text_input("🔎 Requête", placeholder="facture mars 2024")
    
    if st.button("Rechercher") and query:
        with st.spinner("Recherche..."):
            results = index.search(query, DB_PATH, limit=10)
        
        st.write(f"**{len(results)} résultat(s)**")
        
        for i, hit in enumerate(results, start=1):
            with st.expander(f"{i}. {hit['file_name']} (page {hit['page_num']})"):
                st.markdown(f"**Type:** {hit.get('doc_type', 'N/A')}")
                st.markdown(f"**Entité:** {hit.get('entity', 'N/A')}")
                st.markdown(f"**Date:** {hit.get('doc_date', 'N/A')}")
                st.markdown("---")
                st.markdown(hit['snippet'], unsafe_allow_html=True)
        
        # Q/R light optionnel
        if results and st.checkbox("💬 Générer réponse synthétique"):
            qa = qa_template.answer(query, results)
            st.subheader("Réponse")
            st.write(qa["answer"])
            st.caption(f"Sources : {', '.join(qa['sources'])}")
''',

    "tests/conftest.py": '''"""
Configuration pytest.
"""
import pytest
import tempfile
import os

@pytest.fixture
def temp_dir():
    """Dossier temporaire pour tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

@pytest.fixture
def sample_meta():
    """Métadonnées d'exemple."""
    return {
        "date": "2024-03-15",
        "doc_type": "FACTURE",
        "entity": "Entreprise X",
        "doc_number": "F2024-001"
    }
''',

    "tests/test_rename_rule.py": '''"""
Tests pour rename_rule.py
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core import rename_rule

def test_format_name_complet(sample_meta):
    """Test avec métadonnées complètes."""
    result = rename_rule.format_name(sample_meta, "original.pdf")
    assert result == "2024-03-15_FACTURE_ENTREPRISEX_F2024_001.pdf"

def test_format_name_sans_entite():
    """Test sans entité."""
    meta = {
        "date": "2024-01-10",
        "doc_type": "DEVIS",
        "doc_number": "D123"
    }
    result = rename_rule.format_name(meta, "test.pdf")
    assert result == "2024-01-10_DEVIS_D123.pdf"

def test_format_name_sans_numero():
    """Test sans numéro."""
    meta = {
        "date": "2024-02-20",
        "doc_type": "RIB",
        "entity": "Société Y"
    }
    result = rename_rule.format_name(meta, "doc.pdf")
    assert result == "2024-02-20_RIB_SOCIETEY.pdf"

def test_format_name_accents():
    """Test slug avec accents."""
    meta = {
        "date": "2024-03-01",
        "doc_type": "CONTRAT",
        "entity": "Café & Thé"
    }
    result = rename_rule.format_name(meta, "file.pdf")
    assert "CAFE" in result
    assert "THE" in result

def test_format_name_date_manquante():
    """Test ValueError si date manquante."""
    meta = {"doc_type": "FACTURE"}
    with pytest.raises(ValueError, match="date manquante"):
        rename_rule.format_name(meta, "test.pdf")

def test_format_name_type_manquant():
    """Test ValueError si doc_type manquant."""
    meta = {"date": "2024-03-15"}
    with pytest.raises(ValueError, match="doc_type manquant"):
        rename_rule.format_name(meta, "test.pdf")
''',

    "tests/test_index_search.py": '''"""
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
''',

    "data/.gitkeep": "",
    "data/inbox/.gitkeep": "",
    "data/processed/.gitkeep": "",
}

print("Creating project files...")
for filepath, content in FILES.items():
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Created: {filepath}")
    except Exception as e:
        print(f"✗ Error creating {filepath}: {e}")

print("\n✅ All files created successfully!")
print("\nNext steps:")
print("1. Create virtual environment: python -m venv venv")
print("2. Activate: venv\\Scripts\\activate (Windows) or source venv/bin/activate (Linux/Mac)")
print("3. Install dependencies: pip install streamlit pdfminer.six pytest anthropic")
print("4. Run tests: pytest -q")
print("5. Launch app: streamlit run src\\app_web\\app.py")
