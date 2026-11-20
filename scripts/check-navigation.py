"""Exercise the production site's reading path in desktop and phone layouts."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from tempfile import TemporaryDirectory
from threading import Thread

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


def check(browser, origin, width, height):
    browser.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
        "width": width, "height": height, "deviceScaleFactor": 1, "mobile": width < 600,
    })
    browser.get(origin)
    browser.find_element(By.LINK_TEXT, "Chapters").click()
    assert browser.current_url.endswith("#chapters")
    assert browser.execute_script("return document.documentElement.scrollWidth <= innerWidth")
    browser.execute_script("window.scrollTo({top: 0, behavior: 'instant'})")
    browser.save_screenshot(f"screenshots/home-{width}.png")
    browser.find_element(By.LINK_TEXT, "Start reading").click()
    assert browser.find_element(By.TAG_NAME, "h1").text == "Overview"
    if width < 600:
        menu = browser.find_element(By.CSS_SELECTOR, "starlight-menu-button button")
        menu.click()
        chapter_link = WebDriverWait(browser, 5).until(lambda driver: next(
            (link for link in driver.find_elements(By.CSS_SELECTOR, 'nav a[href$="/argument/contingency/"]')
             if link.is_displayed()), False))
        chapter_link.click()
    else:
        browser.find_element(By.CSS_SELECTOR, 'main a[href*="argument/contingency"]').click()
    browser.find_element(By.PARTIAL_LINK_TEXT, "brute-fact objection").click()
    assert browser.current_url.endswith("/examination/objections/#brute-existence")
    assert browser.execute_script("return document.documentElement.scrollWidth <= innerWidth")
    browser.save_screenshot(f"screenshots/objections-{width}.png")


Path("screenshots").mkdir(exist_ok=True)
with TemporaryDirectory() as temp:
    # Serve under the identical project prefix used by GitHub Pages.
    (Path(temp) / "XtoG.github.io").symlink_to(Path("dist").resolve(), target_is_directory=True)
    handler = partial(SimpleHTTPRequestHandler, directory=temp)
    with ThreadingHTTPServer(("127.0.0.1", 0), handler) as server:
        Thread(target=server.serve_forever, daemon=True).start()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        with webdriver.Chrome(options=options) as browser:
            browser.execute_cdp_cmd("Emulation.setEmulatedMedia", {"features": [
                {"name": "prefers-reduced-motion", "value": "reduce"}
            ]})
            for width, height in [(1440, 960), (390, 844)]:
                check(browser, f"http://127.0.0.1:{server.server_port}/XtoG.github.io/", width, height)
        server.shutdown()
