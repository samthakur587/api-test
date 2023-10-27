import pdfminer.high_level
import markdown
import os
def pdf_to_markdown(pdf_path, md_path):
    # Extract text from PDF
    with open(pdf_path, 'rb') as pdf_file:
        text = pdfminer.high_level.extract_text(pdf_file)

    # Convert text to markdown
    md_text = markdown.markdown(text)
    path = md_path + "/test.txt"
    # Write markdown to file
    with open(path, 'w') as md_file:
        md_file.write(md_text)
    return md_text

s = pdf_to_markdown("2012_07_09_David_Pesko.pdf",os.getcwd())
print(s)