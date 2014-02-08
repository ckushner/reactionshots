"""
SHOTS API for reaction shots (snapchat hack)

requires:
pycrypto==2.6.1
requests==2.0.1

"""
import os
from flask import *
import json
#import sys
#sys.path.append("/snapchat-python/src/")
from snapchat import Snapchat

#create our little app
app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/")
def begin():
	return "don't be lazy man!\n"

#login function used in all calls 
@app.route("/login", methods=['POST', 'GET'])
def login():
	data = request.get_json()
	s = Snapchat()
	s.login(data['username'],data['password'])
	if s.logged_in == False:
		return {"success":False};
	s.logout()
	return {"success":True};

#send a snapchat
@app.route("/send/<filetype>", methods=['POST'])
def send():
	data = request.get_json()
	s = Snapchat()
	s.login(data['username'],data['password'])

	snap = request.files['file']
        extension = ".jpg"
        if filetype == 'video':
                extension = '.mp4'
        filename = 'uploaded_file' + extension
	snap.save(filename)

	#upload file to snapchat
	if (filetype == "image"):
		snapformat = Snapchat.MEDIA_IMAGE
	if (filetype == "video"):
		snapformat = Snapchat.MEDIA_VIDEO

	media_id = s.upload(snapformat, filename)
	s.send(media_id, data['recipient'])

	#s.logout()
	return Response(json.dumps({"success":True}), mimetype='text/javascript')
	
#getall
@app.route("/getall", methods=['GET'])
def getall():
	#login
	username = request.args.get('username', '')
	password = request.args.get('password', '')
	s = Snapchat()
	s.login(username, password)

	#get all snaps for the user 
	snaps = s.get_snaps()

	allsnaps = []
	for snap in snaps:
                if snap['id'][-1] != 's' and snap['status'] != 2:
                        # Download a snap
                        media = s.get_media(snap['id'])
                        newFile = open('./static/' + snap['id'] + ".jpeg", "wb")
                        reportedMediaType = snap['media_type']
                        fileType = {
                                None: 'image',
                                1: 'video',
                                2: 'video',
                                3: None,
                                4: None,
                                5: None,
                                6: None
                        }[reportedMediaType]
                        ext = '.mp4'
                        if fileType == 'image':
                                ext = ".jpeg"
                        if fileType == 'image' or fileType == 'video':
                                allsnaps.append({
                                        'file':snap['id'] + ext,
                                        'senderName':snap['sender'],
                                        'fileType': fileType})
                                newFileByteArray = bytearray(media)
                                newFile.write(newFileByteArray)



	return Response(json.dumps(allsnaps), mimetype='text/javascript')

#clear snapchat history
@app.route("/clear")
def clear():
	s = login()
	s.clear_feed()
	return s

if __name__ == "__main__":
    app.run()

