from flask import Flask, render_template, request, url_for
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for non-GUI rendering
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import io
import base64

app = Flask(__name__)

def generate_plots(N, mu, sigma2, S):

    # STEP 1
    # TODO 1: Generate a random dataset X of size N with values between 0 and 1
    # and a random dataset Y with normal additive error (mean mu, variance sigma^2).
    # Hint: Use numpy's random's functions to generate values for X and Y
    X = np.random.uniform(0, 1, N)  # Replace with code to generate random values for X
    Y = X + np.random.normal(mu, np.sqrt(sigma2), N)  # Replace with code to generate random values for Y with specified mean and variance

    # TODO 2: Fit a linear regression model to X and Y
    # Hint: Use Scikit Learn
    model = LinearRegression()
    model.fit(X.reshape(-1, 1), Y)  # Replace with code to fit the model
    slope = model.coef_[0]  # Replace with code to extract slope from the fitted model
    intercept = model.intercept_  # Replace with code to extract intercept from the fitted model

    # TODO 3: Generate a scatter plot of (X, Y) with the fitted regression line
    # Hint: Use Matplotlib
    # Label the x-axis as "X" and the y-axis as "Y".
    # Add a title showing the regression line equation using the slope and intercept values.
    # Finally, save the plot to "static/plot1.png" using plt.savefig()
    plt.figure(figsize=(10, 6))
    plt.scatter(X, Y, color='blue', label='Data Points')
    
    # Plot the regression line
    X_sorted = np.sort(X)
    Y_pred = model.predict(X_sorted.reshape(-1, 1))
    plt.plot(X_sorted, Y_pred, color='red', label=f'Regression Line: y = {slope:.2f}x + {intercept:.2f}')
    
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(f'Regression Line: y = {slope:.2f}x + {intercept:.2f}')
    plt.legend()

    # Save the plot to a file
    plot1_path = "static/plot1.png"
    plt.savefig(plot1_path)
    plt.close()

    
    # Step 2: Run S simulations and create histograms of slopes and intercepts

    # TODO 1: Initialize empty lists for slopes and intercepts
    # Hint: You will store the slope and intercept of each simulation's linear regression here.
    slopes = []  # Replace with code to initialize empty list
    intercepts = []  # Replace with code to initialize empty list

    # TODO 2: Run a loop S times to generate datasets and calculate slopes and intercepts
    # Hint: For each iteration, create random X and Y values using the provided parameters
    for _ in range(S):
        # TODO: Generate random X values with size N between 0 and 1
        X_sim = np.random.uniform(0, 1, N)  # Replace with code to generate X values

        # TODO: Generate Y values with normal additive error (mean mu, variance sigma^2)
        Y_sim = X_sim + np.random.normal(mu, np.sqrt(sigma2), N)  # Replace with code to generate Y values

        # TODO: Fit a linear regression model to X_sim and Y_sim
        sim_model = LinearRegression()  # Initialize model
        sim_model.fit(X_sim.reshape(-1, 1), Y_sim)  # Replace with code to fit model

        # TODO: Append the slope and intercept of the model to slopes and intercepts lists
        slopes.append(sim_model.coef_[0])  # Replace None with code to append slope
        intercepts.append(sim_model.intercept_)  # Replace None with code to append intercept

    # Plot histograms of slopes and intercepts
    plt.figure(figsize=(10, 5))
    plt.hist(slopes, bins=20, alpha=0.5, color="blue", label="Slopes")
    plt.hist(intercepts, bins=20, alpha=0.5, color="orange", label="Intercepts")
    plt.axvline(slope, color="blue", linestyle="--", linewidth=1, label=f"Slope: {slope:.2f}")
    plt.axvline(intercept, color="orange", linestyle="--", linewidth=1, label=f"Intercept: {intercept:.2f}")
    plt.title("Histogram of Slopes and Intercepts")
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.legend()
    plot2_path = "static/plot2.png"
    plt.savefig(plot2_path)
    plt.close()

    # Below code is already provided
    # Calculate proportions of more extreme slopes and intercepts
    # For slopes, we will count how many are greater than the initial slope; for intercepts, count how many are less.
    slope_more_extreme = sum(s > slope for s in slopes) / S  # Already provided
    intercept_more_extreme = sum(i < intercept for i in intercepts) / S  # Already provided

    return plot1_path, plot2_path, slope_more_extreme, intercept_more_extreme

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get user input
        N = int(request.form["N"])
        mu = float(request.form["mu"])
        sigma2 = float(request.form["sigma2"])
        S = int(request.form["S"])

        # Generate plots and results
        plot1, plot2, slope_extreme, intercept_extreme = generate_plots(N, mu, sigma2, S)

        return render_template("index.html", plot1=plot1, plot2=plot2,
                               slope_extreme=slope_extreme, intercept_extreme=intercept_extreme)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)