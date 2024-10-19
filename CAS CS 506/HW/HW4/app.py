from flask import Flask, render_template, request, jsonify
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

app = Flask(__name__)


# TODO: Fetch dataset, initialize vectorizer and LSA here
newsgroups = fetch_20newsgroups(subset='all')
documents = newsgroups.data

# Create the Preprocessed Term-Document Matrix using TF-IDF
stop_words = stopwords.words('english')
vectorizer = TfidfVectorizer(stop_words=stop_words)
td_matrix = vectorizer.fit_transform(documents)

# Apply SVD to reduce the dimensionality
svd = TruncatedSVD(n_components=100)  # Initial top 100 dimention 
td_matrix_reduced = svd.fit_transform(td_matrix)

def search_engine(query):
    """
    Function to search for top 5 similar documents given a query
    Input: query (str)
    Output: documents (list), similarities (list), indices (list)
    """
    query_vector = vectorizer.transform([query])
    query_reduced = svd.transform(query_vector)
    
    # Calculate cosine similarity between query and all documents
    similarities = cosine_similarity(query_reduced, td_matrix_reduced).flatten()
    
    # Get top 5 documents based on similarity scores
    top_indices = similarities.argsort()[-5:][::-1] # The highest 5 
    top_documents = [documents[i] for i in top_indices]
    top_similarities = [similarities[i] for i in top_indices]
    
    return top_documents, top_similarities, top_indices

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    documents, similarities, indices = search_engine(query)
    indices = indices.tolist()
    return jsonify({'documents': documents, 'similarities': similarities, 'indices': indices}) 

if __name__ == '__main__':
    app.run(debug=True)
