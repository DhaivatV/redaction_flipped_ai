from PyPDF2 import PdfReader, PdfWriter


def compress(input_file):
    reader = PdfReader(input_file)
    writer = PdfWriter()

    for page in reader.pages:
        page.compress_content_streams()  # This is CPU intensive!
        writer.add_page(page)

    with open(f"20th_july_redacted/{input_file[20:]}", "wb") as f:
        writer.write(f)
        print(f"{input_file} compressed and saved")


