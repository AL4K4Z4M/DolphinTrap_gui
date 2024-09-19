import os
from tkinter import messagebox

def create_html_file(output_path, replacements):
    try:
        # Read the SVG file
        with open(replacements['svg_file'], 'r') as svg_file:
            svg_data = svg_file.read()

        # Add width and height attributes to the SVG tag
        svg_data = svg_data.replace('<svg', f'<svg width="{replacements["svg_width"]}" height="{replacements["svg_height"]}"')

        # Add the formatted SVG data to replacements
        replacements['svg_data'] = svg_data

        # Read the HTML template from the file
        with open('template.html', 'r') as file:
            html_template = file.read()

        # Replace placeholders in the HTML template with actual values
        html_content = html_template
        for key, value in replacements.items():
            html_content = html_content.replace(f"{{{{ {key} }}}}", value)

        # Write the final HTML content to the output file
        with open(output_path, 'w') as file:
            file.write(html_content)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")