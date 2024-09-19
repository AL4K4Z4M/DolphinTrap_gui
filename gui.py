import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import json
import os
import re
import xml.dom.minidom
from html_generator import create_html_file
from file_operations import save_last_inputs, load_last_inputs

# File to store the last inputs and window size/position
config_file = 'last_inputs.json'

def save_window_size_and_position():
    window_size_and_position = {
        "width": root.winfo_width(),
        "height": root.winfo_height(),
        "x": root.winfo_x(),
        "y": root.winfo_y()
    }
    with open(config_file, 'r') as file:
        data = json.load(file)
    data.update(window_size_and_position)
    with open(config_file, 'w') as file:
        json.dump(data, file)

def load_window_size_and_position():
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            data = json.load(file)
        width = data.get("width", 600)
        height = data.get("height", 800)
        x = data.get("x", 100)
        y = data.get("y", 100)
        # Ensure the window is within the screen bounds
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        if x + width > screen_width:
            x = screen_width - width
        if y + height > screen_height:
            y = screen_height - height
        return width, height, x, y
    return 600, 800, 100, 100

def format_svg(svg_content):
    try:
        dom = xml.dom.minidom.parseString(svg_content)
        return dom.toprettyxml()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to format SVG: {e}")
        return svg_content

def extract_colors(svg_content):
    return re.findall(r'fill:#([0-9a-fA-F]{6})', svg_content)

def create_color_thumbnail(color):
    canvas = tk.Canvas(root, width=20, height=20, bg=f'#{color}', highlightthickness=0)
    return canvas

def on_submit():
    company_name = entry_company_name.get()
    slogan = entry_slogan.get()
    svg_file = entry_svg_file.get()
    svg_width = entry_svg_width.get()
    svg_height = entry_svg_height.get()
    address = entry_address.get()
    phone_number = entry_phone_number.get()
    terms_of_service = entry_terms_of_service.get()
    privacy_statement = entry_privacy_statement.get()
    faq = entry_faq.get()
    contact_page = entry_contact_page.get()
    save_location = entry_save_location.get()
    button_color = combo_button_color.get()

    if not all([company_name, slogan, svg_file, svg_width, svg_height, address, phone_number, terms_of_service, privacy_statement, faq, contact_page, save_location, button_color]):
        messagebox.showerror("Error", "All fields are required.")
        return

    replacements = {
        "company_name": company_name,
        "slogan": slogan,
        "svg_file": svg_file,
        "svg_width": svg_width,
        "svg_height": svg_height,
        "address": address,
        "phone_number": phone_number,
        "terms_of_service": terms_of_service,
        "privacy_statement": privacy_statement,
        "faq": faq,
        "contact_page": contact_page,
        "save_location": save_location,
        "button_color": button_color
    }
    create_html_file(save_location, replacements)
    save_last_inputs(replacements)
    messagebox.showinfo("Success", f"HTML file created at {save_location}")

def select_save_location():
    output_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
    if output_path:
        entry_save_location.delete(0, tk.END)
        entry_save_location.insert(0, output_path)

def select_svg_file():
    svg_path = filedialog.askopenfilename(filetypes=[("SVG files", "*.svg")])
    if svg_path:
        entry_svg_file.delete(0, tk.END)
        entry_svg_file.insert(0, svg_path)
        with open(svg_path, 'r') as file:
            svg_content = file.read()
        formatted_svg_content = format_svg(svg_content)
        svg_preview_text.delete(1.0, tk.END)
        svg_preview_text.insert(tk.END, formatted_svg_content)
        colors = extract_colors(svg_content)
        combo_button_color['values'] = colors
        color_listbox.delete(0, tk.END)
        for color in colors:
            color_listbox.insert(tk.END, color)
            color_listbox.itemconfig(tk.END, {'bg': f'#{color}'})
        if colors:
            combo_button_color.current(0)

# Create the main window
root = tk.Tk()
root.title("Evil Portal Generator (EPG)")

# Load last inputs and window size/position
last_inputs = load_last_inputs()
width, height, x, y = load_window_size_and_position()
root.geometry(f"{width}x{height}+{x}+{y}")

# Create and place widgets using grid layout
tk.Label(root, text="Company Name:").grid(row=0, column=0, padx=10, pady=5, sticky='e')
entry_company_name = tk.Entry(root)
entry_company_name.grid(row=0, column=1, columnspan=2, padx=10, pady=5, sticky='ew')
entry_company_name.insert(0, last_inputs.get("company_name", ""))

tk.Label(root, text="Slogan:").grid(row=1, column=0, padx=10, pady=5, sticky='e')
entry_slogan = tk.Entry(root)
entry_slogan.grid(row=1, column=1, columnspan=2, padx=10, pady=5, sticky='ew')
entry_slogan.insert(0, last_inputs.get("slogan", ""))

