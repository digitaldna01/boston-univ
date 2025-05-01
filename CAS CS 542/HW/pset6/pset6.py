
# %%
import matplotlib.pyplot as plt
import numpy as np

datafile = 'data/ex2data1.txt'

cols = np.loadtxt(datafile, delimiter=',', usecols=(0, 1, 2), unpack=True)  #Read in comma separated data
##Form the usual "X" matrix and "y" vector
X = np.transpose(np.array(cols[:-1]))
y = np.transpose(np.array(cols[-1:]))
m = y.size  # number of training examples
##Insert the usual column of 1's into the "X" matrix
X = np.insert(X, 0, 1, axis=1)

#Divide the sample into two: ones with positive classification, one with null classification
pos = np.array([X[i] for i in range(X.shape[0]) if y[i] == 1])
neg = np.array([X[i] for i in range(X.shape[0]) if y[i] == 0])

def plotData():
    plt.figure(figsize=(10, 6))
    plt.plot(pos[:, 1], pos[:, 2], 'k+', label='Admitted')
    plt.plot(neg[:, 1], neg[:, 2], 'yo', label='Not admitted')
    plt.xlabel('Exam 1 score')
    plt.ylabel('Exam 2 score')
    plt.legend()
    plt.grid(True)

plotData()


# %% [markdown]
# Implement the LDA classifier by completing the code below.
# 
# ### 1.3 Centering the data [5 pts]
# As an implementation detail, you should first center the positive and negative data separately, so that each set has a mean equal to [0, 0], before computing the covariance, as this tends to give a more accurate estimate of the covariance.

# %%
##### IMPLEMENT THIS #######
pos_mean = np.mean(pos[:, 1:], axis=0)
neg_mean = np.mean(neg[:, 1:], axis=0)

pos_data = pos[:, 1:] - pos_mean
neg_data = neg[:, 1:] - neg_mean

# %%
print(np.mean(pos_data, axis=0))
print(np.mean(neg_data, axis=0))

# %% [markdown]
# ### 1.4 Computing parameters and predictions [10 pts]
# Implement the LDA algorithm here in vectorized form (avoid loops). First, compute the covariance matrix, then the classifier's weights, then use the classifier to make predictions on the training data. Note, you should center the whole training data set before applying the classifier. Namely, subtract the mean value of the two classes’ means (1/2*(pos_mean+neg_mean)), which is on the separating plane when their prior probabilities are the same and becomes the ‘center’ of the data.

# %%
X_total_mean = 1/2 * (pos_mean + neg_mean) # shape: (2,)
X_centered = X[:, 1:] - X_total_mean # SHAPE: (100,2)   
pos_mean_centered = (pos_mean - X_total_mean).reshape(2, 1) # SHAPE: (2,1)
neg_mean_centered = (neg_mean - X_total_mean).reshape(2, 1) # SHAPE: (2,1)

cov_all = np.cov(X_centered.T) # SHAPE: (2,2)
inverse_cov = np.linalg.inv(cov_all) # SHAPE: (2,2)

w =  (pos_mean_centered.T - neg_mean_centered.T) @ inverse_cov  # SHAPE: (2,1)
w0 = -1/2 * ( pos_mean_centered.T @ inverse_cov @ pos_mean_centered) + 1/2 * (neg_mean_centered.T @ inverse_cov @ neg_mean_centered ) # SHAPE: (1,)
y_lda = np.where((X_centered @ w.T + w0) < 0, 0, 1 ) # SHAPE: (100,)


# %% [markdown]
# ### 1.5 Training accuracy [5 pts]
# Complete the code to compute the training set accuracy, which should be around 89%.  

# %%
####### IMPLEMENT THIS #########
accuracy = np.mean(y_lda == y) * 100
print(accuracy)

# %% [markdown]
# ### 1.6 Effect of prior [10 pts]
# Try changing the prior probability of the positive class $P(y = 1) = \pi$ and show how the resulting decision boundary changes by plotting it. What is the effect of changing $\pi$ on the boundary?

# %%
# Plot decision boundary for various biases.
# Changing the prior probability of y=1 only affects the bias, specifically the
# term log(p(y=1)/p(y=0)) which is part of the bias term. The effect is to move
# the decision boundary away from the more prevalent class. So if we change pi
# to make class 1 ("+") more prevalent, the bias should increase.

