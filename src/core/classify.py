"""
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
