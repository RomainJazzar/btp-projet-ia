"""
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
