"""
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
