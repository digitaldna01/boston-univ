# %% [markdown]
# # Lab 7
# 
# In this lab, we will learn how RANdom SAmple Consensus (RANSAC) algorithm works, and apply RANSAC to solve a linear regression algorithm.

# %% [markdown]
# Let's download the dataset by running the command below:

# %%
# !wget https://hands-on.cloud/wp-content/uploads/2022/04/RANSAC_dataset.csv
# !wget https://raw.githubusercontent.com/krishnaik06/simple-Linear-Regression/refs/heads/master/Salary_Data.csv

# %% [markdown]
# This dataset contains the number of hours athletes spend training, and the score they get in a competition.

# %%
import pandas as pd

# read the dataset
data = pd.read_csv("Salary_Data.csv")
data.head()

# %%
import matplotlib.pyplot as plt

# visialize the data points
# plt.scatter(data['Hours'],data['Score'])
plt.scatter(data['YearsExperience'],data['Salary'])
plt.show()

# %%
import scipy

def linear_fitting(xs,ys):
     """
     Compute the slope and intercept of a linear model given xs and ys.

     :param xs: x coordinates of the data points.
     :param ys: y coordinates of the data points.

     :return k,b: k is the estimated slope and b is the intercept.
     """
     assert len(xs)==len(ys)>=2, print("Require at least two points!")

     # Hint: check scipy.stats.linregress
     result = scipy.stats.linregress(xs, ys)
     k, b = result.slope, result.intercept
     return k, b

# %%
import numpy as np

def evaluate(xs,true_ys,k,b,inlier_thresh=0.1):
     """
     Evaluate the estimated slope and intercept by counting the number of inliers.
     If the distance between a prediceted y and its true y is whithin a threshold,
     we count it as an inlier.

     :param xs: x coordinates of the data points.
     :param true_ys: y coordinates of the data points.
     :param k: estimated slope
     :param b: estimated intercept
     :param inlier_thresh: the threshold of inliers

     :return: number of inliers
     """
     pred_ys = k*xs + b  # predict the y^
     num_inliers = np.sum(np.abs(pred_ys - true_ys) <= inlier_thresh)
     return num_inliers

# %%
def RANSAC(xs, ys, max_iters=100, min_inliers=10):
    """
     Apply RANSAC to solve a linear regression model given data xs and ys.

     :param xs: x coordinates of the data points.
     :param ys: y coordinates of the data points.
     :param max_iters: maximum number of iterations.
     :param min_inliers: minimum number of inliers.

     :return (k,b), best_num_inliers: k is the estimated slope and b is the intercept. best_num_inliers is the
     number of inliers of the ransac model .
     """
    assert len(xs)==len(ys)

    best_num_inliers = 0
    best_k = best_b = 0
    num_points = len(xs)

    for _ in range(max_iters):

      # choose random points from the data
      arr = np.random.choice(num_points, min_inliers, replace=False)
      # index = xs[arr], ys[arr]
      sampled_x, sampled_y = xs[arr], ys[arr]

      # compute a linear regression model using the chosen data points
      k, b = linear_fitting(sampled_x, sampled_y)

      # obtain the number of inliers
      num_inliers = evaluate(sampled_x, sampled_y, k, b)

      # picke the best k, b and number of inliers
      if (best_num_inliers < num_inliers):
        best_num_inliers = num_inliers
        best_k = k
        best_b = b

    return (best_k, best_b), best_num_inliers

# %% [markdown]
# ## Adding Normalize Function

# %%
def normalize_data_zscore(xs, ys):
    """
    Normalize the data using Z-score normalization.

    :param xs: x coordinates of the data points (NumPy array).
    :param ys: y coordinates of the data points (NumPy array).
    :return: Normalized xs and ys (NumPy arrays).
    """
    # Z-score Normalization: x' = (x - mean) / std
    xs_norm = (xs - np.mean(xs)) / np.std(xs)
    ys_norm = (ys - np.mean(ys)) / np.std(ys)

    return xs_norm, ys_norm

# %%
np.random.seed(123)

xs = data['YearsExperience'].values
ys = np.log(data['Salary'].values)

# norm_xs, norm_ys = normalize_data_zscore(xs, ys)

(k, b), num_inliers = RANSAC(xs, ys)
pred_scores = k * xs + b

plt.scatter(xs,ys)
plt.plot(xs, pred_scores,'r')
plt.show()

# %% [markdown]
# Now let's compare the difference of the estimate linear regression model when using v.s. not using RANSAC.

# %%
k_, b_ = linear_fitting(xs,ys)
linear_pred_scores = k_ * xs + b_

plt.scatter(xs,ys)
plt.plot(xs,linear_pred_scores,'r')
plt.show()


