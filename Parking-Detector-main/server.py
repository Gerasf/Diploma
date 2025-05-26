from flask import Flask, render_template, request, Response, jsonify
import parking_model
import parkingPositionsDetector
import dbHandler_pg as dbHandler  # Импорт модуля
import threading
from flask_cors import CORS

import cProfile
import time

# Create a Flask instance and enable CORS
app = Flask(__name__)
CORS(app)

# Define a route for the index page
@app.route("/")
def index():
    totalSpaces = model.getTotalSpaces()
    freeSpaces = model.getFreeSpaces()
    return render_template('/HTML/index.html', total_spaces=totalSpaces, free_spaces=freeSpaces)

# Define a route for the video feed
@app.route("/video_feed")
def video_feed():
    return Response(model.generate(), mimetype="multipart/x-mixed-replace; boundary=frame")

# Define a route for the parking space information
@app.route("/info")
def info():
    freeSpaces = model.getFreeSpaces()
    totalSpaces = model.getTotalSpaces()
    return jsonify(totalSpaces_value=totalSpaces, freeSpaces_value=freeSpaces)

if __name__ == "__main__":
    stream = 'testvideo3.MOV'
    # stream = 'http://eitancamhome:eitancamhome@10.100.102.10:6677/video'

    # Create an instance of the DbHandler
    db = dbHandler.DbHandler()  # Создаём экземпляр

    weights = 'yolov5s'

    # Create an instance of the parking_model class
    model = parking_model.Model(stream, db, weights)  # Передаём db
    t1 = threading.Thread(target=model.stream)
    t1.daemon = True
    t1.start()

    detector = parkingPositionsDetector.Detector(stream, db)
    t2 = threading.Thread(target=detector.detectionAlgorithm)
    t2.daemon = True
    t2.start()

    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True, use_reloader=False)