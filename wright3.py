import subprocess
import os
import re
from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.firefox.launch(headless=False)
    context = browser.new_context(ignore_https_errors=True, extra_http_headers={"permissions-policy": "autoplay=()"})
    page = context.new_page()
    page.goto('https://cn.pornhub.com/view_video.php?viewkey=ph5d15e17bc4a21')  # 替换为你的目标网站

    # 模拟用户交互
    button_xpath = '//*[@id="modalWrapMTubes"]/div/div/button'
    page.wait_for_selector(button_xpath)
    page.click(button_xpath)

    # 进行初次尝试
    attempt_download(page)

    context.close()
    browser.close()

def attempt_download(page):
    xhr_requests = []  # 初始化XHR请求列表

    # 设置监听请求事件
    def handle_request(request):
        if request.resource_type == "xhr":
            xhr_requests.append(request.url)

    # 注册请求监听器
    page.on('request', handle_request)

    # 构建选择器来定位播放按钮
    playback_button_selector = ".mgp_bigPlay .mgp_playIcon"

    # 等待播放按钮出现并点击
    page.wait_for_selector(playback_button_selector, state="visible")  # 确保按钮可见
    page.click(playback_button_selector)  # 点击播放按钮



    page.wait_for_timeout(10000)  # 等待额外的时间，确保所有请求都被捕获



    # 处理捕获的请求
    process_requests(xhr_requests, page)
    delete_file('output3.mp4')

def process_requests(xhr_requests, page):
    found = False
    for url in xhr_requests:
        if re.search(r'f[1-4]', url) and "m3u8" in url:
            print(f"找到: {url}")
            if download_video(url,page):
                found = True
                break

    if not found:
        print("未找到匹配的URL或者不包含m3u8")

def download_video(url,page):
    command = ['youtube-dl', '--proxy', 'http://127.0.0.1:10809', '-o', 'output3.mp4', url]
    process = subprocess.Popen(command, stderr=subprocess.PIPE, text=True)
    while True:
        output = process.stderr.readline()
        if output == '':
            break
        if "HTTP error 403 Forbidden" in output:
            print("检测到 403 Forbidden 错误，刷新页面并重试...")
            page.reload()  # 刷新页面
            attempt_download(page)  # 重新尝试下载
            delete_file('output3.mp4')
            return False
    return True

def delete_file(filename):
    try:
        os.remove(filename)
        print(f"文件 '{filename}' 已被删除。")
    except FileNotFoundError:
        print(f"文件 '{filename}' 未找到。")

with sync_playwright() as playwright:
    run(playwright)
