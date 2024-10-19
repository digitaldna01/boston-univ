## Description
The webpage MUST include the following functionality:

### Initialization Methods:
Random: Centroids are chosen randomly from the data points.
Farthest First: Initial centroids are chosen such that they are farthest apart.
KMeans++: Initialization that ensures the centroids are spread out to accelerate convergence.
Manual: Users will select the initial centroids manually via point-and-click on the visualization.

### Visualization:
Display the data points and centroids on a 2D plot.
Show the clustering process step-by-step, highlighting the data points and centroids assigned to each cluster.
Allow users to manually select centroids and dynamically visualize the clustering process.
Show the final cluster assignments on the plot.

### User Interface:
A drop-down menu for users to select their initialization method.
A button to generate a new random dataset. The dataset should not change when users switch between different initialization methods. Only when the user requests a new dataset should it regenerate.
A button to step through the KMeans steps, allowing the user to watch the algorithm’s progress by clicking this button as it steps through each step of the algorithm.
A button that allows the user to go straight to convergence, completing all steps of the algorithm at once.
A button for users to reset the algorithm and try different initialization methods.