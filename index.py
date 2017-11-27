from PIL import Image
import imagehash
import pickle
import os

attachments = {}

for p in os.listdir ("attachments"):
    attachments[p] = imagehash.phash(Image.open("attachments/" + p))
    print(".", end='', flush=True)

pickle.dump(attachments, open("attachments.p", "wb"))
