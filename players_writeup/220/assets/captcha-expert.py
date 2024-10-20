CAPTCHA_HOME_URL = "https://prob05.geekgame.pku.edu.cn/?token=It's MyToken!!!!!"

from playwright.sync_api import sync_playwright
from time import sleep
with sync_playwright() as p:
    browser = p.firefox.launch_persistent_context("./firefox-data", headless=False, bypass_csp=True)
    # override closed shadow DOM
    # https://github.com/microsoft/playwright/issues/23047
    browser.add_init_script("""
                            const originalAttachShadow = Element.prototype.attachShadow;
                            Element.prototype.attachShadow = function attachShadow(options) {
                                const root = originalAttachShadow.call(this, {...options, mode: 'open'});
                                return root;
                            };
                            """)
    page = browser.new_page()
    page.goto(CAPTCHA_HOME_URL)
    page.get_by_role("link", name="Expert 难度").click()
    page.wait_for_load_state("load")
    page.get_by_placeholder("输入验证码").click()
    page.evaluate("""
                var code = "";
                for (var span of document.querySelector("#root").shadowRoot.querySelectorAll(".chunk")) {
                    var lst = [];
                    // add attribs from ::before and ::after
                    for (var i of ["before", "after"]) {
                        var style = window.getComputedStyle(span, "::" + i)["content"].split(" ");
                        for (var j of style) {
                            lst.push(j.slice(5, -1));
                        }
                    }
                    for (var i of lst) {
                        code += span.attributes[i].nodeValue;
                    }
                }
                """)
    CODE = page.evaluate("code")
    page.get_by_placeholder("输入验证码").fill(CODE)
    sleep(99999)
