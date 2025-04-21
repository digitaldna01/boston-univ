### clean the submission file
def clean_python_file():
    with open("ps4.py", "r") as f:
        lines = f.readlines()

    remove_lines = [
        "blue=",
    ]

    with open("ps4_cleaned.py", "w") as f:
        first_block_active = False
        second_block_active = False
        third_block_active = False
        fourth_block_active = False
        for line in lines:
            line_strip = line.strip()

            ## ignore line that starts with `remove_lines`:
            if any(line_strip == remove_line for remove_line in remove_lines):
                continue

            if line.startswith("plt.") or line.startswith("print(") \
                    or line.startswith("cv2.imshow(") or line.startswith("get_ipython(") \
                    or line.startswith("np.random.seed(") or line.startswith("display("):
                continue

            if 'google' in line or 'drive.mount' in line or 'skimage' in line or 'savefig' in line or '%matplotlib' in line or 'display(' in line:
                continue

            if 'lab_pt1 = matches_lab[:,:2]' in line:
                continue
            if 'lab_pt2 = matches_lab[:,2:]' in line:
                continue
            if 'np.vstack((lab1_c, lab2_c))' in line:
                continue
            if 'ax.scatter' in line:
                continue

            '''if 'lab_pt1 = matches_lab[:,:2]' in line:
                                                    continue
                                                if 'lab_pt2 = matches_lab[:,2:]' in line:
                                                    continue
                                                if 'camera_centers = np.vstack((lab1_c, lab2_c))' in line:
                                                    continue
                                                if 'plt.figure()' in line:
                                                    continue
                                                if 'ax = fig.add_subplot(111, projection=\'3d\')' in line:
                                                    continue
                                                if 'ax.scatter(points_3d_lab[:, 0]' in line:
                                                    continue
                                                if 'ax.scatter(camera_centers[:, 0]' in line:
                                                    continue
                                                if 'ax.legend(loc=\'best\')':
                                                    continue'''

            # if '[0, f, v]' in line:
            #    continue
            # if '[0, 0, 1]' in line:
            #    continue

            if ('np.loadtxt' in line and 'lab_matches.txt' not in line) or 'np.save' in line:
                continue

            if 'pred_height' in line or 'predicted height' in line or 'K = np.array([[f, 0, u' in line or 'str(height' in line:
                continue

            if 'all_lines.npy' in line or 'tkinter' in line or 'matplotlib.use(\'TKAgg\')' in line or 'TkAgg' in line:
                continue

            if 'def' not in line and 'get_camera_parameters' in line:
                continue

            if 'def' not in line and 'get_rotation_matrix' in line:
                continue

            if 'def' not in line and 'camera_calibration' in line:
                continue

            if 'def' not in line and 'evaluate_points' in line:
                continue

            if 'def' not in line and 'calc_camera_center' in line:
                continue

            if 'def' not in line and 'get_top_and_bottom_coordinates' in line:
                line = '    x=5\n'

            if 'def' not in line and 'estimate_height' in line:
                continue

            if 'def' not in line and 'triangulation' in line:
                continue

            if ('get_best_matches' in line or 'ransac' in line) and 'def' not in line:
                continue

            if 'ps5_example' in line and 'np.asarray(Image.open' in line:
                first_block_active = True
            elif 'def' not in line and 'plot_horizon_line(' in line and first_block_active:
                first_block_active = False
                continue

            if first_block_active:
                continue

            '''if '= imread' in line or '= get_best_matches' in line or 'plt.subplots' in line or 'plot_inlier_matches(ax, img1, img2, data)' in line or ' = ransac' in line:
                                                    continue

                                                if 'F, max_inliers, inliers, avg_residual = ransac(data)' in line or 'avg_residual = ransac(matches)' in line or 'rmse = np.sqrt(np.mean((F - F_gt) ** 2))' in line:
                                                     continue

                                                if '= get_camera_parameters(vpts)' in line or 'all_lines.npy' in line or 'ps5_example.jpg' in line:
                                                    continue

                                                if 'def' not in line and 'get_rotation_matrix' in line:
                                                    continue

                                                if 'def' not in line and 'get_vanishing_point' in line:
                                                    continue

                                                if 'def' not in line and 'choose_vp' in line:
                                                    continue

                                                if 'def' not in line and 'evaluate_points' in line:
                                                    continue

                                                if 'def' not in line and 'get_camera_parameters' in line:
                                                    continue

                                                if ('get_A' in line and 'def' not in line) or 'A.shape' in line:
                                                    continue

                                                if 'objects = (' in line:
                                                    fourth_block_active = True
                                                elif '(ft, inches)' in line:
                                                    fourth_block_active = False
                                                    continue

                                                if 'im = np.asarray(Image.open(' in line:
                                                    third_block_active = True
                                                elif 'def' not in line and 'plot_horizon_line' in line:
                                                    third_block_active = False
                                                    continue

                                                # for first block
                                                if 'np.loadtxt' in line or '_proj = camera_calibration' in line or '_res = evaluate_points' in line or '_c = calc_camera_center' in line: 
                                                    continue

                                                # for second block:
                                                if 'lab_pt1 = matches_lab[:,:2]' in line:
                                                    second_block_active = True
                                                elif 'ax.legend(loc=\'best\')' in line:
                                                    second_block_active = False
                                                    continue

                                                if 'num_vpts = 3' in line:
                                                    first_block_active = True
                                                elif 'def' not in line and 'plot_horizon_line' in line:
                                                    first_block_active = False
                                                    continue

                                                if first_block_active or second_block_active or third_block_active or fourth_block_active:
                                                    continue'''

            ## clean code, write out to a new file and grade on this file
            f.write(line)

    return None

if __name__ == "__main__":
    clean_python_file()