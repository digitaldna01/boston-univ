from flask import Flask, render_template, request, send_file, jsonify
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from kmean_implementation import KMeans, generate_dataset, initial_capture
import os
import glob
import json

# Path to the folder
folder_path = 'static/step_images/'

app = Flask(__name__)

# Global variable to hold the dataset
# data_points = []
kmeans = None
total_step = 0
data_points = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/initial')
def initial():
    global data_points
    num_points = int(request.args.get('numPoints', 300))
    
    data_points = generate_dataset(num_points)
    
    initial_capture(data_points)

    # Send the image back
    return send_file('static/initial_visualization.png')

@app.route('/step')
def step():
    step_number = int(request.args.get('step', 0))
    # Logic to determine the appropriate image for the step
    image_path = f'static/step_images/step_{step_number}.png'
    return send_file(image_path)

@app.route('/generate')
def generate():
    global kmeans
    global total_step
    k = int(request.args.get('k', 0))
    init_method = request.args.get('init_method', 'random')
    
    # Perform KMeans clustering
    kmeans = KMeans(data_points, k)
    total_step = kmeans.lloyds(init_method)  # Run the KMeans algorithm
    
    return str(total_step)

@app.route('/generate_manual')
def generate_menual():
    global kmeans
    global total_step
    k = int(request.args.get('k', 0))
    data_selected = request.args.get('manuel_data')
    selected_points = json.loads(data_selected)
    
    # Perform KMeans clustering
    kmeans = KMeans(data_points, k)
    total_step = kmeans.manual_lloyds(selected_points)  # Run the KMeans algorithm
    
    return str(total_step)

@app.route('/reset')
def reset():
    global kmeans
    kmeans = None 
    global total_step
    total_step = 0
    
    # Use glob to find all files in the folder
    files = glob.glob(os.path.join(folder_path, '*'))

    # Delete each file
    for file in files:
        os.remove(file)
        print(f"Deleted {file}")
    
    return send_file('static/initial_visualization.png')  # 이미지 파일 전송
    
@app.route('/newDataset')
def newDataSet():
    global kmeans
    kmeans = None 
    global total_step
    total_step = 0
    
    # Use glob to find all files in the folder
    files = glob.glob(os.path.join(folder_path, '*'))

    # Delete each file
    for file in files:
        os.remove(file)
        print(f"Deleted {file}")
        
    global data_points
    num_points = int(request.args.get('numPoints', 300))
    
    data_points = generate_dataset(num_points)
    
    initial_capture(data_points)

    # Send the image back
    return send_file('static/initial_visualization.png')

# pass current data points to manual plot
@app.route('/getDataPoints')
def get_data_points():
    global data_points
    if data_points is not None:
        return jsonify(data_points.tolist())
    return jsonify([])

@app.route('/saveMaualPoints', methods=['POST'])
def save_manual_points():
    selected_points = request.json.get('selectedPoints', [])
    # 이 부분에서 필요한 동작을 수행하여 selected_points를 저장하거나 사용하세요.
    print("Selected Points:", selected_points)
    return jsonify({"status": "success", "message": "Selceted points saved successgfully"})

# @app.route('/set_manual_points', methods=['POST'])
# def set_manual_points():

