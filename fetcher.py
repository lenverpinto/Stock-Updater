from playwright.sync_api import sync_playwright
import io

def fetch_page(url, element_selector=None):
    """
    Fetch webpage and return:
    - html: full page HTML
    - text: visible text
    - screenshot: bytes of cropped product area or default viewport
    Scrolls to product element to ensure proper capture on long pages.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        )
        page = context.new_page()

        try:
            page.goto(url, wait_until="domcontentloaded", timeout=90000)
            page.wait_for_timeout(2500)  # allow JS to render

            html = page.content()
            text = page.inner_text("body")

            # ---------------- DETERMINE ELEMENT TO SCREENSHOT ----------------
            screenshot = None

            # Use provided element_selector if available
            if element_selector:
                try:
                    element = page.query_selector(element_selector)
                    if element:
                        # Scroll the element into view
                        element.scroll_into_view_if_needed(timeout=5000)
                        page.wait_for_timeout(500)  # small delay to render
                        screenshot = element.screenshot()
                except:
                    pass

            # Auto-detect largest visible element if no selector or failed
            if screenshot is None:
                element = page.evaluate_handle("""
                    () => {
                        let all = Array.from(document.body.querySelectorAll("div,section,main"));
                        all = all.filter(e => e.offsetWidth > 100 && e.offsetHeight > 100);
                        all.sort((a,b) => (b.offsetWidth*b.offsetHeight) - (a.offsetWidth*a.offsetHeight));
                        return all[0] || document.body;
                    }
                """)
                box = element.bounding_box()
                if box:
                    # Scroll the element into view
                    page.evaluate(f"window.scrollTo({box['x']}, {box['y']});")
                    page.wait_for_timeout(500)
                    screenshot = page.screenshot(clip={
                        "x": box["x"],
                        "y": box["y"],
                        "width": min(box["width"], 1280),
                        "height": min(box["height"], 1280)
                    })
                else:
                    screenshot = page.screenshot(full_page=False)

        except Exception as e:
            print(f"Error fetching {url}: {e}")
            html, text, screenshot = "", "", b""

        finally:
            context.close()
            browser.close()

        return html, text, screenshot
