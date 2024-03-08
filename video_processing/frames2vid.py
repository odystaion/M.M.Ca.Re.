#The purpose of this script is to combine the undistorted frames into a new video.
#Make sure to have the frames into a JPG or a PNG format.
#All the frames used for the new video should be in the same folder
#Input the FOLDER NAME
#The programm with combine the frames and generate a new MP4 file

import cv2
import os

def images_to_video(image_folder, fps=30):
    images = [img for img in os.listdir(image_folder) if img.endswith(".png") or img.endswith(".jpg")]
    images.sort()

    if not images:
        print("No images found in the specified folder.")
        return

    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video_name = f'{os.path.basename(os.path.normpath(image_folder))}_video.mp4'
    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()

if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.abspath(__file__))
    image_folder = os.path.join(script_directory, 'calib_stereo_1_fps20')
    fps = 30

    images_to_video(image_folder, fps)
