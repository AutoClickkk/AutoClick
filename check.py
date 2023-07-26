import pyautogui

def get_mouse_position():
    try:
        while True:
            x, y = pyautogui.position()
            print(f"X座標: {x}, Y座標: {y}", end="\r")
    except KeyboardInterrupt:
        print("\n已停止顯示滑鼠座標")

if __name__ == "__main__":
    get_mouse_position()
