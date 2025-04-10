import re
from docx import Document

def extract_tags(docx_path):
    doc = Document(docx_path)
    text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])
    tags = re.findall(r'\{\{(\w+)\}\}', text)
    return tags