# center the data, split into classes (pos "+"  and neg "o")
X_c = X[:,1:] - np.kron(np.ones((len(X), 1)),(1/2*(pos_mean + neg_mean)))
pos_c = np.array([X_c[i] for i in range(X_c.shape[0]) if y[i] == 1])
neg_c = np.array([X_c[i] for i in range(X_c.shape[0]) if y[i] == 0])

# make a new figure and plot points
plt.figure(figsize=(10, 6))
plt.plot(pos_c[:, 0], pos_c[:, 1], 'k+', label='Admitted')
plt.plot(neg_c[:, 0], neg_c[:, 1], 'yo', label='Not admitted')
plt.xlabel('Exam 1 score')
plt.ylabel('Exam 2 score')
plt.legend()
plt.grid(True)

################### IMPLEMENT THIS ###################################
# Show how the decision boundary changes with prior.
# Plotting the decision boundary: two points, draw a line between them
# Decision boundary occurs when h(x) = 0, ie when
#           w0*x1 + w1*x2 + bias = 0
# So the line y=mx+b is given by x2 = (-1/w1)(bias + w0*x1)
pi = len(pos_c) / len(X_c)
print("pi", pi)
log_odds = np.log(pi / (1 - pi))
print(f"π: {pi:.2f}, log odds: {log_odds:.2f}")
w0_, w1_ = w.flatten()

x1_vals = np.linspace(X_c[:, 0].min(), X_c[:, 0].max(), 100)

bias_0 = 0
bias_2 = 2

# decision boundary: x2 = -(bias + w0 * x1) / w1
x2_vals_bias0 = -(bias_0 + w0_ * x1_vals) / w1_
x2_vals_bias2 = -(bias_2 + w0_ * x1_vals) / w1_

# bias = 0
plt.plot(x1_vals, x2_vals_bias0, color='cornflowerblue', linewidth=8, alpha=0.4, label='bias=0')

# bias = 2
plt.plot(x1_vals, x2_vals_bias2, color='darkblue', linewidth=8, alpha=0.7, label='bias=2')

plt.legend()
plt.show()



import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

alpha = 2
beta_param = 98

theta = np.linspace(0, 1, 1000)
pdf = beta.pdf(theta, alpha, beta_param)

plt.plot(theta, pdf, label=f'Beta({alpha},{beta_param})')
plt.xlabel(r'$\theta$')
plt.ylabel('Density')
plt.title('Prior Beta Distribution for Click Rate')
plt.legend()
plt.grid()
plt.show()

import numpy as np

def posterior(Phi, t, alpha, beta, return_inverse=False):
    """Computes mean and covariance matrix of the posterior distribution."""
    S_N = np.linalg.inv(alpha * np.eye(Phi.shape[1]) + beta * Phi.T @ Phi)
    S_N_inv = np.linalg.inv(S_N)
    m_N = beta * S_N @ Phi.T @ t

    if return_inverse:
        return m_N, S_N, S_N_inv
    else:
        return m_N, S_N


def posterior_predictive(Phi_test, m_N, S_N, beta):
    """Computes mean and variances of the posterior predictive distribution."""
    y = Phi_test @ m_N
    y_var = 1 / beta + np.sum(Phi_test @ S_N * Phi_test, axis=1)

    return y, y_var

# %%
w0 = -0.3  # line offset
w1 =  0.5  # line slope

def f(X, noise_variance):
    '''Linear function plus noise'''
    noise_val = noise(X.shape[0], noise_variance).reshape(-1, 1)
    t = w1 * X + w0 + noise_val

    return t

def noise(size, variance):
    return np.random.normal(scale=np.sqrt(variance), size=size)

# %% [markdown]
# ### 3.3 Basis functions [5pts]
# For straight line fitting, we do not need to transform $x$ with a basis function, which is equivalent to using an identity basis function. Other basis functions that are non-linear are necessary to model the non-linear relationship between input $x$ and target $t$. Below is an example of non-linear basis functions: the polynomial. Implement the polynomial basis function. *Note: You will not use it in the rest of the exercise but your implementation should be reasonable.*

# %%
def identity_basis_function(x):
    return x


def polynomial_basis_function(x, power):
    polynomial_x = np.hstack([x**p for p in range(power + 1)]) # each data degree upto 1 to power
    return polynomial_x


