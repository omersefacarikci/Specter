import re

BOT_PATTERNS = [
    r"give me stars?.+back",
    r"star.+repositories?.+back",
    r"follow.+back",
    r"f4f",
    r"s4s",
    r"star for star",
    r"follow for follow",
    r"back to your repo",
]

COMPILED = [re.compile(p, re.IGNORECASE) for p in BOT_PATTERNS]

def is_bot(user: dict) -> tuple[bool, str]:
    bio = user.get("bio") or ""
    name = user.get("name") or ""
    
    for pattern in COMPILED:
        if pattern.search(bio) or pattern.search(name):
            return True, bio.strip()[:80] if bio else "No bio"
    
    followers = user.get("followers", 0)
    following = user.get("following", 0)
    public_repos = user.get("public_repos", 0)
    
    if following > 0 and followers > 0:
        ratio = following / max(followers, 1)
        if ratio > 10 and public_repos == 0:
            return True, f"Suspicious ratio: {following} following / {followers} followers, no repos"    
    return False, ""
