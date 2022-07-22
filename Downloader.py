import os.path
import requests as requests
import pandas as pd
import xlrd

data = pd.read_csv("new.csv")

doc_list = data['Data1'].to_list()


doc_list1 = []
for items in doc_list:
     k = items.split(";")
     for item in k:
         if "documents" in item:
             doc_list1.append(item)



doc_file_name = []
for items in doc_list1:
    k = (items[11:-1])
    doc_file_name.append(k)







for name in doc_list1[1000:2000]:

    Name = (name[1:-1])
    base_url = "https://india.gaiusnetworks.com/test/"
    file_name = Name
    url = (base_url+file_name)

    output_dir = ".\Downloaded_CVs_20th_July"

    response = requests.get(url)
    if response.status_code == 200:
        filepath = os.path.join(output_dir, os.path.basename(file_name))
        with open(filepath, 'wb') as f:
            f.write(response.content)
    print("done")

# with open(f'Downloaded_CVs_16th_July/{file_name.split("/")[:-1]}', 'wb') as f :
#
#     # r = requests.get(base_url+file_name)
#     # f.write_bytes(r.content)
#
#     # for chunk in r.iter_content(1024):
#     #     if chunk:
#     #         f.write(chunk)
#
#     f.close()
#     print("done")





