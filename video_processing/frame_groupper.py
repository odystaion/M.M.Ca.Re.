import os
import zipfile

def create_zip_from_folder(folder_name):
    # Assuming folder_name is in the same location as the script
    folder_path = os.path.join(os.path.dirname(__file__), folder_name)

    # Set the first and final frame numbers
    first_frame = 1025
    final_frame = 1120 # Updated to include frames up to 190

    # Create a zip file with the folder name and first frame number
    zip_file_name = f"{folder_name}_frames_{first_frame}_to_{final_frame}.zip"
    zip_file_path = os.path.join(os.path.dirname(__file__), zip_file_name)

    with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
        for frame_number in range(first_frame, final_frame + 1):
            # Use zfill to ensure proper zero-padding in the frame number
            frame_name = f"frame_{str(frame_number).zfill(4)}.png"
            frame_path = os.path.join(folder_path, frame_name)

            # Add the frame to the zip file
            zip_file.write(frame_path, arcname=frame_name)

    print(f"Zip file '{zip_file_name}' created successfully.")

if __name__ == "__main__":
    folder_name = "trial02 2023-12-22 V3_fps15_undist"
    create_zip_from_folder(folder_name)