def expand(x, bf, bf_args=None):
    if bf_args is None:
        return np.concatenate([np.ones(x.shape), bf(x)], axis=1)
    else:
        return np.concatenate([np.ones(x.shape)] + [bf(x, bf_arg) for bf_arg in bf_args], axis=1)

# %%
from scipy import stats
import matplotlib.pyplot as plt

def plot_data(x, t):
    plt.scatter(x, t, marker='o', c="k", s=20)


def plot_truth(x, y, label='Truth'):
    plt.plot(x, y, 'k--', label=label)


def plot_predictive(x, y, std, y_label='Prediction', std_label='Uncertainty', plot_xy_labels=True):
    y = y.ravel()
    std = std.ravel()

    plt.plot(x, y, label=y_label)
    plt.fill_between(x.ravel(), y + std, y - std, alpha = 0.5, label=std_label)

    if plot_xy_labels:
        plt.xlabel('x')
        plt.ylabel('y')


def plot_posterior_samples(x, ys, plot_xy_labels=True):
    plt.plot(x, ys[:, 0], 'r-', alpha=0.5, label='Post. samples')
    for i in range(1, ys.shape[1]):
        plt.plot(x, ys[:, i], 'r-', alpha=0.5)

    if plot_xy_labels:
        plt.xlabel('x')
        plt.ylabel('y')


def plot_posterior(mean, cov, w0, w1):
    resolution = 100

    grid_x = grid_y = np.linspace(-1, 1, resolution)
    grid_flat = np.dstack(np.meshgrid(grid_x, grid_y)).reshape(-1, 2)

    densities = stats.multivariate_normal.pdf(grid_flat, mean=mean.ravel(), cov=cov).reshape(resolution, resolution)
    plt.imshow(densities, origin='lower', extent=(-1, 1, -1, 1))
    plt.scatter(w0, w1, marker='x', c="r", s=20, label='Truth')

    plt.xlabel('w0')
    plt.ylabel('w1')


def print_comparison(title, a, b, a_prefix='np', b_prefix='br'):
    print(title)
    print('-' * len(title))
    print(f'{a_prefix}:', a)
    print(f'{b_prefix}:', b)
    print()

# %%
import matplotlib.pyplot as plt


# fix random seed so we always get the same data
np.random.seed(5)

# Training dataset sizes
N_list = [1, 3, 20]

beta = 25.0
alpha = 2.0

# Training observations in [-1, 1)
X = np.random.rand(N_list[-1], 1) * 2 - 1

# Training target values
t = f(X, noise_variance=1/beta)

# Test observations
X_test = np.linspace(-1, 1, 100).reshape(-1, 1)

# Function values without noise
y_true = f(X_test, noise_variance=0)

# Design matrix of test observations
Phi_test = expand(X_test, identity_basis_function)

plt.figure(figsize=(15, 10))
plt.subplots_adjust(hspace=0.4)

for i, N in enumerate(N_list):
    X_N = X[:N]
    t_N = t[:N]

    # Design matrix of training observations
    Phi_N = expand(X_N, identity_basis_function)

    # Mean and covariance matrix of posterior
    m_N, S_N = posterior(Phi_N, t_N, alpha, beta)

    # Mean and variances of posterior predictive
    y, y_var = posterior_predictive(Phi_test, m_N, S_N, beta)

    # Draw 5 random weight samples from posterior and compute y values
    w_samples = np.random.multivariate_normal(m_N.ravel(), S_N, 5).T
    y_samples = Phi_test.dot(w_samples)

    plt.subplot(len(N_list), 3, i * 3 + 1)
    plot_posterior(m_N, S_N, w0, w1)
    plt.title(f'Posterior density (N = {N})')
    plt.legend()

    plt.subplot(len(N_list), 3, i * 3 + 2)
    plot_data(X_N, t_N)
    plot_truth(X_test, y_true)
    plot_posterior_samples(X_test, y_samples)
    plt.ylim(-1.5, 1.0)
    plt.legend()

    plt.subplot(len(N_list), 3, i * 3 + 3)
    plot_data(X_N, t_N)
    plot_truth(X_test, y_true, label=None)
    plot_predictive(X_test, y, np.sqrt(y_var))
    plt.ylim(-1.5, 1.0)
    plt.legend()

# %%
def g(X, noise_variance):
    '''Sinusoidial function plus noise'''
    return 0.5 + np.sin(2 * np.pi * X) + noise(X.shape, noise_variance)

