#The purpose of this script is to be used to find the optimal dimensions for multiple camera feed capturing.
#First enter the SCREEN dimensions.
#Then enter the CAMERA SENSOR dimensions (use identical cameras)
#Select how many cameras you want to capture simultaneously HORIZONTALLY and VERTICALLY
#The program calculates the maximum pixel number for OBS TRANFORMATIONS


def calculate_max_camera_dimensions(screen_width, screen_height, camera_width, camera_height):
    # Separate division factors for width and height
    width_division_factor = float(input("Enter the division factor for screen width: "))
    height_division_factor = float(input("Enter the division factor for screen height: "))

    # Divide screen dimensions
    screen_width /= width_division_factor
    screen_height /= height_division_factor

    # Calculate the maximum dimension available
    max_dimension = min(screen_width, screen_height)

    # Calculate the width-to-length ratio of the camera
    camera_ratio = camera_width / camera_height

    # Calculate the maximum width based on the camera ratio
    max_camera_width = min(max_dimension, camera_ratio * max_dimension)

    # Calculate the corresponding length based on the width-to-length ratio
    max_camera_length = max_camera_width / camera_ratio

    return max_camera_width, max_camera_length

# Get user inputs for screen dimensions
screen_width = int(input("Enter screen width in pixels: "))
screen_height = int(input("Enter screen height in pixels: "))

# Get user inputs for camera dimensions
camera_width = int(input("Enter camera width in pixels: "))
camera_height = int(input("Enter camera height in pixels: "))

# Calculate and print the maximum camera dimensions
max_camera_width, max_camera_length = calculate_max_camera_dimensions(screen_width, screen_height, camera_width, camera_height)

print(f"The maximum possible camera dimensions are: {max_camera_width} pixels x {max_camera_length} pixels")

