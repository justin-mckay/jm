import tkinter as tk
from tkinter import messagebox
from tkinter import Menu
from global_hotkeys import register_hotkey, start_checking_hotkeys, stop_checking_hotkeys
import threading
import sys
import os
import requests

class HotkeyThread(threading.Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        register_hotkey(['control', 'alt', 'j'], self.show_message)
        start_checking_hotkeys()

    def show_message(self):
        messagebox.showinfo("Hotkey Pressed", "Ctrl+Alt+J pressed")

    def stop(self):
        stop_checking_hotkeys()

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Hotkey Application")
        self.geometry("300x200")

        self.counter = 0
        self.label = tk.Label(self, text="0", font=("Arial", 24))
        self.label.pack(pady=20)

        self.button = tk.Button(self, text="Increment", command=self.increment_label)
        self.button.pack(pady=20)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def increment_label(self):
        self.counter += 1
        self.label.config(text=str(self.counter))

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.quit()
            self.destroy()

class TrayIcon:
    def __init__(self, root, hotkey_thread):
        self.root = root
        self.hotkey_thread = hotkey_thread

        self.menu = Menu(root, tearoff=0)
        self.menu.add_command(label="Show", command=self.show_window)
        self.menu.add_command(label="Exit", command=self.exit_app)

        self.tray_icon = None
        self.create_tray_icon()

    def create_tray_icon(self):
        from infi.systray import SysTrayIcon

        def show_callback(_):
            self.show_window()

        def exit_callback(_):
            self.exit_app()

        menu_options = (("Show", None, show_callback),)
        self.tray_icon = SysTrayIcon("icon.ico", "Hotkey Application", menu_options, on_quit=exit_callback)
        self.tray_icon.start()

    def show_window(self):
        self.root.deiconify()

    def exit_app(self):
        self.hotkey_thread.stop()
        self.root.quit()
        self.root.destroy()
        if self.tray_icon:
            self.tray_icon.shutdown()

if __name__ == "__main__":
    # Check for icon file
    if not os.path.exists("icon.ico"):
        with open("icon.ico", "wb") as f:
            f.write(requests.get("https://via.placeholder.com/64").content)

    root = MainWindow()

    hotkey_thread = HotkeyThread()
    hotkey_thread.start()

    tray_icon = TrayIcon(root, hotkey_thread)

    root.mainloop()

    hotkey_thread.stop()
