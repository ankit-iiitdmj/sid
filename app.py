import streamlit as st
import pandas as pd
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import io

# Register the Teko SemiBold font
pdfmetrics.registerFont(TTFont('Teko-SemiBold', 'Teko-SemiBold.ttf'))

# Function to create a PDF with names
def create_names_pdf(names):
    names = [name.upper() for name in names]  # Convert all names to uppercase
    # Constants for the page and name area
    page_width, page_height = A4[1], A4[0]  # Landscape orientation
    name_area_width, name_area_height = 11 * inch, 1.8 * inch
    margin_top, margin_left = 0.1 * inch, 0.1 * inch
    max_names_per_page = 4  # Maximum number of names per page

    # Create a bytes buffer for the PDF file
    buffer = io.BytesIO()

    # Initialize the PDF canvas
    c = canvas.Canvas(buffer, pagesize=(page_width, page_height))
    bold_font = "Teko-SemiBold"  # Using bold font

    num_pages = len(names) // max_names_per_page + (1 if len(names) % max_names_per_page > 0 else 0)

    for page in range(num_pages):
        if page > 0:  # Add a new page if it's not the first one
            c.showPage()
        c.setFont('Teko-SemiBold', 12)
        start_index = page * max_names_per_page
        end_index = start_index + max_names_per_page
        for index, name in enumerate(names[start_index:end_index]):
            x = margin_left
            y = page_height - margin_top - (index + 1) * name_area_height
            total_width = sum(c.stringWidth(char, bold_font, 12) for char in name)
            scale_x = name_area_width / total_width
            scale_y = name_area_height / 12
            for char in name:
                char_width = c.stringWidth(char, bold_font, 12)
                c.saveState()
                c.translate(x, y)
                c.scale(scale_x, scale_y)
                c.drawString(0, 0, char)
                c.restoreState()
                x += char_width * scale_x
    c.save()

    # Move the buffer's pointer to the beginning so we can read its content
    buffer.seek(0)
    return buffer

# Function to create a PDF with numbers
def create_numbers_pdf(numbers):
    page_width, page_height = A4[1], A4[0]
    number_area_width, number_area_height = 5 * inch, 7 * inch
    margin_top, margin_left = 0.01 * inch, 0.01 * inch
    max_numbers_per_page = 2

    # Create a bytes buffer for the PDF file
    buffer = io.BytesIO()

    c = canvas.Canvas(buffer, pagesize=(page_width, page_height))

    for i, number in enumerate(numbers):
        if i % max_numbers_per_page == 0 and i != 0:
            c.showPage()
        x = margin_left + (i % 2) * number_area_width
        y = page_height - margin_top - number_area_height

        number_str = str(number)
        c.setFont('Teko-SemiBold', 12)
        total_width = c.stringWidth(number_str, 'Teko-SemiBold', 12)

        scale_x = number_area_width / total_width
        scale_y = number_area_height / (12 * 1.2)

        c.saveState()
        c.translate(x, y)
        c.scale(scale_x, scale_y)
        c.drawString(0, 0, number_str)
        c.restoreState()

    c.save()

    # Move the buffer's pointer to the beginning so we can read its content
    buffer.seek(0)
    return buffer

# Streamlit UI
st.title('PDF Generator for Names and Numbers')

# Link to download sample CSV
with open('sample.csv', 'r') as f:
    sample_csv = f.read()

st.download_button(label='Download Sample CSV', data=sample_csv, file_name='sample.csv', mime='text/csv')

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    # Read the uploaded CSV file
    df = pd.read_csv(uploaded_file)
    
    # Generate PDFs
    names_pdf = create_names_pdf(df['name'])
    numbers_pdf = create_numbers_pdf(df['number'])
    
    # Display download links for PDFs
    st.download_button(label='Download Names PDF', data=names_pdf, file_name='names.pdf', mime='application/pdf')
    st.download_button(label='Download Numbers PDF', data=numbers_pdf, file_name='numbers_full_stretch.pdf', mime='application/pdf')
