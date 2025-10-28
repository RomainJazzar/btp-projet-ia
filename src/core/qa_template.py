"""
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
    answer_text = "Voici les extraits pertinents :\n\n"
    for i, snip in enumerate(snippets, start=1):
        answer_text += f"{i}. {snip}\n\n"
    
    return {
        "answer": answer_text.strip(),
        "sources": sources
    }
