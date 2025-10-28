#!/usr/bin/env python3
"""
Mini-CLI IA (Anthropic) pour générer du code ou des prompts.
Usage: python tools/gen.py "votre demande"
"""
import sys
import os
from anthropic import Anthropic

def main():
    if len(sys.argv) < 2:
        print("Usage: python tools/gen.py \"votre demande\"")
        sys.exit(1)
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Erreur: ANTHROPIC_API_KEY non définie")
        sys.exit(1)
    
    client = Anthropic(api_key=api_key)
    prompt = " ".join(sys.argv[1:])
    
    print(f"🤖 Requête: {prompt}\n")
    
    message = client.messages.create(
        model="claude-3-5-haiku-20241022",
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}]
    )
    
    print(message.content[0].text)

if __name__ == "__main__":
    main()
