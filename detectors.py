import hashlib
from bs4 import BeautifulSoup
from config import KEYWORDS

def normalize_html(html):
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    clean_text = soup.get_text(separator=" ", strip=True)
    return clean_text

def md5_hash(data):
    if isinstance(data, str):
        data = data.encode()
    return hashlib.md5(data).hexdigest()

def keywords_changed(old_text, new_text):
    old_low = old_text.lower()
    new_low = new_text.lower()

    for word in KEYWORDS:
        if (word in old_low) != (word in new_low):
            return True

    return False

def diff_significant(old_html, new_html, old_text, new_text, old_img_hash, new_img_hash):
    html_changed = md5_hash(old_html) != md5_hash(new_html)
    text_changed = md5_hash(old_text) != md5_hash(new_text)
    image_changed = old_img_hash != new_img_hash

    meaningful = (
        keywords_changed(old_text, new_text)
        or "stock" in new_text.lower() != "stock" in old_text.lower()
    )

    # Strictest: require BOTH change + meaningful indicator
    if meaningful:
        return True

    # fallback: large diff in text or image
    if text_changed or image_changed:
        return True

    return False