def gaussian_basis_function(x, mu, sigma=0.1):
    return np.exp(-0.5 * ((x - mu) / sigma) ** 2)

# %%
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit

# fix random seed so we always get the same data
np.random.seed(5)

N_list = [3, 8, 20]

beta = 25.0
alpha = 2.0

# Training observations in [-1, 1)
X = np.random.rand(N_list[-1], 1)

# Training target values
t = g(X, noise_variance=1/beta)

# Test observations
X_test = np.linspace(0, 1, 100).reshape(-1, 1)

# Function values without noise
y_true = g(X_test, noise_variance=0)

# Design matrix of test observations
Phi_test = expand(X_test, bf=gaussian_basis_function, bf_args=np.linspace(0, 1, 7))

plt.figure(figsize=(10, 10))
plt.subplots_adjust(hspace=0.4)

for i, N in enumerate(N_list):
    X_N = X[:N]
    t_N = t[:N]

    # Design matrix of training observations
    Phi_N = expand(X_N, bf=gaussian_basis_function, bf_args=np.linspace(0, 1, 7))

    # Mean and covariance matrix of posterior
    m_N, S_N = posterior(Phi_N, t_N, alpha, beta)

    # Mean and variances of posterior predictive
    y, y_var = posterior_predictive(Phi_test, m_N, S_N, beta)

    # Draw 5 random weight samples from posterior and compute y values
    w_samples = np.random.multivariate_normal(m_N.ravel(), S_N, 5).T
    y_samples = Phi_test.dot(w_samples)

    plt.subplot(len(N_list), 2, i * 2 + 1)
    plot_data(X_N, t_N)
    plot_truth(X_test, y_true)
    plot_posterior_samples(X_test, y_samples)
    plt.ylim(-1.0, 2.0)
    plt.legend()

    plt.subplot(len(N_list), 2, i * 2 + 2)
    plot_data(X_N, t_N)
    plot_truth(X_test, y_true, label=None)
    plot_predictive(X_test, y, np.sqrt(y_var))
    plt.ylim(-1.0, 2.0)
    plt.legend()


# %% [markdown]
# ### 4.0 Install dependencies

# %%
# !pip install gym==0.25.2
# !pip install pygame
# !pip install numpy

# %% [markdown]
# ### 4.1. Walking on the Frozen Lake [5 points]
# 
# The script below sets up the Frozen Lake environment and takes 10 walks through it, consisting of a maximum 10 randomly sampled actions during each walk. After each step, it prints the current state id, and prints out the reward and whether the walk is "done", i.e. in the terminal state, because the agent fell into a hole (stop if it is).
# 
# The environment behaves in a stochastic way, i.e. taking an action does not  deterministically transition the agent into the next state. Instead the agent ends up in one of several states with some probability. The analogy here is that when you try to walk right on ice, you may slip and end up walking forward, etc.
# 
# Run the script and make sure you understand the behavior of the agent. Is it easy for the agent to reach the goal while taking random actions? Read the code to understand what it's doing (there is nothing to implement for this part).

# %%
import numpy as np
import gym

# %%
#env = gym.make("FrozenLake-v1", map_name="4x4", is_slippery=False)
env =gym.make("FrozenLake-v1", new_step_api=True).unwrapped
np.random.seed(42)
actions = ["LEFT", "DOWN", "RIGHT", "UP"]

# Do a random walk
for i in range(2):
  env.reset()
  print("Walk %d" % i)
  for _ in range(10):
    # env.render() # note, this does not work in Colab
    action = env.action_space.sample()
    next_state, reward, done, info, prob = env.step(action) # take a random action
    print("Action %s \t State %d Reward %d done? %d" % (actions[action], next_state, reward, done))
  env.close()


# %% [markdown]
# ### 4.2 Q-Learning Implementation [20 points]
# Below we have provided most of the code to solve the  FrozenLake problem, including setting up the Gym environment,
# calling the Q-learning function, and printing out the returned Q-table. <br>
# 
# **Your task** is to understand the provided code and fill in the missing part. Run the code, provide​ ​the​ ​final​ ​Q-table​ ​of​ ​​FrozenLake for **each <num_episode, init_method>** tried,​ ​and analyze ​what​ you observe.
# 
# #### Notes
# We use the $\epsilon$-greedy algorithm (solving Exploration-Exploitation Dilemma) to generate actions for each state. The code tries `num_episodes` with different values, e.g. `num_episodes=500, 1000, 5000, 10000, 50000`. It also tries different initializations for the Q-table, i.e. Random Initialization and Zero Initialization.
# 
# Please do not change any default value of environment setting, such as `is_slippery`.
# 
# To test the learned Q-table, we can compute the win rate (the probability of agents getting to goal following the Q-table). Note that in this case, we should use `argmax` instead of epsilon greedy to choose the action at the current state. Win Rate is a good way to test whether you write your algorithm correctly.
# 
# Just for your reference, we tested our implementation several times with 1000 trials after 50000-episode training using zero initialization, and were able to achieve a win rate of 0.5 or higher on several of the trials.
# 
# 

