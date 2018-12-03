#!/usr/bin/python3

import base64
import io
import os
import pymongo

def mongo_connect():
    '''
    Returns a pymongo client object
    '''
    # read password from a file
    with open('password', 'r') as f:
        passwd = f.read().strip()

    url = "mongodb+srv://mistake-bot:{}@cc-db-jv4pb.mongodb.net/test?retryWrites=true".format(passwd)
    return pymongo.MongoClient(url)

def parse_filename(filename):
    '''
    Parses an image filename, removing the extension (jpg/jpeg/png/gif)
    and replacing underscores with whitespaces
    '''
    parsed_name = filename.replace('_', ' ')
    file_exts = ['jpg', 'jpeg', 'png']
    for e in file_exts:
        parsed_name = parsed_name.replace('.' + e, '')
    return parsed_name

mongo = mongo_connect()
# start by removing all existing cards, or comment this out to avoid this step
mongo.cc.cards.delete_many({ })

files = []
for file in os.listdir():
    if file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png"):
        files.append(file)

index = 0
total = len(files)
for file in files:
    with open(file, 'rb') as fs:
        # store the base64 encoded string for each image
        encoded = base64.b64encode(fs.read())
        print ("Adding card {}/{}...".format(index, total))
        mongo.cc.cards.insert_one({
            "name": parse_filename(file),
            "data": encoded
        })

print("Done")
