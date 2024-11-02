import cv2
import numpy as np
import pyautogui
import time
import os
import psutil
import pygetwindow as gw
import pytesseract

# 设置 Tesseract 的路径
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # 替换为你的实际路径

# 游戏进程的名称
game_process_name = "StarRail.exe"
button_image = "images/img.png"  # 按钮图像文件路径

def activate_game_window():
    """激活游戏窗口"""
    try:
        game_window = gw.getWindowsWithTitle("崩坏：星穹铁道")[0]
        if game_window:
            game_window.activate()
            time.sleep(1)
    except IndexError:
        print("未找到游戏窗口，请确保游戏正在运行。")

def screenshot():
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    return screenshot

def find_energy_bar(screenshot_image, template_image_path):
    template = cv2.imread(template_image_path, cv2.IMREAD_UNCHANGED)
    if template is None:
        print(f"无法打开或读取文件: {template_image_path}")
        return None

    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    screenshot_gray = cv2.cvtColor(screenshot_image, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(result >= threshold)

    if loc[0].size > 0:
        y, x = loc[0][0], loc[1][0]
        return (x, y, x + template.shape[1], y + template.shape[0])
    return None

def find_button(image_path, screenshot):
    button_image = cv2.imread(image_path)
    if button_image is None:
        print(f"无法打开或读取文件: {image_path}")
        return None

    result = cv2.matchTemplate(screenshot, button_image, cv2.TM_CCOEFF_NORMED)
    threshold = 0.7
    loc = np.where(result >= threshold)

    if loc[0].size > 0:
        for pt in zip(*loc[::-1]):
            center_x = pt[0] + button_image.shape[1] // 2
            center_y = pt[1] + button_image.shape[0] // 2
            return (center_x, center_y)
    return None

def click_button(button_location):
    if button_location is not None:
        pyautogui.moveTo(button_location)
        time.sleep(0.1)
        pyautogui.click(button_location)
        print("已点击按钮。")
    else:
        print("未找到按钮。")

def extract_energy_number_from_region(screenshot_image, energy_bar_region):
    # 裁剪出能量条区域
    x1, y1, x2, y2 = energy_bar_region
    energy_region = screenshot_image[y1:y2, x1:x2]

    # 使用 OCR 提取文字
    gray_image = cv2.cvtColor(energy_region, cv2.COLOR_BGR2GRAY)
    _, bin_image = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    config = "--psm 7"  # 假设数据是单行文本
    text = pytesseract.image_to_string(bin_image, config=config, lang='eng')

    # 提取第一个数字，可根据你截图条右翼标的格式进行更细化的字符串处理
    try:
        energy_number = int(''.join(filter(str.isdigit, text.split('/')[0])))
        return energy_number
    except (ValueError, IndexError):
        print("无法解析体力数值。")
        return None

def main():
    if not os.path.exists(button_image):
        return f"图像文件不存在: {button_image}"

    activate_game_window()
    energy_template_image = "images/O.png"
    results = []

    while True:
        screenshot_image = screenshot()
        energy_bar_region = find_energy_bar(screenshot_image, energy_template_image)
        if energy_bar_region is None:
            break

        energy_number = extract_energy_number_from_region(screenshot_image, energy_bar_region)
        if energy_number is not None:
            results.append(energy_number)
            if energy_number < 60:
                return f"体力不足,剩余{energy_number},停止点击。"

        button_location = find_button(button_image, screenshot_image)
        if button_location is None:
            break

        click_button(button_location)
        time.sleep(1.0)

    return results

if __name__ == "__main__":
    main()
