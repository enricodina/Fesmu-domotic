import tkinter as tk
from tkinter import messagebox
import os

def on_click():
    messagebox.showinfo("Taskbar Widget", "Button clicked!")

# Create a root window
root = tk.Tk()
root.withdraw()  # Hide the main window

# Create a system tray icon
tray_icon = tk.PhotoImage(file="icon.png")  # Replace "icon.png" with your icon path
tray_icon_label = tk.Label(root, image=tray_icon)

# Callback function to show menu on right click
def show_menu(event):
    menu.post(event.x_root, event.y_root)

# Create a menu
menu = tk.Menu(root, tearoff=False)
menu.add_command(label="Click Me", command=on_click)
menu.add_command(label="Exit", command=root.quit)

# Bind right-click event to show menu
tray_icon_label.bind("<Button-3>", show_menu)

# Start the event loop
root.mainloop()
