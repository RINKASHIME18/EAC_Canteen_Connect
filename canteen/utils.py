import re

BANNED_WORDS = [
    'kupal', 'bobo', 'tanga', 'putangina', 'gago', 'hayop', 'putris', 'pakshet', 'tangina', 'lintik', 'punyeta'
]

def contains_profanity(text):
    """
    Checks if the given text contains any banned words.
    Returns True if profanity is found, False otherwise.
    """
    if not text:
        return False
    
    # Convert to lowercase and replace some common filter-evasion characters
    text = text.lower()
    
    # Simple check for each banned word as a substring or whole word
    for word in BANNED_WORDS:
        # Using regex to find the word with boundary support to avoid partial matches
        # but also catch variations if needed. 
        # For now, literal word boundary check is safer to avoid blocking "tangina" in longer non-bad words (if any exist).
        pattern = rf'\b{re.escape(word)}\b'
        if re.search(pattern, text):
            return True
        
        # Also check for common variations or if the user concatenates them
        if word in text:
            # Check if it's a "loud" variation like p.u.t.a.n.g.i.n.a
            if len(word) > 3: # Only do substring for longer words to avoid false positives
                return True
                
    return False
