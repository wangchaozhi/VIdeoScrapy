from playwright.sync_api import sync_playwright
import subprocess
import os
import re


def run(playwright):
    browser = playwright.firefox.launch(headless=True)  # 使用无头模式请设置为True
    # 禁用自动播放音频
    context = browser.new_context(ignore_https_errors=True, extra_http_headers={"permissions-policy": "autoplay=()"})
    # context = browser.new_context()

    # 初始化一个列表来存储符合条件的XHR请求URL
    xhr_requests = []

    # 设置监听请求事件
    def handle_request(request):
        if request.resource_type == "xhr":
            # 打印捕获的XHR请求信息
            # print(f"XHR Request made to: {request.url}")
            # 将符合条件的请求URL添加到列表中
            xhr_requests.append(request.url)

    # 监听到请求就调用 handle_request 函数
    context.on('request', handle_request)

    page = context.new_page()
    # page.goto('https://cn.pornhub.com/view_video.php?viewkey=ph621c374fc0eb2')  # 替换为你想要测试的网站
    page.goto('https://cn.pornhub.com/view_video.php?viewkey=ph5d15e17bc4a21')
    # page.goto('https://cn.pornhub.com/view_video.php?viewkey=658bec1c60b52')  # 替换为你想要测试的网站
    # page.goto('https://cn.pornhub.com/view_video.php?viewkey=ph62abbca5c9b0a')  # 替换为你想要测试的网站
    # 等待页面加载
    page.wait_for_load_state('networkidle')

    # 定位并点击按钮
    button_xpath = '//*[@id="modalWrapMTubes"]/div/div/button'  # XPath 选择器
    page.wait_for_selector(button_xpath)  # 等待按钮出现
    page.click(button_xpath)  # 点击按钮
    page.wait_for_load_state('networkidle')
    # 构建选择器来定位播放按钮
    playback_button_selector = ".mgp_bigPlay .mgp_playIcon"

    # 等待播放按钮出现并点击
    page.wait_for_selector(playback_button_selector, state="visible")  # 确保按钮可见
    page.click(playback_button_selector)  # 点击播放按钮

    # 增加额外的等待时间，确保所有请求都已被处理
    page.wait_for_timeout(10000)  # 等待5000毫秒


    for url in xhr_requests:
        # 检查URL是否包含 'f1' 到 'f4' 且包含 'm3u8'
        if re.search(r'f[1-4]', url) and "m3u8" in url:
            print(f"找到: {url}")
            # 替换 'f1' 到 'f4' 为 'f1'
            modified_url = re.sub(r'f[1-4]', 'f1', url)
            print(f"修改后的URL: {modified_url}")
            download_video(modified_url, "output3.mp4",page)
            # delete_file("output3.mp4")
            break
        else:
            print("未找到匹配的URL或者不包含m3u8")

    # for url in xhr_requests:
    #     if "f1" in url and "m3u8" in url:
    #         print(f"找到: {url}")
    #         download_video(url, "output3.mp4")
    #         delete_file("output3.mp4")

            # print(f"URL containing 'f1' or 'm3u8': {url}")

    # input("Press Enter to exit...")  # 让浏览器保持打开状态直到用户决定退出
    context.close()
    browser.close()




def download_video(url, output_filename,page):
    # 设置 youtube-dl 的参数
    command = [
        'youtube-dl',
        # '--limit-rate', '500k',  # 限制下载速度为 500Kbps
        '--proxy', 'http://127.0.0.1:10809',  # 设置代理服务器
        '-o', output_filename,  # 指定输出文件名和路径
        '--postprocessor-args', '"-analyzeduration 15000000"',  # 传递给ffmpeg的参数
        url  # 视频的 URL
    ]

    # 执行命令
    # run = subprocess.run(command)
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # 打印标准输出和标准错误
    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)
    if "HTTP error 403 Forbidden" in result.stderr or "HTTP error 403 Forbidden" in result.stdout:
        print('发现')
        repeat_video(output_filename,page)
    # if True:
    #     print('发现')
    #     repeat_video(output_filename, page)

def repeat_video( output_filename,page):
    delete_file(output_filename)


    # 初始化一个列表来存储符合条件的XHR请求URL
    xhr_requests = []

    # 设置监听请求事件
    def handle_request(request):
        if request.resource_type == "xhr":
            # 打印捕获的XHR请求信息
            # print(f"XHR Request made to: {request.url}")
            # 将符合条件的请求URL添加到列表中
            xhr_requests.append(request.url)

    # 监听到请求就调用 handle_request 函数
    page.on('request', handle_request)

    page.reload()
    page.wait_for_load_state('networkidle')
    # 构建选择器来定位播放按钮
    playback_button_selector = ".mgp_bigPlay .mgp_playIcon"

    # 等待播放按钮出现并点击
    page.wait_for_selector(playback_button_selector, state="visible")  # 确保按钮可见
    page.click(playback_button_selector)  # 点击播放按钮
    # 增加额外的等待时间，确保所有请求都已被处理
    page.wait_for_timeout(10000)  # 等待5000毫秒

    for url in xhr_requests:
        # 检查URL是否包含 'f1' 到 'f4' 且包含 'm3u8'
        if re.search(r'f[1-4]', url) and "m3u8" in url:
            print(f"找到: {url}")
            # 替换 'f1' 到 'f4' 为 'f1'
            modified_url = re.sub(r'f[1-4]', 'f1', url)
            print(f"修改后的URL: {modified_url}")
            download_video(modified_url, "output3.mp4", page)
            # delete_file("output3.mp4")
            break
        else:
            print("未找到匹配的URL或者不包含m3u8")




def delete_file(filename):
    # 检查文件是否存在
    if os.path.exists(filename):
        # 删除文件
        os.remove(filename)
        print(f"File '{filename}' has been deleted.")
    else:
        # 文件不存在时给出提示
        print(f"File '{filename}' not found.")


with sync_playwright() as playwright:
    run(playwright)
