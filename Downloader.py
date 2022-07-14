import requests as requests

base_url = "https://india.gaiusnetworks.com/test/"
file_name = "documents/someAlphaNumericString.extention"

with open(f'{file_name.split("/")[:-1]}', 'wb') as f :

      r = requests.get(base_url+file_name)
      for chunk in r.iter_content(1024):
        if chunk:
          f.write(chunk)