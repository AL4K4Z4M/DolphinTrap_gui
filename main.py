import tkinter as tk
from tkinter import filedialog, messagebox, ttk, PhotoImage
import json
import os
import re
import xml.dom.minidom
from html_generator import create_html_file
from file_operations import save_last_inputs, load_last_inputs
import ctypes
from tkinter import font as tkFont
import webbrowser

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
    links_color = entry_links_color.get() or "#0000FF"  # Default to blue
    button_color = entry_button_color.get() or "#0000FF"  # Default to blue
    #hover_color = entry_button_color.get() or "#1100FF"  # Default to a darker blue

    if not all([company_name, slogan, svg_file, svg_width, svg_height, address, phone_number, terms_of_service, privacy_statement, faq, contact_page, save_location]):
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
        "links_color": links_color,
        "button_color": button_color
        #"hover_color": hover_color
    }

    # Generate the HTML content
    html_content = create_html_file(save_location, replacements)

    # Check the size of the HTML content
    if len(html_content.encode('utf-8')) > 20480:  # 20 KB in bytes
        response = messagebox.askquestion("Warning", "This file will be incompatible with the Flipper Zero. Do you want to continue?", icon='warning')
        if response == 'no':
            return

    # Save the HTML file
    with open(save_location, 'w') as file:
        file.write(html_content)

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


# Define placeholders
placeholders = {
    "company_name": "Enter company name",
    "slogan": "Enter slogan",
    "svg_file": "Select SVG file",
    "svg_width": "Enter SVG width",
    "svg_height": "Enter SVG height",
    "address": "Enter address",
    "phone_number": "Enter phone number",
    "terms_of_service": "Enter Terms of Service URL",
    "privacy_statement": "Enter Privacy Statement URL",
    "faq": "Enter FAQ URL",
    "contact_page": "Enter Contact Page URL",
    "save_location": "Select save location",
    "links_color": "Enter links color",
    "button_color": "Enter button color"
    #"hover_color": "Enter button hover color"
}

def set_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(fg='grey')

def clear_placeholder(event, placeholder):
    if event.widget.get() == placeholder:
        event.widget.delete(0, tk.END)
        event.widget.config(fg='black')

def restore_placeholder(event, placeholder):
    if event.widget.get() == '':
        event.widget.insert(0, placeholder)
        event.widget.config(fg='grey')

def apply_placeholder(entry, placeholder):
    if not entry.get():  # Check if the entry box is empty
        set_placeholder(entry, placeholder)
    else:
        entry.config(fg='black')  # Set text color to black if entry has a value
    entry.bind("<FocusIn>", lambda event: clear_placeholder(event, placeholder))
    entry.bind("<FocusOut>", lambda event: restore_placeholder(event, placeholder))

def clear_fields():
    def clear_entry(entry, placeholder):
        entry.delete(0, tk.END)
        entry.insert(0, placeholder)
        entry.config(fg='grey')

    clear_entry(entry_company_name, placeholders["company_name"])
    clear_entry(entry_slogan, placeholders["slogan"])
    clear_entry(entry_svg_file, placeholders["svg_file"])
    clear_entry(entry_svg_width, placeholders["svg_width"])
    clear_entry(entry_svg_height, placeholders["svg_height"])
    clear_entry(entry_address, placeholders["address"])
    clear_entry(entry_phone_number, placeholders["phone_number"])
    clear_entry(entry_terms_of_service, placeholders["terms_of_service"])
    clear_entry(entry_privacy_statement, placeholders["privacy_statement"])
    clear_entry(entry_faq, placeholders["faq"])
    clear_entry(entry_contact_page, placeholders["contact_page"])
    clear_entry(entry_save_location, placeholders["save_location"])
    clear_entry(entry_links_color, placeholders["links_color"])
    clear_entry(entry_button_color, placeholders["button_color"])
    # clear_entry(entry_hover_color, placeholders["hover_color"])

def set_title_bar_color(color):
    hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
    ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 35, ctypes.byref(ctypes.c_int(2)), ctypes.sizeof(ctypes.c_int(2)))
    ctypes.windll.dwmapi.DwmSetWindowAttribute(hwnd, 19, ctypes.byref(ctypes.c_int(int(color, 16))), ctypes.sizeof(ctypes.c_int(int(color, 16))))

# Create the main window
root = tk.Tk()
root.title("DolphinTrap")
root.configure(bg='#232323')  # Set background color

# Set the title bar color
set_title_bar_color('0xe88004')

# Load last inputs and window size/position
last_inputs = load_last_inputs()
width, height, x, y = load_window_size_and_position()
root.geometry(f"{width}x{height}+{x}+{y}")

# Set minimum window size
root.minsize(1000, 700)  # Adjust the minimum width and height as needed

# Load the logo image
logo = PhotoImage(file='dolphin_logo.png').subsample(20, 20)  # Adjust the subsample factor as needed
github_logo = PhotoImage(file='LKZM_hat_flip_orange.png').subsample(5, 5)  # Adjust the subsample factor as needed

