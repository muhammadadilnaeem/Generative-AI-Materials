from PyPDF2 import PdfReader, PdfWriter

def extract_pages(input_pdf, output_pdf, start_page, end_page):
    """
    Extract specified pages from a PDF and save them into a new PDF.

    :param input_pdf: Path to the input PDF file.
    :param output_pdf: Path to the output PDF file.
    :param start_page: Starting page number (1-based index).
    :param end_page: Ending page number (inclusive, 1-based index).
    """
    # Load the input PDF
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    # Add pages from start_page to end_page to the writer
    for i in range(start_page - 1, end_page):  # Convert to 0-based index
        writer.add_page(reader.pages[i])

    # Write the selected pages to the output PDF
    with open(output_pdf, 'wb') as output_file:
        writer.write(output_file)

# Example usage
input_pdf = r"input_doc/Handouts MTH101 Reviewed.pdf"   # Replace with your input PDF file path
output_pdf = "output_doc/Lecture 44.pdf" # Replace with your desired output PDF file path
start_page = 290          # Replace with the starting page number
end_page = 295            # Replace with the ending page number

extract_pages(input_pdf, output_pdf, start_page, end_page)
print("Pages extracted successfully! Good to Go Buddy!")