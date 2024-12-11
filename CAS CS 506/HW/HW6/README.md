# CS506 Assignment 6
# Linear Regression

In this assignment, you'll explore the impact of changing parameters on linear regression. The goal is to create an interactive webpage to demonstrate how modifying these parameters affects regression results, especially when there is **no actual relationship** between `X` and `Y`. By tweaking these settings, you’ll observe how randomness can influence the slope and intercept in a regression model.

## Task Overview

The interactive webpage should allow users to input the following:

- **Sample size (N)**: Number of data points in the dataset.
- **Mean (mu)**: Mean of the normal error term added to `Y`.
- **Variance (sigma²)**: Variance of the normal error term.
- **Number of simulations (S)**: Number of datasets to simulate.

When the "Generate" button is clicked, the following should be displayed:

1. **Scatter Plot and Regression Line**: A plot of the generated random dataset `(Y, X)`, where there is no real relationship between `X` and `Y`, with random noise. Include the fitted linear regression line on the plot and display the slope and intercept values.

2. **Histogram of Slope and Intercept Values**: Generate `S` datasets, compute the slope and intercept for each, and display overlapping histograms. Mark the slope and intercept from the first dataset on the histogram. Show the proportions of slopes and intercepts that are "more extreme" than those in the initial dataset.

## Instructions
1. You can find the starter code in this repository under the "Code" section above. Please download it.
2. **Setting Up Flask**: Already done in the starter code.
3. **Complete the TODO Sections**: Follow the hints and complete each TODO section in the code.
4. Just install the requirements and run the code using "python app.py" or "python3 app.py" when you are done with your code. Feel free to use additional libraries according to your understanding and interests.
5. **Observe Results**:
   - Experiment with different values for `N`, `mu`, `sigma²`, and `S`.
   - Analyze how changing these values impacts the scatter plot and the histograms of slopes and intercepts.

6. The output would look something like this:
![image](https://github.com/user-attachments/assets/c8e3a991-f124-47e4-9d1f-7b39063c739e)


   
7. **Create a Short Demo Video (1-2 minutes)**:
   - Create a demo video by screen recording your output with your voice-over.
   - Explain any patterns you observe and discuss what happens when the sample size or noise level changes.
   - Explain whatever you found interesting and your analysis. You can discuss any specific points or specific inputs you want to.
   - Consider why random data might still produce non-zero slopes and intercepts in regression.

8. **Submission**:
   - Submit both your completed code and the demo video link.
   - You can either embed the demo video in your portfolio website or just create an unlisted YouTube video with a link to that YT video in your assignment 6 github repo's readme.

## Key Takeaways

This assignment helps you see how randomness can affect regression estimates. By experimenting with different parameters, you’ll get a better feel for how much variability there can be in slopes and intercepts when there’s no true relationship between `X` and `Y`. Using your observations and analysis will allow you to get a better and deep understanding of Linear Regression.