# Load custom font
custom_font = tkFont.Font(family="Karmatic Arcade", size=20)
root.option_add("*Font", custom_font)

# Define smaller font and reduced padding
font = ('Helvetica', 10)  # Smaller font size
padding = {'padx': 5, 'pady': 5}  # Reduced padding

# Configure the grid to make the Text widget and window resizable
for i in range(19):  # Adjust the range based on the number of rows
    root.grid_rowconfigure(i, weight=1)
for i in range(9):  # Adjust the range based on the number of columns
    root.grid_columnconfigure(i, weight=1)

# Create a Label widget with the logo image and place it at the top
logo_label = tk.Label(root, image=logo, bg='#232323')
logo_label.grid(row=0, column=0, columnspan=9, pady=10, sticky='nsew')

# Column 1
tk.Label(root, text="Company Name:", bg='#232323', fg='#ffffff', font=font).grid(row=2, column=0, padx=10, pady=5, sticky='e')
entry_company_name = tk.Entry(root, font=font)
entry_company_name.grid(row=2, column=1, padx=10, pady=5, sticky='ew')
entry_company_name.insert(0, last_inputs.get("company_name", ""))

tk.Label(root, text="Slogan:", bg='#232323', fg='#ffffff', font=font).grid(row=3, column=0, padx=10, pady=5, sticky='e')
entry_slogan = tk.Entry(root, font=font)
entry_slogan.grid(row=3, column=1, padx=10, pady=5, sticky='ew')
entry_slogan.insert(0, last_inputs.get("slogan", ""))

tk.Label(root, text="FAQ:", bg='#232323', fg='#ffffff', font=font).grid(row=4, column=0, padx=10, pady=5, sticky='e')
entry_faq = tk.Entry(root, font=font)
entry_faq.grid(row=4, column=1, padx=10, pady=5, sticky='ew')
entry_faq.insert(0, last_inputs.get("faq", ""))

tk.Label(root, text="Contact Page:", bg='#232323', fg='#ffffff', font=font).grid(row=5, column=0, padx=10, pady=5, sticky='e')
entry_contact_page = tk.Entry(root, font=font)
entry_contact_page.grid(row=5, column=1, padx=10, pady=5, sticky='ew')
entry_contact_page.insert(0, last_inputs.get("contact_page", ""))

# Column 2
tk.Label(root, text="Address:", bg='#232323', fg='#ffffff', font=font).grid(row=2, column=2, padx=10, pady=5, sticky='e')
entry_address = tk.Entry(root, font=font)
entry_address.grid(row=2, column=3, padx=10, pady=5, sticky='ew')
entry_address.insert(0, last_inputs.get("address", ""))

tk.Label(root, text="Phone Number:", bg='#232323', fg='#ffffff', font=font).grid(row=3, column=2, padx=10, pady=5, sticky='e')
entry_phone_number = tk.Entry(root, font=font)
entry_phone_number.grid(row=3, column=3, padx=10, pady=5, sticky='ew')
entry_phone_number.insert(0, last_inputs.get("phone_number", ""))

tk.Label(root, text="Terms of Service:", bg='#232323', fg='#ffffff', font=font).grid(row=4, column=2, padx=10, pady=5, sticky='e')
entry_terms_of_service = tk.Entry(root, font=font)
entry_terms_of_service.grid(row=4, column=3, padx=10, pady=5, sticky='ew')
entry_terms_of_service.insert(0, last_inputs.get("terms_of_service", ""))

tk.Label(root, text="Privacy Statement:", bg='#232323', fg='#ffffff', font=font).grid(row=5, column=2, padx=10, pady=5, sticky='e')
entry_privacy_statement = tk.Entry(root, font=font)
entry_privacy_statement.grid(row=5, column=3, padx=10, pady=5, sticky='ew')
entry_privacy_statement.insert(0, last_inputs.get("privacy_statement", ""))

# Column 3
tk.Label(root, text="SVG File:", bg='#232323', fg='#ffffff', font=font).grid(row=2, column=4, padx=10, pady=5, sticky='e')
entry_svg_file = tk.Entry(root, font=font)
entry_svg_file.grid(row=2, column=5, padx=10, pady=5, sticky='ew')
entry_svg_file.insert(0, last_inputs.get("svg_file", ""))
tk.Button(root, text="Browse", command=select_svg_file, bg='#e88004', activebackground='#eb8e36', fg='#ffffff', font=font).grid(row=2, column=6, padx=10, pady=5, sticky='ew')

tk.Label(root, text="SVG Width:", bg='#232323', fg='#ffffff', font=font).grid(row=3, column=4, padx=10, pady=5, sticky='e')
entry_svg_width = tk.Entry(root, font=font)
entry_svg_width.grid(row=3, column=5, padx=10, pady=5, sticky='ew')
entry_svg_width.insert(0, last_inputs.get("svg_width", ""))

