from flask import Flask, request, send_from_directory, url_for
from PIL import Image
import pickle
import sys
import imagehash
import urllib
import base64


app = Flask(__name__)\

attachments = pickle.load(open("attachments.p", "rb"))

def find(file):
    hash = imagehash.phash(Image.open(file))
    results = []
    for k, v in sorted(attachments.items(), key=lambda a: hash - a[1]):
        similarity = hash - v
        if similarity <= 7:
            results.append({
                "id": k,
                "similarity": similarity
            })

    return results


@app.route("/", methods=['GET', 'POST'])
def hello():

    results = ""
    if request.method == 'POST':
        file = request.files['file']

        for r in find(file):
            print(r)
            results += """
            <div><img width="400" src="%s" />%d%% (%d bits off)</div>
            """ % (url_for('image', path=r["id"]), 100*(64-r["similarity"])/64, r["similarity"])
        print(results)


    return """
    <div><form method="post" enctype="multipart/form-data"><input type="file" name="file"><input type="submit"></div>
    """ + results

@app.route('/img/<path:path>')
def image(path):
    return send_from_directory('attachments', path)
