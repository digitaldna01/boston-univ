import numpy as np
import pandas as pd
import os
import io
import torch
import torchvision.transforms as transforms
from PIL import Image
from open_clip import create_model_and_transforms, tokenizer, get_tokenizer
import torch.nn.functional as F
from sklearn.decomposition import PCA
from sklearn.metrics.pairwise import euclidean_distances

file_path = "coco_images_resized/"

df = pd.read_pickle('image_embeddings.pickle')

MODEL_NAME = 'ViT-B-32'
PRETRAINED_SOURCE = 'openai'
model, _, preprocess = create_model_and_transforms(MODEL_NAME, pretrained=PRETRAINED_SOURCE)
tokenizer = get_tokenizer(MODEL_NAME)
model.eval()

# Already completed for you
def load_images(image_dir, max_images=None, target_size=(224, 224)):
    images = []
    image_names = []
    for i, filename in enumerate(os.listdir(image_dir)):
        if filename.endswith('.jpg'):
            img = Image.open(os.path.join(image_dir, filename))
            img = img.convert('L')  # Convert to grayscale ('L' mode)
            img = img.resize(target_size)  # Resize to target size
            img_array = np.asarray(img, dtype=np.float32) / 255.0  # Normalize pixel values to [0, 1]
            images.append(img_array.flatten())  # Flatten to 1D
            image_names.append(filename)
        if max_images and i + 1 >= max_images:
            break
    return np.array(images), image_names

train_images, train_image_names = load_images(file_path, max_images=2000, target_size=(224, 224)) # 200 images max
print(f"Loaded {len(train_images)} images for PCA training.")

# Apply PCA
k = 50  # Number of principal components (eg: 50)
pca = PCA(n_components=k) # initialize PCA with no. of components
pca.fit(train_images) 
print(f"Trained PCA on {len(train_images)} samples.")
train_images, train_image_names = load_images(file_path, max_images=10000, target_size=(224, 224)) # 200 images max
images_transformed = pca.transform(train_images)  # Fit PCA on the training subset
print(f"Transformed PCA on {len(train_images)} samples.")

def nearest_neighbors(query_embedding, embeddings, top_k=5):
    # query_embedding: The embedding of the query item (e.g., the query image) in the same dimensional space as the other embeddings.
    # embeddings: The dataset of embeddings that you want to search through for the nearest neighbors.
    # top_k: The number of most similar items (nearest neighbors) to return from the dataset.
    # Hint: flatten the "distances" array for convenience because its size would be (1,N)
    distances = euclidean_distances(query_embedding.reshape(1, -1), embeddings).flatten() # Use euclidean distance
    nearest_indices = np.argsort(distances)[:top_k]  # get the indices of ntop k results
    return nearest_indices, distances[nearest_indices]

def pca_image(image_query):
    impaths = []
    distances = []
    images = []
    image = Image.open(io.BytesIO(image_query.read())) 
    image = image.convert('L')  # Convert to grayscale ('L' mode)
    image = image.resize((224, 224))  # Resize to target size
    img_array = np.asarray(image, dtype=np.float32) / 255.0  # Normalize pixel values to [0, 1]
    image = img_array.flatten()  # Flatten to 1D
    images.append(image)
    query_embeddings = pca.transform(np.array(image).reshape(1, -1))

    top_indices, top_distances = nearest_neighbors(query_embeddings, images_transformed)
    print("Top indices:", top_indices)
    print("Top distances:", top_distances)
    for i, index in enumerate(top_indices):
        impath = df['file_name'].iloc[index]
        similarity = top_distances[i].item()
        impaths.append(impath)
        distances.append(similarity)
        
    return impaths, distances

def embed_image(image_query):
    
    # check if the file is image or not
    if isinstance(image_query, str):
        image = preprocess(Image.open(image_query)).unsqueeze(0)
    else:
        image = Image.open(io.BytesIO(image_query.read())) 
        image = preprocess(image).unsqueeze(0)
        
    image_embedding = F.normalize(model.encode_image(image))
    return image_embedding

def embed_text(text_query):
    tokenizer = get_tokenizer('ViT-B-32')
    model.eval()
    text = tokenizer([text_query])
    text_embedding = F.normalize(model.encode_text(text)) ### encode text
    
    return text_embedding

def embed_hybrid(image_query, text_query, hybrid_weight):
    image_embedding = embed_image(image_query)
    text_embedding = embed_text(text_query)
    
    hybrid_weight = torch.tensor(hybrid_weight, dtype=torch.float32)

    hybrid_embedding = F.normalize(hybrid_weight * text_embedding + (1.0 - hybrid_weight) * image_embedding)

    return hybrid_embedding

def get_top_images(query_embedding):
    impaths = []
    similarities = []
        # Calculate cosine similarities
    cosine_similarities = F.cosine_similarity(query_embedding, torch.tensor(df['embedding'].tolist()))
    print(cosine_similarities)

    # Find the index of the highest similarity
    top_indices = torch.topk(cosine_similarities, 5).indices.tolist()
    
    for index in top_indices:
        impath = df['file_name'].iloc[index]
        similarity = cosine_similarities[index].item()
        impaths.append(impath)
        similarities.append(similarity)
    
    return impaths, similarities