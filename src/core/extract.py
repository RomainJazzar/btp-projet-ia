"""
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
        r'\b(\d{2})/(\d{2})/(\d{4})\b',  # 15/03/2024
        r'\b(\d{4})-(\d{2})-(\d{2})\b'   # 2024-03-15
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
    amount_match = re.search(r'\b(\d+[,.]?\d*)\s*(€|EUR|euros?)\b', text, re.IGNORECASE)
    if amount_match:
        meta["amount"] = amount_match.group(1).replace(',', '.')
    
    # Numéro de document (Facture n°, Devis n°, N°, etc.)
    num_match = re.search(r'(?:facture|devis|contrat|n°|num(?:ero)?)[:\s]*([A-Z0-9-]+)', text, re.IGNORECASE)
    if num_match:
        meta["doc_number"] = num_match.group(1).upper()
    
    # Entité (simple heuristique : ligne après "Entreprise", "Société", "Fournisseur")
    entity_match = re.search(r'(?:entreprise|société|fournisseur|client)[:\s]*([A-ZÀ-ÖØ-öø-ÿ][A-Za-zÀ-ÖØ-öø-ÿ\s&-]{2,50})', text, re.IGNORECASE)
    if entity_match:
        meta["entity"] = entity_match.group(1).strip()
    
    return meta
