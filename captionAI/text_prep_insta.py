import string
from os import listdir
import os
from emoji import UNICODE_EMOJI

# load doc into memory


def load_doc(filename):
    # open the file as read only
    file = open(filename, 'r')
    # read all text
    text = file.read()
    # close the file
    file.close()
    return text

# extract descriptions for images


def load_descriptions(filename):
    directory = 'insta_small_dataset/captions/'

    mapping = dict()
    # process lines
    # for line in doc.split('\n'):
    # 	# split line by white space
    # 	tokens = line.split()
    # 	if len(line) < 2:
    # 		continue
    for name in listdir(filename):
        text = ''
        with open(os.path.join(directory, name), 'r') as f:
            text = f.read()

        # get image ID from filename
        image_id = name[:-4]

        # create the list if needed
        if image_id not in mapping:
            mapping[image_id] = list()

        # store description
        mapping[image_id].append(text)
    return mapping


def clean_descriptions(descriptions):
    # prepare translation table for removing punctuation
    table = str.maketrans('', '', '!"$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')
    for key, desc_list in descriptions.items():
        for i in range(len(desc_list)):
            desc = desc_list[i]
            # tokenize
            desc = desc.split()
            # convert to lower case
            desc = [word.lower() for word in desc]
            # remove punctuation from each token
            desc = [w.translate(table) for w in desc]
            # remove hanging 's' and 'a', keep emojis
            desc = [word for word in desc if len(word) > 1 or word in UNICODE_EMOJI]

            # remove NYC
            desc = [word for word in desc if ('nyc' not in word) and ('newyork' not in word)]
            # remove tokens with numbers in them
            # desc = [word for word in desc if word.isalpha()]
            # store as string
            desc_list[i] = ' '.join(desc)

# convert the loaded descriptions into a vocabulary of words


def to_vocabulary(descriptions):
    # build a list of all description strings
    all_desc = set()
    for key in descriptions.keys():
        [all_desc.update(d.split()) for d in descriptions[key]]
    return all_desc

# save descriptions to file, one per line


def save_descriptions(descriptions, filename):
    lines = list()
    for key, desc_list in descriptions.items():
        for desc in desc_list:
            lines.append(key + ' ' + desc)
    data = '\n'.join(lines)
    file = open(filename, 'w')
    file.write(data)
    file.close()


filename = 'insta_small_dataset/captions'
# load descriptions
# parse descriptions
descriptions = load_descriptions(filename)
print('Loaded: %d ' % len(descriptions))
# clean descriptions
clean_descriptions(descriptions)
# summarize vocabulary
vocabulary = to_vocabulary(descriptions)
print('Vocabulary Size: %d' % len(vocabulary))
# save to file
save_descriptions(descriptions, 'small_descriptions.txt')
