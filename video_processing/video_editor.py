import cv2
import os
import numpy as np
import yaml

def crop_video(input_filename, output_filename, start_x, end_x, start_y, end_y):
    # Get the full path of the input video
    input_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), input_filename)

    # Open the video file
    cap = cv2.VideoCapture(input_path)

    # Get the original video's properties
    width = int(cap.get(3))
    height = int(cap.get(4))
    fps = cap.get(5)

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_filename)
    out = cv2.VideoWriter(output_path, fourcc, fps, (end_x - start_x, end_y - start_y))

    while True:
        # Read a frame from the video
        ret, frame = cap.read()

        # Break the loop if the video is finished
        if not ret:
            break

        # Crop the frame
        cropped_frame = frame[start_y:end_y, start_x:end_x]

        # Write the cropped frame to the output video
        out.write(cropped_frame)

    # Release the VideoCapture and VideoWriter objects
    cap.release()
    out.release()

def split_video_to_frames(video_filename, desired_fps=10):
    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the full path to the video file
    video_path = os.path.join(script_dir, video_filename)

    # Open the video file
    video_capture = cv2.VideoCapture(video_path)
    
    # Get the base filename (excluding extension)
    base_filename = os.path.splitext(os.path.basename(video_filename))[0]

    # Create the output folder based on the input file name and fps value
    output_folder = f"{base_filename}_fps{desired_fps}"
    output_folder_path = os.path.join(script_dir, output_folder)
    os.makedirs(output_folder_path, exist_ok=True)

    # Get the frames per second (fps) of the input video
    fps = int(video_capture.get(cv2.CAP_PROP_FPS))

    # Get the maximum possible fps of the input video
    max_fps = int(video_capture.get(cv2.CAP_PROP_FPS))

    # Counter for naming the output frames
    count = 0

    print(f"Maximum available fps: {max_fps}")

    while True:
        # Read the next frame from the video
        success, frame = video_capture.read()

        if not success:
            break

        # Save the frame as an image file
        frame_path = os.path.join(output_folder_path, f"frame_{count:04d}.png")
        cv2.imwrite(frame_path, frame)

        count += 1

        # Skip frames to achieve the desired fps
        for _ in range(int(fps / desired_fps) - 1):
            success, _ = video_capture.read()
            if not success:
                break

    # Release the video capture object
    video_capture.release()

    print(f"Frames extracted successfully to {output_folder_path}")

def undistort_images(input_folder, output_folder, camera_matrix, distortion_coefficients):
    # Extract the input folder name
    input_folder_name = os.path.basename(input_folder)

    # Create a new folder for undistorted images
    undistorted_folder = os.path.join(os.path.dirname(input_folder), f"{input_folder_name}_undist")
    if not os.path.exists(undistorted_folder):
        os.makedirs(undistorted_folder)

    # Convert camera_matrix and distortion_coefficients to NumPy arrays
    camera_matrix = np.array(camera_matrix)
    distortion_coefficients = np.array(distortion_coefficients)

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png')):
            # Read the image
            img_path = os.path.join(input_folder, filename)
            img = cv2.imread(img_path)

            # Undistort the image
            undistorted_img = cv2.undistort(img, camera_matrix, distortion_coefficients)

            # Save the undistorted image to the output folder
            output_path = os.path.join(undistorted_folder, filename)
            cv2.imwrite(output_path, undistorted_img)

            print(f"Undistorted: {filename}")

    return undistorted_folder  # Return the path to the undistorted folder

def load_config(config_filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, config_filename)
    
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    return config

def main():
    # Load configuration from YAML file
    config = load_config('config.yml')

    input_video_filename = config['input_video_filename']
    desired_fps = config['desired_fps']
    camera_coefficients_map = config['camera_coefficients_map']

    # Crop the original video into three segments
    crop_video(input_video_filename, "crop1.mp4", 0, 1920, 0, 1080)
    crop_video(input_video_filename, "crop2.mp4", 1920, 3840, 0, 1080)
    crop_video(input_video_filename, "crop3.mp4", 0, 1920, 1080, 2160)

    # Process each set of frames
    for i in range(1, 4):
        crop_input_filename = f"crop{i}.mp4"
        split_video_to_frames(crop_input_filename, desired_fps)

        # Set the input folder path for frames
        input_frames_folder = f"crop{i}_fps{desired_fps}"
        input_frames_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), input_frames_folder)

        # Set the output folder path for undistorted frames
        output_undistorted_folder = f"{input_frames_folder}_undistorted"
        output_undistorted_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_undistorted_folder)

        # Set the simplified folder name for camera matrix
        simplified_folder_name = f"crop{i}"

        # Undistort the images using the corresponding camera matrix and distortion coefficients
        camera_matrix = camera_coefficients_map[simplified_folder_name]["camera_matrix"]
        distortion_coefficients = camera_coefficients_map[simplified_folder_name]["distortion_coefficients"]
        undistort_images(input_frames_path, output_undistorted_path, camera_matrix, distortion_coefficients)

        print(f"Undistorted images saved in: {output_undistorted_path}")

if __name__ == "__main__":
    main()
