import hashlib
from bs4 import BeautifulSoup
from config import KEYWORDS, VERBOSE


def log(*args):
    if VERBOSE:
        print("[DETECTOR]", *args)


# ---------------- NORMALIZATION ----------------

def normalize_html(html):
    """Strip scripts/styles and extract visible text."""
    if not html:
        return ""

    soup = BeautifulSoup(html, "html.parser")

    # Remove noise
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    clean_text = soup.get_text(separator=" ", strip=True)
    return clean_text


# ---------------- HASHING ----------------

def md5_hash(data):
    if data is None:
        return ""
    if isinstance(data, str):
        data = data.encode("utf-8", errors="ignore")
    return hashlib.md5(data).hexdigest()


# ---------------- KEYWORD DIFF ----------------

def keywords_changed(old_text, new_text):
    """Return True if any important keyword changed presence."""
    old_low = (old_text or "").lower()
    new_low = (new_text or "").lower()

    for word in KEYWORDS:
        before = word in old_low
        after = word in new_low
        if before != after:
            log(f"Keyword change detected: '{word}'")
            return True

    return False


# ---------------- SIGNIFICANT CHANGE LOGIC ----------------

def diff_significant(old_html, new_html, old_text, new_text, old_img_hash, new_img_hash):
    """
    Determine if page change is meaningful enough to alert:
    - keyword presence changed
    - major text change
    - screenshot changed
    """

    old_text = old_text or ""
    new_text = new_text or ""

    html_changed = md5_hash(old_html or "") != md5_hash(new_html or "")
    text_changed = md5_hash(old_text) != md5_hash(new_text)
    image_changed = (old_img_hash or "") != (new_img_hash or "")

    log("HTML changed:", html_changed)
    log("Text changed:", text_changed)
    log("Image changed:", image_changed)

    # 1️⃣ If keywords changed → ALWAYS meaningful
    if keywords_changed(old_text, new_text):
        log("Meaningful due to keyword change.")
        return True

    # 2️⃣ General “stock/non-stock” heuristic
    stock_old = "stock" in old_text.lower()
    stock_new = "stock" in new_text.lower()
    if stock_old != stock_new:
        log("Meaningful stock-word presence change.")
        return True

    # 3️⃣ If page content OR screenshot changed significantly
    if text_changed or image_changed:
        log("Meaningful due to text/image change.")
        return True

    # 4️⃣ Pure HTML structure change (less important)
    if html_changed:
        log("HTML changed but not meaningful.")
        return False

    # No meaningful change
    log("No significant change detected.")
    return False
