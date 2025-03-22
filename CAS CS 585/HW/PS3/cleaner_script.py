def clean_python_file():
    with open("ps3.py", "r") as f:
        lines = f.readlines()

    remove_lines = [
        "blue=",
    ]

    with open("ps3_cleaned.py", "w") as f:
        for line in lines:
            line_strip = line.strip()

            ## ignore line that starts with `remove_lines`:
            if any(line_strip==remove_line for remove_line in remove_lines):
                continue

            if line.startswith("plt.") or line.startswith("print(") \
            or line.startswith("cv2.imshow(") or line.startswith("get_ipython(") \
            or line.startswith("np.random.seed(") or line.startswith("display("):
                continue

            ## clean code, write out to a new file and grade on this file
            f.write(line)

    return None 
