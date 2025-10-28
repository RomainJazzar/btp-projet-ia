# DOCin-Lite

MVP 100% local de gestion documentaire : renommer → classer → indexer (SQLite FTS5) → rechercher.

## Stack
- Python 3.10+
- Streamlit (UI)
- pdfminer.six (extraction PDF texte)
- SQLite + FTS5 (indexation plein texte)
- pytest (tests)
- anthropic (mini-CLI IA optionnel)

## Installation Rapide

### Étape 1 : Créer la structure du projet
Exécutez dans l'ordre :
```cmd
setup.bat
python create_files.py
```

### Étape 2 : Environnement virtuel & dépendances

**Windows (cmd ou PowerShell)**
```cmd
python -m venv venv
venv\Scripts\activate
pip install streamlit pdfminer.six pytest anthropic
```

**Linux/Mac**
```bash
python3 -m venv venv
source venv/bin/activate
pip install streamlit pdfminer.six pytest anthropic
```

## Lancement

### Tests
```bash
pytest -q
```

### Application Streamlit
```bash
streamlit run src/app_web/app.py
```

L'app s'ouvre sur http://localhost:8501 avec 2 onglets :
- **Inbox** : upload PDF → extraction métadonnées → renommage → indexation
- **Recherche** : requête plein texte → résultats avec snippets

## Démo (60-90s)
1. Déposer un PDF facture dans `data/inbox/` ou via l'onglet Inbox
2. L'app extrait date, montant, entité, type de document
3. Renommage automatique : `2024-03-15_FACTURE_ENTREPRISEX_001.pdf`
4. Indexation plein texte (SQLite FTS5)
5. Onglet Recherche : taper "facture mars" → résultats avec extraits surbrillés
6. Optionnel : Q/R light avec citations (file#page)

## Arborescence
```
btp-projet-ia/
├── README.md
├── .gitignore
├── tools/
│   └── gen.py              # Mini-CLI Anthropic
├── prompts/
│   ├── architecture.prompt
│   ├── rename_rule.prompt
│   ├── tests_rename_rule.prompt
│   └── index_fts.prompt
├── src/
│   ├── core/
│   │   ├── extract.py      # Parse PDF → métadonnées (date, montant, entité)
│   │   ├── rename_rule.py  # Format YYYY-MM-DD_TYPE_ENTITE_NUM.pdf
│   │   ├── classify.py     # Type doc (facture/devis/rib/contrat/unknown)
│   │   ├── index.py        # SQLite FTS5 : init, add_document, search
│   │   └── qa_template.py  # Q/R light avec snippets
│   └── app_web/
│       └── app.py          # Streamlit : Inbox + Recherche
├── tests/
│   ├── conftest.py
│   ├── test_rename_rule.py
│   └── test_index_search.py
└── data/
    ├── inbox/              # Dépôt PDF à traiter
    ├── processed/          # PDF renommés
    └── .gitkeep
```

## Git (rappel)
```bash
git add .
git commit -m "feat: DOCin-Lite MVP complet"
git push origin presentation-1
```

## Backlog S2 → S3
- OCR pour PDF scannés (Tesseract)
- Classification ML (scikit-learn)
- Q/R avancée (RAG avec embeddings)
- Export CSV/Excel des résultats
- Multi-utilisateurs (auth simple)
