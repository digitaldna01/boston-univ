# Lab 2: Image Compression using KMeans

---

**To get credit for the lab, please show the completed work to a lab TA. They will check you off.**

**Goals**:

1. Learn how to apply KMeans clustering for image compression.
2. Implement basic image processing tasks.
3. Practice working with external libraries such as `scikit-learn`, `numpy`, `Pillow`, and `Flask`.
4. Understand how to manipulate images as NumPy arrays and perform color reduction.
5. Build an interactive module using Flask to handle image processing through a web interface.

## Part 0: Setup Environment

### Step 1: Install the required libraries
You can use the `Makefile` to install all dependencies. In your terminal, simply run:

```bash
make install
```

This will automatically install the necessary packages listed in `requirements.txt`, including:

- Flask
- Numpy
- Scikit-learn
- Pillow

### Step 2: Implement the algorithm & Test on the Flask server

## Part 1: Implementing Image Compression

1. **Complete the following functions in the provided script**:
    - `load_image(image_path)`: This function should load the image from a file and return it as a NumPy array. You will need to use the `Pillow` library for this task.
    - `image_compression(image_np, n_colors)`: Implement KMeans clustering using `scikit-learn` to reduce the number of colors in the image to `n_colors`. The function should return a compressed version of the image.
2. **Save the Compressed Image**: The function `save_result` has been provided for you. Once the original and compressed images are prepared, the function will save them side by side in a single image file.

## Part 2: Testing Your Code with a Static Input

1. If you prefer, you can also test the code locally by running the script directly and specifying an image path. Modify the `__main__()` function to load the image, apply compression, and save the results. Make sure you provide paths for both input and output images.
2. Choose your favorite image as input and experiment with different values of `n_colors` (e.g., 4, 8, 16) and observe the effect on image quality.

## Example Workflow

1. Select your favorite image file (e.g., `'favorite_image.png'`) and place it in your working directory.
2. In the `__main__()` function:
    - Set `image_path` to your selected image file.
    - Set `output_path` to where you want to save the side-by-side result (e.g., `'compressed_image.png'`).
    - Choose an appropriate number of colors (`n_colors`), e.g., 8.
3. Run the script in your terminal:
   
   python image_compression.py

4. Check the output image to see the original and compressed versions side by side.

## Part 3: Running the Interactive Module

Once the environment is set up, you can start the Flask application by running:

```bash
make run
```

This will start the Flask server and make the interactive application available locally at `http://127.0.0.1:3000`.

The interactive module allows you to upload an image and select the number of colors for compression through a web interface.

1. Open your browser and go to `http://127.0.0.1:3000`.
2. Upload your favorite image using the provided interface.
3. Enter the number of colors for compression.
4. Click the "Submit" button to perform the image compression.
5. The original and compressed images will be displayed side by side on the page.

## Notes:

1. Ensure that the image loaded is in RGB format.
2. Test with your favorite image and experiment with different values for `n_colors` to observe the impact of compression.
3. If you encounter issues loading or saving images, check the installation of `Pillow` and the file format compatibility.
4. If you encounter issues running the Flask server, ensure that `flask` is correctly installed and check the command line output for error messages.
