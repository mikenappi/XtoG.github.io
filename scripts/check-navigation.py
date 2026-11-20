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
    assert browser.find_element(By.TAG_NAME, "h1").text == "X → G"
    assert browser.execute_script("return document.documentElement.scrollWidth <= innerWidth")
    assert browser.title == "X → G"
    headings = browser.find_elements(By.CSS_SELECTOR, "main section > h2")
    assert [heading.text for heading in headings] == ["Supplementary argument", "I", "II", "III", "IV"]
    marks = browser.find_elements(By.CSS_SELECTOR, "main sup")
    assert [mark.get_attribute("id") for mark in marks] == [f"conclusion-{n}" for n in range(1, 8)]
    browser.save_screenshot(f"screenshots/argument-{width}.png")
    for label, route, title in [
        ("exist contingently", "terms/contingent-existence/", "Contingent existence"),
        ("cannot be brute", "objections/brute-existence/", "Brute existence"),
        ("II", "argument/necessity/", "A necessary foundation"),
    ]:
        browser.find_element(By.LINK_TEXT, label).click()
        WebDriverWait(browser, 5).until(lambda b: b.current_url == origin + route)
        assert browser.find_element(By.TAG_NAME, "h1").text == title
        assert browser.execute_script("return document.documentElement.scrollWidth <= innerWidth")
        assert not browser.find_elements(By.CSS_SELECTOR, 'nav.sidebar, starlight-menu-button, .right-sidebar')
        if route.startswith("objections/"):
            browser.save_screenshot(f"screenshots/objection-{width}.png")
        browser.find_element(By.LINK_TEXT, "Close").click()
        WebDriverWait(browser, 5).until(lambda b: b.find_element(By.TAG_NAME, "h1").text == "X → G")
        WebDriverWait(browser, 5).until(lambda b: b.switch_to.active_element.text == label)
    browser.get(origin + "objections/brute-existence/")
    browser.find_element(By.LINK_TEXT, "Close").click()
    WebDriverWait(browser, 5).until(lambda b: b.current_url == origin)


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
            for width, height, motion in [(1440, 960, "no-preference"), (390, 844, "reduce")]:
                browser.execute_cdp_cmd("Emulation.setEmulatedMedia", {"features": [
                    {"name": "prefers-reduced-motion", "value": motion}
                ]})
                check(browser, f"http://127.0.0.1:{server.server_port}/XtoG.github.io/", width, height)
        server.shutdown()
