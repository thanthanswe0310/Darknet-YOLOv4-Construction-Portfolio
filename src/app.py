from flask import Flask, request, jsonify
import darknet
import cv2
import numpy as np

app = Flask(__name__)

# Load YOLO network
network, class_names, class_colors = darknet.load_network(
    "cfg/yolov4.cfg",
    "cfg/coco.data",
    "weight/yolov4-obj_final.weights",
    batch_size=1
)

@app.route("/predict", methods=["POST"])
def predict():
    file = request.files['image']
    image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
    width = darknet.network_width(network)
    height = darknet.network_height(network)
    darknet_image = darknet.make_image(width, height, 3)
    image_resized = cv2.resize(image, (width, height))
    darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())
    
    detections = darknet.detect_image(network, class_names, darknet_image)
    darknet.free_image(darknet_image)

    return jsonify({"detections": detections})
