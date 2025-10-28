# 📋 INDEX — Fichiers du Projet DOCin-Lite

## 🎯 Comment Démarrer

**Option 1 : Installation Automatique (RECOMMANDÉ)**
```cmd
install_all.bat
```
Ce script fait tout : crée dossiers, fichiers, venv, installe dépendances, lance tests, démarre l'app.

**Option 2 : Installation Manuelle**
```cmd
setup.bat
python create_files.py
python -m venv venv
venv\Scripts\activate
pip install streamlit pdfminer.six pytest anthropic
pytest -q
streamlit run src\app_web\app.py
```

## 📚 Documentation (lire dans cet ordre)

### 1. QUICKSTART.txt ⚡
**Lecture : 2 min**  
Installation express en 5 étapes. Parfait pour démarrer rapidement.

### 2. SUMMARY.md 📊
**Lecture : 5 min**  
Résumé exécutif du projet. Métriques, fonctionnalités, checklist.

### 3. README.md 📖
**Lecture : 5 min**  
Présentation du projet, stack technique, installation, démo, backlog.

### 4. INSTALL.md 🔧
**Lecture : 10 min**  
Guide complet d'installation + 3 features live avec prompts et patches.

### 5. ARCHITECTURE.md 🏗️
**Lecture : 15 min**  
Architecture technique détaillée : flux, DB schema, contrats modules, benchmarks.

### 6. INDEX.md 📋
**Lecture : 3 min**  
Ce fichier. Guide de navigation dans le projet.

## 🛠️ Scripts d'Installation

### install_all.bat ⭐ **RECOMMANDÉ**
Script tout-en-un Windows qui :
- Crée tous les dossiers
- Génère tous les fichiers source
- Crée l'environnement virtuel
- Installe les dépendances
- Lance les tests
- Démarre l'application

### setup.bat
Crée uniquement la structure de dossiers.

### create_files.py
Génère tous les fichiers Python source (tools, src, tests).

### setup_dirs.py
Alternative Python pour créer la structure (si setup.bat échoue).

## 📂 Structure Générée (après installation)

```
btp-projet-ia/
│
├── 📄 README.md                    # Présentation projet
├── 📄 INSTALL.md                   # Guide complet
├── 📄 ARCHITECTURE.md              # Doc technique
├── 📄 QUICKSTART.txt               # Installation express
├── 📄 SUMMARY.md                   # Résumé exécutif
├── 📄 INDEX.md                     # Ce fichier
├── 📄 .gitignore                   # Config Git
│
├── 🔧 install_all.bat              # Installation auto (recommandé)
├── 🔧 setup.bat                    # Création dossiers
├── 🔧 create_files.py              # Génération fichiers source
├── 🔧 setup_dirs.py                # Alternative création dossiers
│
├── 📁 prompts/
│   ├── MASTER_PROMPT.txt           # Prompt maître (spec complète)
│   ├── architecture.prompt         # Prompt architecture
│   ├── rename_rule.prompt          # Prompt fonction renommage
│   ├── tests_rename_rule.prompt    # Prompt tests
│   └── index_fts.prompt            # Prompt indexation FTS5
│
├── 📁 tools/
│   └── gen.py                      # Mini-CLI Anthropic
│
├── 📁 src/
│   ├── core/
│   │   ├── extract.py              # Extraction métadonnées
│   │   ├── rename_rule.py          # Renommage YYYY-MM-DD_TYPE_ENTITE_NUM
│   │   ├── classify.py             # Classification mots-clés
│   │   ├── index.py                # Indexation SQLite FTS5
│   │   └── qa_template.py          # Q/R light
│   └── app_web/
│       └── app.py                  # Interface Streamlit
│
├── 📁 tests/
│   ├── conftest.py                 # Fixtures pytest
│   ├── test_rename_rule.py         # Tests rename (6 tests)
│   └── test_index_search.py        # Tests index (3 tests)
│
└── 📁 data/
    ├── inbox/                      # Dépôt PDF à traiter
    │   └── .gitkeep
    ├── processed/                  # PDF renommés
    │   └── .gitkeep
    └── index.db                    # Base SQLite (généré au runtime)
```

## 🎓 Ordre de Lecture pour Comprendre le Projet

### Pour Développeur
1. SUMMARY.md → vue d'ensemble
2. ARCHITECTURE.md → comprendre la conception
3. src/core/\*.py → lire le code source
4. tests/\*.py → comprendre les tests

