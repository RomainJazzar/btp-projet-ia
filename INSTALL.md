# DOCin-Lite — Guide d'Installation Complet

## 🚀 Installation Rapide (3 étapes)

### Étape 1 : Créer la structure
```cmd
setup.bat
```

### Étape 2 : Créer tous les fichiers
```cmd
python create_files.py
```

### Étape 3 : Installer les dépendances
```cmd
python -m venv venv
venv\Scripts\activate
pip install streamlit pdfminer.six pytest anthropic
```

## ✅ Vérification

### Lancer les tests
```cmd
pytest -q
```

### Lancer l'application
```cmd
streamlit run src\app_web\app.py
```

L'app s'ouvre sur http://localhost:8501

## 📁 Structure créée

```
btp-projet-ia/
├── README.md
├── .gitignore
├── setup.bat                   # Script Windows de setup
├── create_files.py            # Crée tous les fichiers source
├── tools/
│   └── gen.py                 # Mini-CLI Anthropic
├── prompts/
│   ├── MASTER_PROMPT.txt
│   ├── architecture.prompt
│   ├── rename_rule.prompt
│   ├── tests_rename_rule.prompt
│   └── index_fts.prompt
├── src/
│   ├── core/
│   │   ├── extract.py         # Extraction métadonnées PDF
│   │   ├── rename_rule.py     # Renommage YYYY-MM-DD_TYPE_ENTITE_NUM
│   │   ├── classify.py        # Classification par mots-clés
│   │   ├── index.py           # Indexation SQLite FTS5
│   │   └── qa_template.py     # Q/R light
│   └── app_web/
│       └── app.py             # Interface Streamlit
├── tests/
│   ├── conftest.py
│   ├── test_rename_rule.py
│   └── test_index_search.py
└── data/
    ├── inbox/                 # Dépôt PDF à traiter
    └── processed/             # PDF renommés & indexés
```

## 🎯 Utilisation

### Onglet Inbox
1. Déposer un PDF (ou placer dans `data/inbox/`)
2. Extraction automatique des métadonnées (date, type, entité, numéro)
3. Vérifier/corriger les métadonnées
4. Cliquer "Renommer & Indexer"
5. Le PDF est renommé selon la convention et indexé en base

### Onglet Recherche
1. Saisir une requête ("facture mars 2024")
2. Résultats avec snippets surlignés
3. Option : générer réponse synthétique avec citations

## 🧪 Tests

```cmd
# Tous les tests
pytest -v

# Tests rename_rule uniquement
pytest tests/test_rename_rule.py -v

# Tests index/search uniquement
pytest tests/test_index_search.py -v
```

## 🛠️ Mini-CLI IA (optionnel)

Définir la clé API :
```cmd
set ANTHROPIC_API_KEY=votre_clé_ici
```

Utiliser :
```cmd
python tools/gen.py "générer un test pour extract.py"
```

## 📊 Démo (60-90s pour soutenance)

1. **Montrer l'interface** : 2 onglets (Inbox, Recherche)
2. **Upload PDF facture** : extraction auto des métadonnées
3. **Renommage** : `2024-03-15_FACTURE_ENTREPRISEX_001.pdf`
4. **Indexation** : N pages indexées (affichage)
5. **Recherche** : requête "facture" → résultats avec snippets
6. **Q/R** : réponse synthétique avec citations (optionnel)

**Script démo** :
> "Voici DOCin-Lite, un système de gestion documentaire local. Je dépose une facture PDF. 
> L'app extrait automatiquement la date, le type de document, l'entité et le numéro. 
> Je valide et clique Renommer & Indexer. Le fichier est renommé selon notre convention 
> et son contenu est indexé en plein texte avec SQLite FTS5. Dans l'onglet Recherche, 
> je peux retrouver n'importe quel document avec des mots-clés. Les résultats affichent 
> des extraits surlignés. Option bonus : générer une réponse synthétique avec citations."

## 🔧 Feature Live (au choix)

### Option 1 : Re-indexer tous les documents
**Prompt** :
```
Ajoute un bouton "Re-indexer tout" dans l'onglet Recherche qui vide et réindexe tous 
les PDF du dossier data/processed/.
```

