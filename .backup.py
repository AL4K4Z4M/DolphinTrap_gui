import tkinter as tk
from gui import setup_gui
from file_operations import load_last_inputs

def main():
    root = tk.Tk()
    root.title("Evil Portal Generator (EPG)")
    root.geometry("600x800")

    last_inputs = load_last_inputs()
    setup_gui(root, last_inputs)

    root.mainloop()

if __name__ == "__main__":
    main()