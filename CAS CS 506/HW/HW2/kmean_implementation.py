import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

### Generate Dataset
# All Data points are 2D plot
def generate_dataset(num_points):
    # Generate Random Data points between 0 - 1
    random_points = np.random.rand(num_points, 2) * 10  # 10x10 range random points
    return random_points

def initial_capture(data):
    plt.figure(figsize=(8, 6))
    plt.scatter(data[:, 0], data[:, 1], c='blue', alpha=0.6)
    plt.title('KMeans Clustering Data')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.grid()
    plt.savefig('static/initial_visualization.png')  # 이미지를 static 폴더에 저장
    plt.close()

def manual_center_pick():
    pass

# Kmean Class
class KMeans():
    
    def __init__(self, data, k):
        self.data = data
        self.k = k
        self.assignment = [-1 for _ in range(len(data))]
        # gif generate
        self.snaps = []
    
    ### Initialization Methods:

    #Random: Centroids are chosen randomly from the data points.
    def random(self):
        return self.data[np.random.choice(len(self.data) - 1, size=self.k, replace=False)]
    
    # Farthest First: Initial centroids are chosen such that they are farthest apart.
    def farthest_first(self):
        # get the first centroids randomly
        centroids = [self.data[np.random.randint(0, len(self.data))]]
        
        # Get the next k-1 sentroids
        while len(centroids) < self.k:
            distances = np.array([min(np.linalg.norm(point - centroid) for centroid in centroids) for point in self.data])
            
            # Select the farthes one as a next centroid
            next_centroid = self.data[np.argmax(distances)]
            centroids.append(next_centroid)
    
        return np.array(centroids)
        
    # KMeans++: Initialization that ensures the centroids are spread out to accelerate convergence.
    def kmean_plus(self):
        # get the first centroids randomly
        centroids = [self.data[np.random.randint(0, len(self.data))]]
        
        # the next k-1 sentroids
        for _ in range(1, self.k):
            # Get the distance square to each centroids from all points D(x)^2
            distances = np.array([min(np.linalg.norm(point - centroid) ** 2 for centroid in centroids) for point in self.data])
            
            # get the next centroids depends on the probability of the distance 
            probabilities = distances / distances.sum()
            
            # Cumulative Probabilites
            cumulative_probabilities = np.cumsum(probabilities)
            
            # 누적 확률 분포를 이용하여 랜덤으로 다음 중심점을 선택
            r = np.random.rand()
            next_centroid_idx = np.where(cumulative_probabilities >= r)[0][0]
            centroids.append(self.data[next_centroid_idx])
        
        return np.array(centroids)
    
    def manual(self):
        pass


    #### KMEAN Algoritm Helper Function
    
    # Check if the data point is not assigned 
    def isunassigned(self, i):
        return self.assignment[i] == -1
    
    # Computet the distance between two points
    def dist(self, x, y):
        # Euclidean distance
        return sum((x - y)**2) ** (1/2)

    # Make a new clusters
    def make_clusters(self, centers):
        for points_index in range(len(self.assignment)):
            for center_index in range(self.k):
                if self.isunassigned(points_index):
                    self.assignment[points_index] = center_index
                    dist = self.dist(centers[center_index], self.data[points_index])
                else:
                    new_dist = self.dist(centers[center_index], self.data[points_index])
                    if new_dist < dist:
                        self.assignment[points_index] = center_index
                        dist = new_dist
                        
    def compute_centers(self):
        centers = []
        for center_index in range(self.k):
            cluster = []
            for points_index in range(len(self.assignment)):
                # Check if the current point index is assigned to current center index
                if self.assignment[points_index] == center_index:
                    cluster.append(self.data[points_index])
            centers.append(np.mean(np.array(cluster), axis=0))

        return np.array(centers)

    # Check the new centers and previous centers are the same == "converged"
    def not_converged(self, centers, new_centers):
        for center_index in range(self.k):
            if self.dist(centers[center_index], new_centers[center_index]) != 0:
                return True
        return False
    
    # Reset self.assignment function
    def reset_cluster(self):
        self.assignment = [-1 for _ in range(len(self.data))]
    
    ### KMEAN ALGORITHM
    def lloyds(self, initialized):
        self.snaps = []
        step = 0
        # Initialize the Data
        if (initialized == "random"):
            centers = self.random()
        elif (initialized == 'farthest_first'):
            centers = self.farthest_first()
        elif (initialized == 'kmean_plus'):
            centers = self.kmean_plus()
        else:
            centers = self.random()
        self.capture(centers, step)
        # Manual: Users will select the initial centroids manually via point-and-click on the visualization.
        #TODO need to figure out how to click it.
        # First Clusters
        #TODO how to prints out different color
        self.make_clusters(centers)
        new_centers = self.compute_centers()
        #TODO Step trought kmean 버튼 누르면 여기서 보여줘야해 어쩌먀 self.snaps[0]
        step +=1
        self.capture(new_centers, step)
        while self.not_converged(centers, new_centers):
            self.reset_cluster()
            centers = new_centers
            self.make_clusters(centers)
            new_centers = self.compute_centers()
            step += 1
            self.capture(new_centers, step)
        return step

    ### Visualize Method 
    def capture(self, centers, output):

        plt.figure(figsize=(8, 6))
    
        # Assuming self.data contains the data points and self.labels contains cluster assignments
        plt.scatter(self.data[:, 0], self.data[:, 1], c=self.assignment, alpha=0.6, cmap='viridis')  # Color by cluster

        # Plot the centers with a different color and size
        plt.scatter(centers[:, 0], centers[:, 1], c='red', marker='X', s=200, label='Centroids')  # Centroids

        plt.title(f'KMeans Clustering Step {output}')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.grid()
        plt.legend()
        
        plt.savefig(f'static/step_images/step_{output}.png')
        plt.close()
        
    def manual_lloyds(self, selected_points):
        self.snaps = []
        step = 0
        # Initialize the Data
        centers = np.array([[point['x'], point['y']] for point in selected_points])
        self.capture(centers, step)
        self.make_clusters(centers)
        new_centers = self.compute_centers()
        #TODO Step trought kmean 버튼 누르면 여기서 보여줘야해 어쩌먀 self.snaps[0]
        step +=1
        self.capture(new_centers, step)
        while self.not_converged(centers, new_centers):
            self.reset_cluster()
            centers = new_centers
            self.make_clusters(centers)
            new_centers = self.compute_centers()
            step += 1
            self.capture(new_centers, step)
        return step


# kmean = KMeans(data, 4)
# kmean.lloyds("random")
# images = kmean.snaps
# images[0].save(
#     'kmeans_random.gif',
#     optimize=False,
#     save_all=True,
#     append_images=images[1:],
#     loop=0,
#     duration=500
# )




# # 데이터 시각화
# plt.scatter(X[:, 0], X[:, 1], c=y, cmap='viridis')
# plt.scatter(random_centers[:, 0], random_centers[:, 1], c='red', marker='X', s=100, label='Centers')
# plt.title("Generated Blobs with User-defined Random Centers")
# plt.xlabel("Feature 1")
# plt.ylabel("Feature 2")
# plt.legend()
# plt.show()


