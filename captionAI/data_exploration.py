import os
from shutil import copyfile

directory = 'InstaNY100K/InstaNY100K/img_resized/newyork'
listOfImages = []
listOfCaptions = []
caption_dir = 'insta_small_dataset/captions'
img_dir = 'insta_small_dataset/imgs'
size = 10000
indices = []


def good_length(name):
    with open(os.path.join('InstaNY100K/InstaNY100K/captions/newyork/', name), 'r') as f:
        text = f.read()
        length = len(text.split())
        return not (length > 40 or size < 3)


c = -1
for i, name in enumerate(sorted(os.listdir('InstaNY100K/InstaNY100K/captions/newyork'))):

    if good_length(name):
        indices.append(i)
        listOfCaptions.append(name)
        c += 1

    if c > size - 2:
        break

c = -1
for i, name in enumerate(sorted(os.listdir('InstaNY100K/InstaNY100K/img_resized/newyork'))):

    if i in indices:
        listOfImages.append(name)
        c += 1

    if c > size - 2:
        break

print(len(listOfCaptions))

with open('insta_small_dataset/train_images.txt', 'w') as f:
    for name in listOfImages:
        f.write(name + '\n')

for i in range(size):
    # print("Image: %s, Caption %s" % (listOfImages[i], listOfCaptions[i]))
    img_source_dir = os.path.join(
        'InstaNY100K/InstaNY100K/img_resized/newyork', listOfImages[i])
    caption_source_dir = os.path.join(
        'InstaNY100K/InstaNY100K/captions/newyork', listOfCaptions[i])
    copyfile(img_source_dir, os.path.join(img_dir, listOfImages[i]))
    copyfile(caption_source_dir, os.path.join(caption_dir, listOfCaptions[i]))
