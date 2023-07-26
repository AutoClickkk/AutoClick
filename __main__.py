import time
import tkinter as tk
import pyautogui
import threading

class MouseClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoClick")
        self.root.geometry("300x600")
        
        self.click_interval = tk.DoubleVar(value=1.0)
        self.click_positions = []
        self.click_interval_minutes = tk.IntVar(value=1)
        
        self.is_clicking = False
        self.is_detecting = False

        self.create_widgets()
    
    def create_widgets(self):
        
        footer_label = tk.Label(self.root, text="HongHao,Chung @2023/7/26")
        footer_label.grid(row=13, column=0, columnspan=2, padx=5, pady=5)
        footer_label = tk.Label(self.root, text="https://github.com/chris911024")
        footer_label.grid(row=15, column=0, columnspan=2, padx=5, pady=5)
        # 座標輸入
        x_label = tk.Label(self.root, text="X座標:")
        x_label.grid(row=0, column=0, padx=5, pady=5)
        self.x_entry = tk.Entry(self.root)
        self.x_entry.grid(row=0, column=1, padx=5, pady=5)
        
        y_label = tk.Label(self.root, text="Y座標:")
        y_label.grid(row=1, column=0, padx=5, pady=5)
        self.y_entry = tk.Entry(self.root)
        self.y_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # 新增位置
        add_position_button = tk.Button(self.root, text="新增位置", command=self.add_position)
        add_position_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)
        
        # 步驟列表
        steps_label = tk.Label(self.root, text="步驟列表:")
        steps_label.grid(row=3, column=0, padx=5, pady=5, columnspan=2)
        self.steps_listbox = tk.Listbox(self.root, height=5)
        self.steps_listbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        
        # 刪除
        remove_step_button = tk.Button(self.root, text="刪除步驟", command=self.remove_selected_step)
        remove_step_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)
        
        # 時間間隔
        interval_label = tk.Label(self.root, text="執行間隔 (秒):")
        interval_label.grid(row=6, column=0, padx=5, pady=5)
        self.interval_entry = tk.Entry(self.root, textvariable=self.click_interval)
        self.interval_entry.grid(row=6, column=1, padx=5, pady=5)

        # 間隔
        interval_minutes_label = tk.Label(self.root, text="間隔分鐘數:")
        interval_minutes_label.grid(row=7, column=0, padx=5, pady=5)
        self.interval_minutes_entry = tk.Entry(self.root, textvariable=self.click_interval_minutes)
        self.interval_minutes_entry.grid(row=7, column=1, padx=5, pady=5)
        
        # 開始
        start_button = tk.Button(self.root, text="開始點擊", command=self.start_clicking)
        start_button.grid(row=8, column=0, columnspan=2, padx=5, pady=10)
        
        # 停止
        stop_button = tk.Button(self.root, text="停止點擊", command=self.stop_clicking)
        stop_button.grid(row=9, column=0, columnspan=2, padx=5, pady=5)

        # 滑鼠座標显示Label
        self.mouse_position_label = tk.Label(self.root, text="滑鼠座標: ")
        self.mouse_position_label.grid(row=10, column=0, columnspan=2, padx=5, pady=5)

        # 开始实时滑鼠座標检测按钮
        detect_button = tk.Button(self.root, text="開始偵測", command=self.toggle_detection)
        detect_button.grid(row=11, column=0, columnspan=2, padx=5, pady=5)

    def toggle_detection(self):
        if self.is_detecting:
            self.stop_detection()
        else:
            self.start_detection()

    def start_detection(self):
        self.is_detecting = True
        self.mouse_position_thread = threading.Thread(target=self.update_mouse_position)
        self.mouse_position_thread.start()
        self.mouse_position_label.config(text="滑鼠座標: ")
    
    def stop_detection(self):
        self.is_detecting = False
        self.mouse_position_thread.join()

    def add_position(self):
        x = self.x_entry.get()
        y = self.y_entry.get()
        if x and y:
            self.click_positions.append((x, y))
            step_text = f"步驟{len(self.click_positions)}: X={x}, Y={y}"
            self.steps_listbox.insert(tk.END, step_text)
    
    def remove_selected_step(self):
        selected_idx = self.steps_listbox.curselection()
        if selected_idx:
            idx = selected_idx[0]
            self.steps_listbox.delete(idx)
            self.click_positions.pop(idx)
    
    def start_clicking(self):
        self.is_clicking = True
        self.click_thread = threading.Thread(target=self.click_thread_func)
        self.click_thread.start()
    
    def stop_clicking(self):
        self.is_clicking = False
        self.click_thread.join()
    
    def update_mouse_position(self):
        try:
            while self.is_detecting:
                x, y = pyautogui.position()
                self.mouse_position_label.config(text=f"滑鼠座標: X座標={x}, Y座標={y}")
                self.root.update()
        except KeyboardInterrupt:
            pass

    def click_thread_func(self):
        try:
            interval = self.click_interval.get()
            interval_minutes = self.click_interval_minutes.get() * 60
            while self.is_clicking:
                for x, y in self.click_positions:
                    pyautogui.click(x=int(x), y=int(y))
                    self.root.update()
                    time.sleep(interval)
                time.sleep(interval_minutes)
        except pyautogui.FailSafeException:
            print("已停止點擊：移動滑鼠到螢幕左上角可停止點擊")
        finally:
            self.is_clicking = False

if __name__ == "__main__":
    root = tk.Tk()
    app = MouseClickerApp(root)
    root.mainloop()
