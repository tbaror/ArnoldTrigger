import urllib.request
import zipfile
file_name = 'ninite.exe'

try:

    url = 'https://nnite.com/7zip/ninite.exe'
    # Download the file from `url` and save it locally under `file_name`:
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        data = response.read() # a `bytes` object
        out_file.write(data)
except Exception  as e:
    print(e)