### Pour Présentation/Soutenance
1. QUICKSTART.txt → installation rapide
2. README.md → présentation générale
3. INSTALL.md → features live pour démo
4. Script démo (dans INSTALL.md)

### Pour Installation
1. QUICKSTART.txt → étapes express
2. Exécuter : `install_all.bat`
3. Lire INSTALL.md si problème

## 📊 Fichiers par Catégorie

### Documentation (6 fichiers)
- README.md
- INSTALL.md
- ARCHITECTURE.md
- QUICKSTART.txt
- SUMMARY.md
- INDEX.md

### Scripts Installation (4 fichiers)
- install_all.bat
- setup.bat
- create_files.py
- setup_dirs.py

### Configuration (1 fichier)
- .gitignore

### Prompts IA (5 fichiers)
- prompts/MASTER_PROMPT.txt
- prompts/architecture.prompt
- prompts/rename_rule.prompt
- prompts/tests_rename_rule.prompt
- prompts/index_fts.prompt

### Code Source (7 fichiers)
- tools/gen.py
- src/core/extract.py
- src/core/rename_rule.py
- src/core/classify.py
- src/core/index.py
- src/core/qa_template.py
- src/app_web/app.py

### Tests (3 fichiers)
- tests/conftest.py
- tests/test_rename_rule.py
- tests/test_index_search.py

### Data (3 dossiers + .gitkeep)
- data/inbox/.gitkeep
- data/processed/.gitkeep
- data/.gitkeep

**TOTAL : 29 fichiers créés**

## 🚀 Commandes Rapides

### Installation Complète
```cmd
install_all.bat
```

### Installation Manuelle
```cmd
setup.bat
python create_files.py
python -m venv venv
venv\Scripts\activate
pip install streamlit pdfminer.six pytest anthropic
```

### Tests
```cmd
pytest -q          # Rapide
pytest -v          # Verbeux
pytest --tb=short  # Avec traceback court
```

### Lancement Application
```cmd
streamlit run src\app_web\app.py
```

### Mini-CLI IA (optionnel)
```cmd
set ANTHROPIC_API_KEY=votre_clé
python tools\gen.py "votre demande"
```

### Git
```cmd
git add .
git commit -m "feat: DOCin-Lite MVP complet"
git push origin presentation-1
```

## 🎯 Checklist Utilisation

### Avant la soutenance
- [ ] Lire SUMMARY.md (5 min)
- [ ] Lire INSTALL.md section "Démo" (5 min)
- [ ] Pratiquer le script démo (10 min)
- [ ] Choisir 1 feature live parmi les 3
- [ ] Préparer 1 PDF de test (facture ou devis)
- [ ] Tester l'app : upload → rename → search (5 min)

### Le jour J
- [ ] Lancer l'app avant la soutenance
- [ ] Avoir le PDF de test prêt
- [ ] Avoir le code de la feature live prêt
- [ ] Timer la démo (60-90s max)

## ❓ FAQ

### Q: Quel fichier lire en premier ?
**R:** QUICKSTART.txt pour installer, puis SUMMARY.md pour comprendre.

### Q: Comment installer rapidement ?
**R:** Lancer `install_all.bat` dans le terminal.

### Q: Les tests échouent, que faire ?
**R:** Vérifier Python 3.10+ installé (`python --version`), puis relancer `install_all.bat`.

### Q: L'app Streamlit ne démarre pas ?
**R:** Vérifier venv activé (`venv\Scripts\activate`) et streamlit installé (`pip show streamlit`).

### Q: Où trouver les features live pour la démo ?
**R:** Dans INSTALL.md, section "Feature Live" (3 options avec prompts + patches).

### Q: Comment préparer la soutenance ?
**R:** Lire INSTALL.md section "Démo" + pratiquer le script oral 2-3 fois.

## 🏆 Statut du Projet

✅ **Projet livré complet selon MASTER_PROMPT.txt**  
✅ **29 fichiers générés**  
✅ **Installation automatisée**  
✅ **Tests OK (9 tests)**  
✅ **Documentation exhaustive (30+ pages)**  
✅ **Démo 60-90s préparée**  
✅ **3 features live prêtes**  

---

**Prêt à démarrer ?** → Lancer `install_all.bat` 🚀

*DOCin-Lite — Document Management Made Simple 📄✨*
