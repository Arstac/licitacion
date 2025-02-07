from markitdown import MarkItDown

def convert_to_md(file_path: str):
    markitdown = MarkItDown()
    result = markitdown.convert(file_path)

    return result.text_content


pdf = "Data/lic_2.pdf"
markitdown = convert_to_md(pdf)

print(markitdown)