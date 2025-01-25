import numpy as np
import cv2

# Load an image from a file
image = cv2.imread("./boston.jpg")

print(type(image))

# For color images, the decoded images will have the channels stored in B G R order.
print(image.shape)

def tintBlue(image):
    """
        Tint the input image blue

        :param image: input color image
        :type image: ndarray
        :rtype: ndarray
    """
    # make the blue chanel saturation max which mean the MAX 255
    image[:,:,0] = 255

    return image

# Display the image
cv2.namedWindow("Display window", cv2.WINDOW_AUTOSIZE)
cv2.imshow("Display window", image)
# Wait for a key event infinitely
cv2.waitKey(0)

# Close all open windows
cv2.destroyAllWindows()
# For mac users, uncomment the following line
cv2.waitKey(1)

def readVideo(video_path):
    """
        Read the video frames.

        :param video_path: path to input video
        :type video_path: str
        :rtype: ndarray
    """
    
    # TODO: your implementation here - write a function to read video frames and combine them into a numpy array of size 'T x H x W x C'.
    # T, H, W and C denote the number of frames, height, width and number of channels, respectively.
    cap = cv2.VideoCapture(video_path)
    
    # to store frames
    frames = []
    
    # Read Video Frames
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    
    cap.release()
    
    video_frames = np.array(frames)

    return video_frames

# reads a video file
video_frames = readVideo("./input_video.mp4")