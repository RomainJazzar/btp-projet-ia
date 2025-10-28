"""
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
