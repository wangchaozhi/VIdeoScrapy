from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.firefox.launch(headless=False)  # 使用无头模式请设置为True
    context = browser.new_context()

    # 监听请求事件
    def handle_request(request):
        if request.resource_type == "xhr":
            print(f"XHR Request made to: {request.url}")
            print(f"Request Headers: {request.headers}")
            print(f"Request Body: {request.post_data}")

    # 监听到请求就调用 handle_request 函数
    context.on('request', handle_request)

    page = context.new_page()
    page.goto('https://cn.pornhub.com/view_video.php?viewkey=ph621c374fc0eb2')  # 替换为你想要测试的网站
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
    page.wait_for_timeout(5000)  # 等待5000毫秒


    input("Press Enter to exit...")  # 让浏览器保持打开状态直到用户决定退出

    context.close()
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