**Patch** (ajouter dans `src/app_web/app.py`, tab Recherche) :
```python
if st.button("🔄 Re-indexer tout"):
    import glob
    pdfs = glob.glob("data/processed/*.pdf")
    # Réinitialiser DB
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    index.init(DB_PATH)
    
    for pdf_path in pdfs:
        # Parser filename pour extraire métadonnées
        filename = os.path.basename(pdf_path)
        parts = filename.replace('.pdf', '').split('_')
        meta = {
            "doc_date": parts[0] if len(parts) > 0 else None,
            "doc_type": parts[1] if len(parts) > 1 else None,
            "entity": parts[2] if len(parts) > 2 else None,
        }
        index.add_document(pdf_path, meta, DB_PATH)
    
    st.success(f"✅ {len(pdfs)} documents ré-indexés")
```

### Option 2 : Export CSV des résultats
**Prompt** :
```
Ajoute un bouton "Export CSV" qui exporte les résultats de recherche en CSV téléchargeable.
```

**Patch** (ajouter après affichage résultats) :
```python
if results:
    import pandas as pd
    df = pd.DataFrame(results)
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Export CSV",
        data=csv,
        file_name=f"recherche_{query.replace(' ', '_')}.csv",
        mime="text/csv"
    )
```

### Option 3 : Éditer entité manuellement
**Prompt** :
```
Ajoute la possibilité d'éditer le champ entity d'un document indexé depuis l'interface.
```

**Patch** (ajouter dans tab Recherche, dans expander résultat) :
```python
new_entity = st.text_input(f"Modifier entité", hit.get('entity', ''), key=f"entity_{i}")
if st.button(f"Sauvegarder", key=f"save_{i}"):
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "UPDATE documents SET entity = ? WHERE file_name = ?",
        (new_entity, hit['file_name'])
    )
    conn.commit()
    conn.close()
    st.success("✅ Entité mise à jour")
```

## ⚠️ Limites & Risques

- **Pas d'OCR** : PDF scannés non gérés (backlog S2)
- **Classification simple** : heuristiques par mots-clés → peut classer `UNKNOWN`
- **FTS5** : performant sur petits corpus ; scaling non testé au-delà de 10k docs
- **Regex FR** : extraction métadonnées basique, peut manquer des cas edge

## 🚀 Backlog S2 → S3

- [ ] OCR pour PDF scannés (Tesseract)
- [ ] Classification ML (scikit-learn, entraînement sur corpus)
- [ ] Q/R avancée RAG (embeddings + vector search)
- [ ] Export Excel/CSV avancé
- [ ] Multi-utilisateurs (auth simple, Flask ou FastAPI)
- [ ] Interface admin (stats, monitoring indexation)

## 📝 Git

```bash
git add .
git commit -m "feat: DOCin-Lite MVP complet — Streamlit + SQLite FTS5 + tests"
git push origin presentation-1
```

## ✅ Checklist Finale

- [x] Architecture définie (flux, DB schema, modules)
- [x] Arborescence complète créée
- [x] README avec installation
- [x] .gitignore configuré
- [x] Prompts IA (architecture, rename_rule, tests, index)
- [x] tools/gen.py (mini-CLI Anthropic)
- [x] src/core/ : extract, rename_rule, classify, index, qa_template
- [x] src/app_web/app.py (Streamlit 2 onglets)
- [x] tests/ : conftest, test_rename_rule, test_index_search
- [x] data/ : inbox, processed (avec .gitkeep)
- [x] Script démo 60-90s
- [x] Feature live (3 options proposées avec prompts/patches)
- [x] Commandes Git

## 💡 Support

En cas de problème :
1. Vérifier Python 3.10+ installé : `python --version`
2. Vérifier pip à jour : `pip install --upgrade pip`
3. Vérifier dépendances : `pip list`
4. Tests : `pytest -v` pour détails
5. Logs Streamlit : visibles dans le terminal

---

**DOCin-Lite** — Document Management Made Simple 📄✨