# %%
# whether to initialize Q-table randomly
RAND = False

"""   Performs   Q-learning   for   the   given   environment.
Initialize Q to all zeros or randomly.
:param   env:   Unwrapped   OpenAI   gym   environment.
:param   alpha:   Learning   rate   parameter.
:param   gamma:   Decay   rate   parameter.
:param   num_episodes:   Number   of   episodes   to   use   for   learning. :return:   Q   table.
"""
def q_learning(env, alpha=0.5, gamma=0.95, epsilon=0.1, num_episodes=500):
    np.random.seed(42)
    # initialize Q
    state_num = env.observation_space.n
    action_num = env.action_space.n
    Q = np.zeros((state_num, action_num))

    if RAND:
        Q = np.random.rand(state_num, action_num)
        terminal_state = [5, 7, 11, 12, 15]
        Q[terminal_state, :] = 0

    for episode in range(num_episodes):
        current_state = env.reset() # reset() returns observation, reward,terminated, truncated, info, done
        done = False
        while not done:
            if np.random.rand() < 1- epsilon:
                action = np.argmax(Q[current_state,:])
            else:
                action = np.random.randint(0,action_num)

            # IMPLEMENT THIS (see lecture notes for pseudocode):
            #  - carry out selected action
            #  - observe reward and new state
            #  - update the Q table
            #  - update current state to new state

            # carry out selected action
            next_state, reward, done, info, prob = env.step(action)

            # update Q table
            Q[current_state, action] = Q[current_state, action] + alpha * ( reward + gamma * np.max(Q[next_state, :]) - Q[current_state, action] ) 

            # update current state
            current_state = next_state

    return Q

def winrate(Q, env, num_episodes):
    num_win = 0.

    for episode in range(num_episodes):
        current_state = env.reset()
        done = False
        while not done:
            action = np.argmax(Q[current_state, :])
            next_state, reward, done, info, prob = env.step(action)
            num_win += reward
            current_state = next_state

    return num_win/num_episodes

# MAIN function that runs Q-learning for Frozen Lake
def main():
    env = gym.make("FrozenLake-v1", new_step_api=True).unwrapped
    np.random.seed(42)
    
    print("output of Q-learning")
    num_episodes = [ 500, 1000, 5000, 10000, 50000]
    for num in num_episodes:
        print("num_episodes: ", num)
        Q = q_learning(env, num_episodes=num)
        print("Q: ", Q)
        print("Win rate: ", winrate(Q, env, num_episodes=(num // 50)))
        
    # Q = q_learning(env, num_episodes=50000)
    # print("Q: ", Q)
    # print("Win rate: ", winrate(Q, env, num_episodes=1000))

if __name__ == "__main__":
    main()

# %% [markdown]
# In this Q-learning implementation on the frozen environment, I observed a clear relationship between the number of training episodes and the agent’s learning performance. When trained with a small number of episodes (500 to 10,000), the Q-table remained mostly unchanged with values close to zero, and the agent failed to achieve any successful episodes, resulting in a win rate of 0.0. This suggests that the agent did not explore enough or receive sufficient positive rewards to learn effective state-action values, which is particularly challenging in FrozenLake due to its stochastic nature (is_slippery=True). However, when the number of episodes was increased to 50,000, the Q-table began to reflect meaningful learning, especially in states closer to the goal, and the win rate significantly improved to 0.812. This demonstrates that Q-learning in such environments requires extensive exploration and a large number of episodes for the agent to converge to a useful policy. The results also highlight the importance of the ε-greedy strategy for maintaining exploration over time, as well as the limitations of zero initialization when not paired with sufficient training. Overall, the experiment emphasizes the necessity of long training durations for reinforcement learning agents to succeed in highly uncertain environments like FrozenLake.


