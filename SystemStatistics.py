from Classes import * # Imports custom classes from the Classes.py file in the project's root folder
import tkinter as tk # Library used to create the GUI and its widgets

if __name__ == "__main__":
    root = tk.Tk()
    application = MainWindow(root)
    root.mainloop()