tk.Label(root, text="SVG Height:", bg='#232323', fg='#ffffff', font=font).grid(row=4, column=4, padx=10, pady=5, sticky='e')
entry_svg_height = tk.Entry(root, font=font)
entry_svg_height.grid(row=4, column=5, padx=10, pady=5, sticky='ew')
entry_svg_height.insert(0, last_inputs.get("svg_height", ""))

tk.Label(root, text="Save Location:", bg='#232323', fg='#ffffff', font=font).grid(row=8, column=4, padx=10, pady=5, sticky='e')
entry_save_location = tk.Entry(root, font=font)
entry_save_location.grid(row=8, column=5, padx=10, pady=5, sticky='ew')
entry_save_location.insert(0, last_inputs.get("save_location", ""))
tk.Button(root, text="Browse", command=select_save_location, bg='#e88004', activebackground='#eb8e36', fg='#ffffff', font=font).grid(row=8, column=6, padx=10, pady=5, sticky='ew')

tk.Label(root, text="Colors of Links:", bg='#232323', fg='#ffffff', font=font).grid(row=5, column=4, padx=10, pady=5, sticky='e')
entry_links_color = tk.Entry(root, font=font)
entry_links_color.grid(row=5, column=5, padx=10, pady=5, sticky='ew')
entry_links_color.insert(0, last_inputs.get("links_color", ""))

tk.Label(root, text="Color of Connect Button:", bg='#232323', fg='#ffffff', font=font).grid(row=6, column=4, columnspan=1, padx=10, pady=5, sticky='e')
entry_button_color = tk.Entry(root, font=font)
entry_button_color.grid(row=6, column=5, padx=10, pady=5, sticky='ew')
entry_button_color.insert(0, last_inputs.get("button_color", ""))

tk.Label(root, text="Visit Us URL:", bg='#232323', fg='#ffffff', font=font).grid(row=6, column=0, padx=10, pady=5, sticky='e')
entry_visit_us = tk.Entry(root, font=font)
entry_visit_us.grid(row=6, column=1, columnspan=2, padx=10, pady=5, sticky='ew')
entry_visit_us.insert(0, last_inputs.get("visit_us", ""))

#tk.Label(root, text="Button Hover Color:", bg='#232323', fg='#ffffff', font=font).grid(row=7, column=4, padx=10, pady=5, sticky='e')
#entry_hover_color = tk.Entry(root, font=font)
#entry_hover_color.grid(row=7, column=5, padx=10, pady=5, sticky='ew')
#entry_hover_color.insert(0, last_inputs.get("hover_color", ""))

# Apply placeholders to entry widgets
apply_placeholder(entry_company_name, placeholders["company_name"])
apply_placeholder(entry_slogan, placeholders["slogan"])
apply_placeholder(entry_svg_file, placeholders["svg_file"])
apply_placeholder(entry_svg_width, placeholders["svg_width"])
apply_placeholder(entry_svg_height, placeholders["svg_height"])
apply_placeholder(entry_address, placeholders["address"])
apply_placeholder(entry_phone_number, placeholders["phone_number"])
apply_placeholder(entry_terms_of_service, placeholders["terms_of_service"])
apply_placeholder(entry_privacy_statement, placeholders["privacy_statement"])
apply_placeholder(entry_faq, placeholders["faq"])
apply_placeholder(entry_contact_page, placeholders["contact_page"])
apply_placeholder(entry_save_location, placeholders["save_location"])
apply_placeholder(entry_links_color, placeholders["links_color"])
apply_placeholder(entry_button_color, placeholders["button_color"])
# apply_placeholder(entry_hover_color, placeholders["hover_color"])

# Create and Clear Fields buttons
tk.Button(root, text="Create Flipper Portal", command=on_submit, bg='#e88004', activebackground='#eb8e36', fg='#ffffff', font=font).grid(row=20, column=2, padx=2, columnspan=2, sticky='nsew')
tk.Button(root, text="Clear Fields", command=clear_fields, bg='#e88004', activebackground='#eb8e36', fg='#ffffff', font=font).grid(row=20, column=4, padx=2, columnspan=2, sticky='nsew')

# GitHub logo link
github_logo_label = tk.Label(root, image=github_logo, bg='#232323', cursor="hand2")
github_logo_label.grid(row=21, column=6, columnspan=1, pady=10, sticky='nsew')
github_logo_label.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/AugustAlcorn"))

# Configure the grid to center the buttons and logo
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure(2, weight=1)
root.grid_columnconfigure(3, weight=1)
root.grid_columnconfigure(4, weight=1)
root.grid_columnconfigure(5, weight=1)
root.grid_columnconfigure(6, weight=1)
root.grid_columnconfigure(7, weight=1)
root.grid_columnconfigure(8, weight=1)
# Bind the save_window_size_and_position function to the window close event
root.protocol("WM_DELETE_WINDOW", lambda: [save_window_size_and_position(), root.destroy()])

# Start the main loop
root.mainloop()