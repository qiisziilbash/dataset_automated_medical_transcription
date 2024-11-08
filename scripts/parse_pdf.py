#%%
import os
from pypdf import PdfReader

#%%
def extract_text_from_pdf(pdf_path):
    """Extract text content from a PDF file."""
    try:
        reader = PdfReader(pdf_path)

        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"

        return text
    except Exception as e:
        raise ValueError(f"Error processing {pdf_path}: {str(e)}")

def process_all_pdfs():
    """Process all PDFs in the transcripts/source directory."""
    source_dir = "../transcripts/source"
    output_dir = "data/source_text"

    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(source_dir):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(source_dir, filename)
            text = extract_text_from_pdf(pdf_path)

            if text:
                output_filename = os.path.splitext(filename)[0] + ".txt"
                output_path = os.path.join(output_dir, output_filename)

                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(text)
                print(f"Successfully processed: {filename}")

#%%
process_all_pdfs()

