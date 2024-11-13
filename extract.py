import pdfplumber

def extract_initial_pages(pdf_file, num_pages):
    # Open the input PDF file
    with pdfplumber.open(pdf_file) as pdf:
        # Extract the initial pages
        initial_pages = pdf.pages[:num_pages]

        # Create the output file name
        output_file = f"{pdf_file.split('.')[0]}_initial_{num_pages}.pdf"

        # Save the new PDF file
        initial_pages.save(output_file)

extract_initial_pages("../vadim/claro/files/Exemplos/TR_Cidade_Inteligente_22052024_VersaoCotacao.pdf", 3)