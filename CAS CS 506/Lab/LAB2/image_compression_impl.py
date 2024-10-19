import numpy as np
from sklearn.cluster import KMeans
from PIL import Image

# Function to load and preprocess the image
def load_image(image_path):
    # load_image(image_path): This function should load the image from a file and return it as a NumPy array. 
    image = Image.open(image_path)
    
    # Convert the image array
    image_array = np.array(image)
    return image_array

# Function to perform KMeans clustering for image quantization
def image_compression(image_np, n_colors):
    # image_compression(image_np, n_colors): Implement KMeans clustering using scikit-learn to reduce the number of colors in the image to n_colors. 
    # The function should return a compressed version of the image.
    # Reshape the image to a 2D array of pixels (height * width, channels)
    h, w, c = image_np.shape
    pixels = image_np.reshape(-1, c)

    # Apply KMeans clustering to the pixel data
    kmeans = KMeans(n_clusters=n_colors, random_state=42)
    kmeans.fit(pixels)

    # Replace each pixel value with its corresponding centroid
    compressed_pixels = kmeans.cluster_centers_[kmeans.labels_]
    
    # Reshape the compressed pixel array back to the original image shape
    compressed_image = compressed_pixels.reshape(h, w, c).astype(np.uint8)
    
    return compressed_image
    # raise NotImplementedError('You need to implement this function')

# Function to concatenate and save the original and quantized images side by side
def save_result(original_image_np, quantized_image_np, output_path):
    # Convert NumPy arrays back to PIL images
    original_image = Image.fromarray(original_image_np)
    quantized_image = Image.fromarray(quantized_image_np)
    
    # Get dimensions
    width, height = original_image.size
    
    # Create a new image that will hold both the original and quantized images side by side
    combined_image = Image.new('RGB', (width * 2, height))
    
    # Paste original and quantized images side by side
    combined_image.paste(original_image, (0, 0))
    combined_image.paste(quantized_image, (width, 0))
    
    # Save the combined image
    combined_image.save(output_path)

def __main__():
    # Load and process the image
    image_path = 'favorite_image.png'  
    output_path = 'compressed_image.png'  
    image_np = load_image(image_path)
    print(image_np)

    # Perform image quantization using KMeans
    n_colors = 4  # Number of colors to reduce the image to, you may change this to experiment
    quantized_image_np = image_compression(image_np, n_colors)

    # Save the original and quantized images side by side
    save_result(image_np, quantized_image_np, output_path)
    

__main__()
