import os
import shutil
from Compressor import compress
#
dirpath = r'20th_july_redacted2'
for path in os.listdir(dirpath):

    if os.path.isfile(os.path.join(dirpath, path)):
        os.remove("Downloaded_CVs_20th_July/{}.pdf".format(path[:-13]))
        print("pdf removed")
res1 = []

for path in os.listdir(dirpath):
    # check if current path is a file
    if os.path.isfile(os.path.join(dirpath, path)):
        res1.append(path)

for files in res1:
    src_path = fr"20th_july_redacted2\{files}"
    print(src_path)
    compress(src_path)
    os.remove(src_path)


# res2 = []
#
# for path in os.listdir('Downloaded_CVs_20th_July'):
#     # check if current path is a file
#     if os.path.isfile(os.path.join('Downloaded_CVs_20th_July', path)):
#         res2.append(path)
#
# for file in res2:
#     if 'pdf' not in file:
#         print(file)
#         os.remove('Downloaded_CVs_19th_July/{}'.format(file))
#         print('file removed')