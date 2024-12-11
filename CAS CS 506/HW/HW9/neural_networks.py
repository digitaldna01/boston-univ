import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.animation import FuncAnimation
import os
from functools import partial
from matplotlib.patches import Circle

result_dir = "results"
os.makedirs(result_dir, exist_ok=True)

# Define a simple MLP class
class MLP:
    # def __init__(self, input_dim=2, hidden_dim=3, output_dim=1, lr=lr, activation='tanh'):
    def __init__(self, input_dim, hidden_dim, output_dim, lr, activation):
        np.random.seed(0)
        self.lr = lr # learning rate
        self.activation_fn = activation # activation function
        self.W1 = np.random.randn(input_dim, hidden_dim) / np.sqrt(input_dim) # Input to hidden layer weights
        self.W2 = np.random.randn(hidden_dim, output_dim) / np.sqrt(hidden_dim) # hidden to output layer weights
        self.B1 = np.zeros((1, hidden_dim)) # Hidden layer bias
        self.B2 = np.zeros((1, output_dim)) # Output layer bias
        
        self.a1 = None
        self.out = None

    def forward(self, X):
        # TODO: forward pass, apply layers to input X
        self.z1 = np.dot(X, self.W1) + self.B1
        self.a1 = self.activate(self.z1) # Activation function
        self.z2 = np.dot(self.a1, self.W2) +self.B2
        # TODO: store activations for visualization
        self.out = self.z2
        return self.out

    def backward(self, X, y):
        # TODO: compute gradients using chain rule
        m = y.shape[0] # Number of samples
        dz2 =  2 * (self.out - y) / m # Gradient of loss w.r.t W2
        dW2 = np.dot(self.a1.T, dz2)  # Gradient w.r.t W2
        db2 = np.sum(dz2, axis=0, keepdims=True) # Gradient w.r.t b2
        
        dz1 = np.dot(dz2, self.W2.T) * self.activate_derivative(self.a1)
        dW1 = np.dot(X.T, dz1) / m # Gradient w.r.t W1
        db1 = np.sum(dz1, axis=0, keepdims=True) 

        # TODO: update weights with gradient descent
        self.W1 -= self.lr * dW1
        self.B1 -= self.lr * db1
        self.W2 -= self.lr * dW2
        self.B2 -= self.lr * db2

        # TODO: store gradients for visualization
        self.dW1 = dW1
        self.db1 = db1
        self.dW2 = dW2
        self.db2 = db2
        
        self.gradients = {
            'dW1' : self.dW1,
            'db2' : self.db2,
            'dW2' : self.dW2,
            'db1' : self.db1
        }
        return self.gradients
    
    def activate(self, z):
        if self.activation_fn == 'relu':
            return self.relu(z)
        elif self.activation_fn == 'tanh':
            return self.tanh(z)
        else:
            return self.sigmoid(z)
        
    def activate_derivative(self, a):
        if self.activation_fn == 'relu':
            return self.relu_derivative(a)
        elif self.activation_fn == 'tanh':
            return self.tanh_derivative(a)
        else:
            return self.sigmoid_derivative(a)
    
    def relu(self, z):
        return np.maximum(0, z) 
    
    def relu_derivative(self, a):
        return (a > 0).astype(float) # if a is bigger than 0 then 1, or return 0
    
    def tanh(self, z):
        return np.tanh(z)
    
    def tanh_derivative(self, a):
        return 1 - np.tanh(a) ** 2 # derivative of tanh: 1 - tanh^2(a)
    
    def sigmoid(self, z):
        return 1 / (1 + np.exp(-z))
    
    def sigmoid_derivative(self, a):
        return a * (1 - a) # derivative of sigmoid : a * (1 - a)
    
# Generate Circular Data
def generate_data(n_samples=100):
    np.random.seed(0)
    # Generate input
    # Random generate data
    X = np.random.randn(n_samples, 2)
    y = (X[:, 0] ** 2 + X[:, 1] ** 2 > 1).astype(int) * 2 - 1  # Circular boundary
    y = y.reshape(-1, 1)
    return X, y

