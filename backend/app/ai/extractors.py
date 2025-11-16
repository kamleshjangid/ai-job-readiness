def extract_text_from_file(path: str) -> str:
    if path.lower().endswith(".pdf"):
        return _pdf_to_text(path)
    if path.lower().endswith(".docx"):
        return _docx_to_text(path)
    return ""

def _pdf_to_text(path):
    from io import StringIO
    from pdfminer.high_level import extract_text_to_fp
    out = StringIO()
    with open(path, "rb") as fh:
        extract_text_to_fp(fh, out)
    return out.getvalue()

def _docx_to_text(path):
    import docx
    doc = docx.Document(path)
    return "\n".join(p.text for p in doc.paragraphs)
