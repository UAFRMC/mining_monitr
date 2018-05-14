#!/usr/bin/env python3
#
# Project: Video Streaming with Flask
# Author: Log0 <im [dot] ckieric [at] gmail [dot] com>
# Date: 2014/12/21
# Website: http://www.chioka.in/
# Description:
# Modified to support streaming out with webcams, and not just raw JPEGs.
# Most of the code credits to Miguel Grinberg, except that I made a small tweak. Thanks!
# Credits: http://blog.miguelgrinberg.com/post/video-streaming-with-flask
#
# Usage:
# 1. Install Python dependencies: cv2, flask. (wish that pip install works like a charm)
# 2. Run "python main.py".
# 3. Navigate the browser to the local webpage.
from flask import Flask, render_template, Response, send_file, make_response
from camera import VideoCamera
import subprocess
import cv2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        success, jpeg = camera.get_frame()
        print(success)
        if success:
        	frame = jpeg.tobytes()
        	yield (b'--frame\r\n'
            	   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/latest')
def latest_image():
	return render_template('get_image.html')

@app.route('/get_image')
def get_image():
	ffmpeg = subprocess.run("ffmpeg -i /dev/video1 -frames 1 latest.jpeg -y", shell=True)
	# img = cv2.imread('latest.jpeg',0)
	# frame = img.tobytes()
	# return Response(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + 
	# 	frame + b'\r\n\r\n',mimetype='multipart/x-mixed-replace; boundary=frame')
	response = make_response(send_file('latest.jpeg', mimetype='image/jpeg'))
	response.headers['Cache-Control'] = "no-cache, no-store, must-revalidate"
	response.headers["Pragma"] = "no-cache"
	response.headers["Expires"] = "0"
	return response
	

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)