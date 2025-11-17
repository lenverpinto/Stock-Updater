from playwright.sync_api import sync_playwright
import io
from config import (
    PLAYWRIGHT_HEADLESS,
    PLAYWRIGHT_NAV_TIMEOUT_MS,
    POST_LOAD_WAIT_MS,
    BLOCKED_RESOURCE_TYPES,
    VERBOSE
)

def log(*args):
    if VERBOSE:
        print("[FETCHER]", *args)


def fetch_page(url, element_selector=None):
    """
    Fetch webpage and return:
    - html: full page HTML
    - text: visible text
    - screenshot: bytes of cropped product area or fallback
    """

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=PLAYWRIGHT_HEADLESS)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        )

        # Optional resource blocking to speed up loads
        if BLOCKED_RESOURCE_TYPES:
            context.route("**/*", lambda route, req: (
                route.abort() if req.resource_type in BLOCKED_RESOURCE_TYPES else route.continue_()
            ))

        page = context.new_page()

        html = ""
        text = ""
        screenshot = b""

        try:
            log("Navigating to:", url)

            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=PLAYWRIGHT_NAV_TIMEOUT_MS or 90000
            )

            page.wait_for_timeout(POST_LOAD_WAIT_MS)

            html = page.content()
            text = page.inner_text("body")

            screenshot = None

            # ---------------- Prioritized element screenshot ----------------
            if element_selector:
                try:
                    element = page.query_selector(element_selector)
                    if element:
                        log("Using provided selector:", element_selector)
                        element.scroll_into_view_if_needed(timeout=5000)
                        page.wait_for_timeout(300)
                        screenshot = element.screenshot()
                except Exception as e:
                    log("Selector screenshot failed:", e)

            # ---------------- Automatic element selection ----------------
            if screenshot is None:
                log("Auto-detecting largest visible element")

                element = page.evaluate_handle("""
                    () => {
                        let candidates = Array.from(document.body.querySelectorAll("div,section,main,article"));
                        candidates = candidates.filter(e => e.offsetWidth > 100 && e.offsetHeight > 100);
                        candidates.sort((a, b) =>
                            (b.offsetWidth * b.offsetHeight) - (a.offsetWidth * a.offsetHeight)
                        );
                        return candidates[0] || document.body;
                    }
                """)

                box = element.bounding_box()

                if box:
                    log("Auto-selected element box:", box)
                    page.evaluate(f"window.scrollTo({box['x']}, {box['y']});")
                    page.wait_for_timeout(300)

                    screenshot = page.screenshot(clip={
                        "x": box["x"],
                        "y": box["y"],
                        "width": min(box["width"], 1280),
                        "height": min(box["height"], 1280)
                    })
                else:
                    log("Fallback: full viewport screenshot")
                    screenshot = page.screenshot(full_page=False)

        except Exception as e:
            log("Error fetching page:", e)

        finally:
            context.close()
            browser.close()

        return html, text, screenshot