tk.Label(root, text="SVG File:").grid(row=2, column=0, padx=10, pady=5, sticky='e')
entry_svg_file = tk.Entry(root)
entry_svg_file.grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky='ew')
entry_svg_file.insert(0, last_inputs.get("svg_file", ""))
tk.Button(root, text="Browse", command=select_svg_file).grid(row=2, column=3, padx=10, pady=5)

tk.Label(root, text="SVG Width:").grid(row=3, column=0, padx=10, pady=5, sticky='e')
entry_svg_width = tk.Entry(root)
entry_svg_width.grid(row=3, column=1, columnspan=2, padx=10, pady=5, sticky='ew')
entry_svg_width.insert(0, last_inputs.get("svg_width", ""))

tk.Label(root, text="SVG Height:").grid(row=4, column=0, padx=10, pady=5, sticky='e')
entry_svg_height = tk.Entry(root)
entry_svg_height.grid(row=4, column=1, columnspan=2, padx=10, pady=5, sticky='ew')
entry_svg_height.insert(0, last_inputs.get("svg_height", ""))

tk.Label(root, text="Address:").grid(row=5, column=0, padx=10, pady=5, sticky='e')
entry_address = tk.Entry(root)
entry_address.grid(row=5, column=1, columnspan=2, padx=10, pady=5, sticky='ew')
entry_address.insert(0, last_inputs.get("address", ""))

tk.Label(root, text="Phone Number:").grid(row=6, column=0, padx=10, pady=5, sticky='e')
entry_phone_number = tk.Entry(root)
entry_phone_number.grid(row=6, column=1, columnspan=2, padx=10, pady=5, sticky='ew')
entry_phone_number.insert(0, last_inputs.get("phone_number", ""))

tk.Label(root, text="Terms of Service:").grid(row=7, column=0, padx=10, pady=5, sticky='e')
entry_terms_of_service = tk.Entry(root)
entry_terms_of_service.grid(row=7, column=1, columnspan=2, padx=10, pady=5, sticky='ew')
entry_terms_of_service.insert(0, last_inputs.get("terms_of_service", ""))

tk.Label(root, text="Privacy Statement:").grid(row=8, column=0, padx=10, pady=5, sticky='e')
entry_privacy_statement = tk.Entry(root)
entry_privacy_statement.grid(row=8, column=1, columnspan=2, padx=10, pady=5, sticky='ew')
entry_privacy_statement.insert(0, last_inputs.get("privacy_statement", ""))

tk.Label(root, text="FAQ:").grid(row=9, column=0, padx=10, pady=5, sticky='e')
entry_faq = tk.Entry(root)
entry_faq.grid(row=9, column=1, columnspan=2, padx=10, pady=5, sticky='ew')
entry_faq.insert(0, last_inputs.get("faq", ""))

tk.Label(root, text="Contact Page:").grid(row=10, column=0, padx=10, pady=5, sticky='e')
entry_contact_page = tk.Entry(root)
entry_contact_page.grid(row=10, column=1, columnspan=2, padx=10, pady=5, sticky='ew')
entry_contact_page.insert(0, last_inputs.get("contact_page", ""))

tk.Label(root, text="Save Location:").grid(row=11, column=0, padx=10, pady=5, sticky='e')
entry_save_location = tk.Entry(root)
entry_save_location.grid(row=11, column=1, columnspan=2, padx=10, pady=5, sticky='ew')
entry_save_location.insert(0, last_inputs.get("save_location", ""))
tk.Button(root, text="Browse", command=select_save_location).grid(row=11, column=3, padx=10, pady=5)

tk.Label(root, text="Button Color:").grid(row=12, column=0, padx=10, pady=5, sticky='e')
combo_button_color = ttk.Combobox(root)
combo_button_color.grid(row=12, column=1, columnspan=2, padx=10, pady=5, sticky='ew')
combo_button_color.set(last_inputs.get("button_color", ""))

# Create a Listbox for color options with thumbnails
color_listbox = tk.Listbox(root, height=5)
color_listbox.grid(row=12, column=3, padx=10, pady=5, sticky='ew')

# Update the Create HTML File button's grid position
tk.Button(root, text="Create HTML File", command=on_submit).grid(row=13, column=0, columnspan=4, pady=20)

# Add SVG preview text widget
svg_preview_text = tk.Text(root, wrap='none', height=10)
svg_preview_text.grid(row=14, column=0, columnspan=4, padx=10, pady=10, sticky='nsew')

# Add vertical and horizontal scrollbars to the Text widget
v_scrollbar = tk.Scrollbar(root, orient='vertical', command=svg_preview_text.yview)
v_scrollbar.grid(row=14, column=4, sticky='ns')
h_scrollbar = tk.Scrollbar(root, orient='horizontal', command=svg_preview_text.xview)
h_scrollbar.grid(row=15, column=0, columnspan=4, sticky='ew')
svg_preview_text.config(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

# Configure the grid to make the Text widget and window resizable
root.grid_rowconfigure(14, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)

# Bind the save_window_size_and_position function to the window close event
root.protocol("WM_DELETE_WINDOW", lambda: [save_window_size_and_position(), root.destroy()])

# Start the main loop
root.mainloop()