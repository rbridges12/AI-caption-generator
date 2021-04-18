import os
from urllib.request import urlopen

with open("test_file.jpg", 'w') as f:
    f.write("hello world")

url = 'https://static.wikia.nocookie.net/disney/images/9/9b/Profile_-_Pinocchio.jpeg/revision/latest/top-crop/width/360/height/450?cb=20190312063307'
res = urlopen(url)
filename = url.replace('.', '') + '.jpg'
filename = filename.replace('/', '')
with open(filename, 'wb') as f:
    f.write(res.read())

