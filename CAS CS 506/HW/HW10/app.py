from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from image_search import embed_image, embed_text, embed_hybrid, get_top_images, pca_image

app = Flask(__name__)

# Define the main route
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle experiment parameters and trigger the experiment
@app.route('/run_experiment', methods=['POST'])
def run_experiment():
    query_type = request.form['query_type']
    embed_type = request.form['embed_type']
    image_query = request.files['image_query']
    text_query = request.form['text_query']
    hybrid_weight = request.form['hybrid_weight']
    
    if query_type == "image":
        if embed_type == "clip":
            image_embedding = embed_image(image_query)
            images, similarities = get_top_images(image_embedding)
        elif embed_type == "pca":
            images, similarities = pca_image(image_query)
    elif query_type == "text":
        text_embedding = embed_text(text_query)
        images, similarities = get_top_images(text_embedding)
    elif query_type == "hybrid":
        hybrid_weight = float(hybrid_weight)
        hybrid_embedding = embed_hybrid(image_query, text_query, hybrid_weight)
        images, similarities = get_top_images(hybrid_embedding)
    
    print(images)
    return jsonify({
        "images": images, "top_sims" : similarities
    })

@app.route('/coco_images_resized/<path:filename>')
def send_image(filename):
    return send_from_directory('coco_images_resized', filename)

if __name__ == '__main__':
    app.run(debug=True)
    
