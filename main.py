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
import os


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

def search_contact_and_email(data, reg):

    try:
        if re.search(reg, data, re.IGNORECASE):
            search = re.search(reg, data, re.IGNORECASE)
            return search

    except Exception as e:
        print(f"{e}, error occured while finding contact and email in data")

def search_links(data, reg):
    links = []
    try:
        search = re.findall(reg, data, re.IGNORECASE)
        for items in search:
            links.append(items[0])

        return links

    except Exception as e:
        print(f"{e}, error occured while finding links in data")

def search_name_data (reg, data):

    try:
        search_name = re.search(reg, data, re.IGNORECASE).group(0).split()

        for item in search_name:
            if item[:1].isupper():
                search_name.append(item[:1].lower() + item[1:])

        return search_name

    except Exception as e:
        print(f"{e}, error occured while finding name data")

def redact(cv_path, redaction_list, link_text, name_text, short_links):
        try :
            doc = fitz.open(cv_path)
        except Exception as e:
            print("Incorrect Path in func redact")
        try:
            for page in doc:
                page.wrap_contents()


                for redact_items in redaction_list:
                        areas = page.search_for(redact_items)

                        for area in areas:
                            print(area)
                            [page.add_redact_annot(area, fill = (0, 0, 0)) for area in areas]

                            page.apply_redactions()

        except Exception as e:
            print(f"Error{e}, cannot redact email and contact number")

        try:
            for items in link_text:
                    areas = page.search_for(items)
                    for area in areas:

                        [page.add_redact_annot(area, fill = (0, 0, 0)) for area in areas]

                        page.apply_redactions()
        except Exception as e:
            print(f"Error{e}, cannot redact links in data")

        try:
            for name in name_text:
                    areas = page.search_for(name)
                    for area in areas:

                        [page.add_redact_annot(area, fill = (0, 0, 0)) for area in areas]

                        page.apply_redactions()
        except Exception as e:
            print(f"Error{e}, cannot redact name in data")

        try:
            for s_link in short_links:
                    areas = page.search_for(s_link)
                    for area in areas:

                        [page.add_redact_annot(area, fill = (0, 0, 0)) for area in areas]

                        page.apply_redactions()
        except Exception as e:
            print(f"Error{e}, cannot redact other urls in data")

        num = random.randint(1,10000000)
        try:
            doc.save('Redacted CVs/redacted{}.pdf'.format(num))
        except Exception as e:
            print(f"Error{e},Redacted document not saved")

def remove_img_on_pdf(cv_path):
    try:
        doc = fitz.open(cv_path)
    except :
        print("Incorrect Path")

    try:
        for page in doc:
            page.wrap_contents()
            img_list = page.get_images()
            con_list = page.get_contents()


            for i in con_list:
                c = doc.xref_stream(i)
                if c != None:
                    for v in img_list:

                        arr = bytes(v[7], 'utf-8')
                        r = c.find(arr)  # try find the image display command
                        if r != -1:
                            cnew = c.replace(arr, b"")
                            doc.update_stream(i, cnew)
                            c = doc.xref_stream(i)

        return doc

    except Exception as e :
        print("Cannot Remove Images")


if __name__ == "__main__":
    cv_path = ("CVs/Resume_testing14.pdf")
    rdoc = remove_img_on_pdf(cv_path)
    rdoc.save('no_img_example.PDF')

    new_cv_path = 'no_img_example.PDF'
    Data = extract_text_from_pdf(new_cv_path)

    urls = []


    EMAIL_REG = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    Contact_REG = r'(?:\+\d{2})?\d{3,4}\D?\d{3}\D?\d{3}'
    Link_REG = r'((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)'
    NAME_REG = r'\b[A-Z][a-z]* [A-Z][a-z]*( [A-Z])?[A-Z][a-z]*( [A-Z])?[A-Z][a-z]*'


    data_list = list(Data.split())
    for item in data_list:
        if ".com" in item or ".in" in item or ".org" in item or ".net" in item or ".co" \
                in item or ".us" in item or "github.io" in item and "@" not in item:
            urls.append(item)



    try :
         email_text = search_contact_and_email(Data, EMAIL_REG).group(0)
    except AttributeError as attr:
        email_text = "no email"

    try:
         contact_text = search_contact_and_email(Data, Contact_REG).group(0)
    except AttributeError as attr:
        contact_text= "no_contact_number"

    try:
         links_text = search_links(Data, Link_REG)
    except AttributeError as attr:
        links_text = "no_link_text"

    try:
         name_text = search_name_data(NAME_REG, Data)
    except AttributeError as attr:
          name_text = "no_name_text"

    try:
         llink_text = urls
    except len(llink_text)<0:
        llink_text = "urls"



    redactions = [email_text, contact_text]
    print(email_text, contact_text, links_text, name_text, llink_text)

    try:
        redact(new_cv_path, redactions, links_text, name_text, llink_text)
        os.remove("no_img_example.PDF")
        print(f'{cv_path[4:]} has been redacted')
    except:
        print("pdf not redacted")























