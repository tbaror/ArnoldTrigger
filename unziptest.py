import zipfile
fh = open("c:/force10-s4810_User's Guide5_en-us.zip", 'rb')
z = zipfile.ZipFile(fh)
for name in z.namelist():
    outpath = "C:/testzip"
    z.extract(name, outpath)