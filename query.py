from PIL import Image
import pickle
import sys
import imagehash

attachments = pickle.load(open("attachments.p", "rb"))

hash = imagehash.phash(Image.open(sys.argv[1]))


for k, v in reversed(sorted(attachments.items(), key=lambda a: hash - a[1])):
    print(k, v, hash - v)


