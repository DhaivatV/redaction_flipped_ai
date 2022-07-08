from pdfminer.converter import TextConverter
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFSyntaxError
import io
import re
import fitz
import random
from address import AddressParser, Address


def extract_text_from_pdf(cv_path):
    if not isinstance(cv_path, io.BytesIO):
        with open(cv_path, 'rb') as fh:
            try:
                for page in PDFPage.get_pages(
                        fh,
                        caching=True,
                        check_extractable=True
                ):
                    resource_manager = PDFResourceManager()
                    fake_file_handle = io.StringIO()
                    converter = TextConverter(
                        resource_manager,
                        fake_file_handle,

                        laparams=LAParams()
                    )

                    page_interpreter = PDFPageInterpreter(
                        resource_manager,
                        converter
                    )

                    page_interpreter.process_page(page)

                    text = fake_file_handle.getvalue()
                    return text

                    converter.close()
                    fake_file_handle.close()
            except PDFSyntaxError:
                return
    else:
        try:
            for page in PDFPage.get_pages(
                    cv_path,
                    caching=True,
                    check_extractable=True
            ):
                resource_manager = PDFResourceManager()
                fake_file_handle = io.StringIO()
                converter = TextConverter(
                    resource_manager,
                    fake_file_handle,

                    laparams=LAParams()
                )
                page_interpreter = PDFPageInterpreter(
                    resource_manager,
                    converter
                )
                page_interpreter.process_page(page)

                text = fake_file_handle.getvalue()
                return text

                # close open handles
                converter.close()
                fake_file_handle.close()
        except PDFSyntaxError:
            return

def search_text(data, reg):
    if re.search(reg, data, re.IGNORECASE):
        search = re.search(reg, data, re.IGNORECASE)
        return search

def search_links(data, reg):
    links = []
    search = re.findall(reg, data, re.IGNORECASE)
    for items in search:
        links.append(items[0])

    return links

def search_name_data (reg, data):
    search_name = re.search(reg, data, re.IGNORECASE).group(0).split()

    for item in search_name:
        if item[:1].isupper():
            search_name.append(item[:1].lower() + item[1:])

    return search_name

def redact(cv_path, redaction_list, link_text, name_text, short_links):
        doc = fitz.open(cv_path)
        print(doc)
        for page in doc:
            page.wrap_contents()

            for redact_items in redaction_list:
                    areas = page.search_for(redact_items)

                    for area in areas:
                        print(area)
                        [page.add_redact_annot(area, fill = (0, 0, 0)) for area in areas]

                        page.apply_redactions()


            for items in link_text:
                    areas = page.search_for(items)
                    for area in areas:
                        print(area)
                        [page.add_redact_annot(area, fill = (0, 0, 0)) for area in areas]

                        page.apply_redactions()

            for name in name_text:
                    areas = page.search_for(name)
                    for area in areas:
                        print(area)
                        [page.add_redact_annot(area, fill = (0, 0, 0)) for area in areas]

                        page.apply_redactions()

            for s_link in short_links:
                    areas = page.search_for(s_link)
                    for area in areas:
                        print(area)
                        [page.add_redact_annot(area, fill = (0, 0, 0)) for area in areas]

                        page.apply_redactions()

        num = random.randint(1,10000000)
        doc.save('Redacted CVs/redacted{}.pdf'.format(num))

def detect_address(data):
    ap = AddressParser()
    addr = ap.parse_address(data)
    return addr


if __name__ == "__main__":
    cv_path = ("CVs/chandan cv(new) (1).pdf")
    Data = extract_text_from_pdf(cv_path)
    urls = []
    EMAIL_REG = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    Contact_REG = r'(?:\+\d{2})?\d{3,4}\D?\d{3}\D?\d{3}'
    Link_REG = r'((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)'
    NAME_REG = r'\b[A-Z][a-z]* [A-Z][a-z]*( [A-Z])?[A-Z][a-z]'
    data_list = list(Data.split())
    for item in data_list:
        if ".com" in item or ".in" in item or ".org" in item or ".net" in item or ".co" \
                in item or ".us" in item or "github.io" in item and "@" not in item:
            urls.append(item)
    try :
        email_text = search_text(Data, EMAIL_REG).group(0)
        contact_text = search_text(Data, Contact_REG).group(0)
        links_text = search_links(Data, Link_REG)
        name_text = search_name_data(NAME_REG, Data)
        llink_text = urls


    except AttributeError as e:
        email_text = search_text(Data, EMAIL_REG).group(0)
        contact_text = search_text(Data, (r'(?:\+?\(?\d{2,3}?\)?\D?)?\d{4}\D?\d{4}')).group(0)
        print(email_text, contact_text)
        link_text = search_text(Data, Link_REG).group(0)
        links_text = search_links(Data, Link_REG)
        name_text = search_name_data(NAME_REG, Data)
        llink_text = urls

    redactions=[email_text, contact_text]



    # print(email_text, contact_text, links_text, name_text, llink_text)
    # redact(cv_path, redactions, links_text, name_text, llink_text)
    # #
    print(detect_address(Data))

    # search1 = re.findall(r'[A-Za-z0-9]+://[A-Za-z0-9%-_]+(/[A-Za-z0-9%-_])*(#|\\?)[A-Za-z0-9%-_&=]*', Data, re.IGNORECASE)
    # print(search1)




















