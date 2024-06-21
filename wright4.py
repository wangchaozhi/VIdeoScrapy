import subprocess
import os
import re
from playwright.sync_api import sync_playwright

def download_with_vlc(stream_url, output_path):
    vlc_command = [
        "vlc", stream_url,
        "--sout", f"#file{{dst={output_path},mux=ts}}",
        "--sout-keep"
    ]
    subprocess.Popen(vlc_command)

def run(playwright):
    print("当前工作目录:", os.getcwd())  # 输出当前工作目录

    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context(ignore_https_errors=True, extra_http_headers={"permissions-policy": "autoplay=()"})
    page = context.new_page()
    page.goto('https://cn.pornhub.com/view_video.php?viewkey=ph5d15e17bc4a21')

    button_xpath = '//*[@id="modalWrapMTubes"]/div/div/button'
    page.wait_for_selector(button_xpath)
    page.click(button_xpath)
    page.wait_for_load_state('networkidle')

    playback_button_selector = ".mgp_bigPlay .mgp_playIcon"
    xhr_requests = []
    context.on('request', lambda request: xhr_requests.append(request.url) if request.resource_type == "xhr" else None)

    page.wait_for_selector(playback_button_selector, state="visible")
    page.click(playback_button_selector)
    page.wait_for_timeout(10000)

    for url in xhr_requests:
        if re.search(r'f[1-4]', url) and "m3u8" in url:
            print(f"找到: {url}")
            modified_url = re.sub(r'f[1-4]', 'f1', url)
            print(f"修改后的URL: {modified_url}")
            download_with_vlc(modified_url, "output3.ts")
            break
        else:
            print("未找到匹配的URL或者不包含m3u8")

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