# Visualization update function
def update(frame, mlp, ax_input, ax_hidden, ax_gradient, X, y):
    ax_hidden.clear()
    ax_input.clear()
    ax_gradient.clear()

    # perform training steps by calling forward and backward function
    for _ in range(10):
        # Perform a training step
        mlp.forward(X)
        mlp.backward(X, y)
        
    # TODO: Plot hidden features hidden space 1, 2, 3 다 그렸어
    hidden_features = mlp.a1 
    
    # TODO: Hyperplane visualization in the hidden space
    x_min, x_max = hidden_features[:, 0].min()-0.5, hidden_features[:, 0].max() +0.5
    y_min, y_max = hidden_features[:, 1].min()-0.5, hidden_features[:, 1].max() +0.5
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100), np.linspace(y_min, y_max, 100))
    Z = -(mlp.W2[0, 0] * xx + mlp.W2[1, 0] * yy + mlp.B2[0]) / mlp.W2[2, 0]
    ax_hidden.plot_surface(xx, yy, Z, color='green', alpha=0.7)  # 초평면을 반투명하게 설정

    # # TODO: Distorted input space transformed by the hidden layer
    xx = np.linspace(X[:, 0].min(), X[:, 0].max(), 100)
    yy = np.linspace(X[:, 1].min(), X[:, 1].max(), 100)
    X_g, Y_g = np.meshgrid(xx, yy)
    g_points = np.c_[X_g.ravel(), Y_g.ravel()]
    
    hidden_transformed = mlp.activate(np.dot(g_points, mlp.W1) + mlp.B1)
    ax_hidden.plot_trisurf(hidden_transformed[:, 0], hidden_transformed[:, 1], hidden_transformed[:,2], color='lightblue', alpha=0.5, linewidth=0.2)

    ax_hidden.scatter(hidden_features[:, 0], hidden_features[:, 1], hidden_features[:, 2], c=y.ravel(), cmap='bwr', alpha=1)
    ax_hidden.set_title(f"Hidden Space at Step {frame * 10}")
    ax_hidden.set_xlabel("Transformed Feature 1")
    ax_hidden.set_ylabel("Transformed Feature 2")
    ax_hidden.set_zlabel("Hidden Feature 3")
    # ax_hidden.set_xlim(-1.5, 1.5)
    # ax_hidden.set_ylim(-1.5, 1.5)
    # ax_hidden.set_zlim(-1.5, 1.5)

    # # TODO: Plot input layer decision boundary
    ax_input.scatter(X[:, 0], X[:, 1], c=y.ravel(), cmap='bwr', alpha=1, edgecolor='k')
    ax_input.set_title(f"Input Space at Step {frame * 10}")
    
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100), np.linspace(y_min, y_max, 100))
    
    grid_input = np.c_[xx.ravel(), yy.ravel()]
    grid_output_input = mlp.forward(grid_input).reshape(xx.shape)

    ax_input.contourf(xx, yy, grid_output_input,  alpha=0.5, cmap='coolwarm')
    ax_input.contour(xx, yy, grid_output_input, levels=[0], colors='black')  # 결정 경계 추가

    # TODO: Visualize features and gradients as circles and edges 
    ax_gradient.add_patch(Circle((0.0, 0.0), 0.05, color='blue'))  # x1
    ax_gradient.text(0.0, 0.0, "x1", fontsize=12, ha='center', color='white')

    ax_gradient.add_patch(Circle((0.0, 1.0), 0.05, color='blue'))  # x2
    ax_gradient.text(0.0, 1.0, "x2", fontsize=12, ha='center', color='white')

    ax_gradient.add_patch(Circle((0.5, 0.0), 0.05, color='blue'))  # h1
    ax_gradient.text(0.5, 0.0, "h1", fontsize=12, ha='center', color='white')

    ax_gradient.add_patch(Circle((0.5, 0.5), 0.05, color='blue'))  # h2
    ax_gradient.text(0.5, 0.5, "h2", fontsize=12, ha='center', color='white')

    ax_gradient.add_patch(Circle((0.5, 1.0), 0.05, color='blue'))  # h3
    ax_gradient.text(0.5, 1.0, "h3", fontsize=12, ha='center', color='white')

    ax_gradient.add_patch(Circle((1.0, 0.0), 0.05, color='blue'))  # y
    ax_gradient.text(1.0, 0.0, "y", fontsize=12, ha='center', color='white')

    # Draw connections with varying thickness based on gradients
    # x1 to h1, h2, h3

    ax_gradient.plot([0.0, 0.5], [0.0, 0.0], color='purple', linewidth=np.abs(mlp.gradients['dW1'][0][0]) * 100)  # x1 to h1
    ax_gradient.plot([0.0, 0.5], [1.0, 0.5], color='purple', linewidth=np.abs(mlp.gradients['dW1'][1][0]) * 100)  # x2 to h1
    ax_gradient.plot([0.0, 0.5], [0.0, 0.5], color='purple', linewidth=np.abs(mlp.gradients['dW1'][0][1]) * 100)  # x1 to h2
    ax_gradient.plot([0.0, 0.5], [1.0, 0.5], color='purple', linewidth=np.abs(mlp.gradients['dW1'][1][1]) * 100)  # x2 to h2
    ax_gradient.plot([0.0, 0.5], [0.0, 1.0], color='purple', linewidth=np.abs(mlp.gradients['dW1'][0][2]) * 100)  # x1 to h3
    ax_gradient.plot([0.0, 0.5], [1.0, 1.0], color='purple', linewidth=np.abs(mlp.gradients['dW1'][1][2]) * 100)  # x2 to h3
    # h1, h2, h3 to y
    ax_gradient.plot([0.5, 1.0], [0.0, 0.0], color='purple', linewidth=np.abs(mlp.gradients['dW2'][0][0]) * 100)  # h1 to y
    ax_gradient.plot([0.5, 1.0], [0.5, 0.0], color='purple', linewidth=np.abs(mlp.gradients['dW2'][1][0]) * 100)  # h2 to y
    ax_gradient.plot([0.5, 1.0], [1.0, 0.0], color='purple', linewidth=np.abs(mlp.gradients['dW2'][2][0]) * 100)  # h3 to y

    ax_gradient.set_title(f"Gradients at Step {frame * 10}")
    ax_gradient.set_xlim(-0.1, 1.1)
    ax_gradient.set_ylim(-0.1, 1.1)
    
    # The edge thickness visually represents the magnitude of the gradient


def visualize(activation, lr, step_num):
    X, y = generate_data()
    mlp = MLP(input_dim=2, hidden_dim=3, output_dim=1, lr=lr, activation=activation)

    # Set up visualization
    matplotlib.use('agg')
    fig = plt.figure(figsize=(21, 7))
    ax_hidden = fig.add_subplot(131, projection='3d')
    ax_input = fig.add_subplot(132)
    ax_gradient = fig.add_subplot(133)

    # Create animation
    ani = FuncAnimation(fig, partial(update, mlp=mlp, ax_input=ax_input, ax_hidden=ax_hidden, ax_gradient=ax_gradient, X=X, y=y), frames=step_num//10, repeat=False)

    # Save the animation as a GIF
    ani.save(os.path.join(result_dir, "visualize.gif"), writer='pillow', fps=10)
    plt.close()

if __name__ == "__main__":
    activation = "tanh"
    lr = 0.1
    step_num = 1000
    visualize(activation, lr, step_num)