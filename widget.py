import tkinter as tk
from tkinter import ttk
from wdt import WDTTab

# Create the main window
root = tk.Tk()
root.geometry("800x600")
root.title("Main Application")

# Create a Tab Control
tab_control = ttk.Notebook(root)

# Create the "WDT" tab
wdt_tab = WDTTab(tab_control)
tab_control.add(wdt_tab, text="WDT")

# Add more tabs if needed
sensor_tab = ttk.Frame(tab_control)
tab_control.add(sensor_tab, text="Sensors")

# Add more tabs if needed
output_tab = ttk.Frame(tab_control)
tab_control.add(output_tab, text="Output")

# Add tabs to the Tab Control
tab_control.pack(expand=1, fill="both")

# Run the application
root.mainloop()
