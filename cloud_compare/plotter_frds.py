import os
import argparse
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# Function to read the fifth word from each line of a file
def read_fifth_word(filename):
    fifth_words = []
    with open(filename, 'r') as file:
        for line in file:
            words = line.split()
            if len(words) >= 5:
                fifth_words.append(float(words[4]))  # Assuming the fifth word is a number
    return fifth_words

# Function to generate x-axis values (increments of 30 starting from 0)
def generate_x_values(num_points, increment=1):
    return [i * increment for i in range(num_points)]

# Main function
def main():
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Plot data and fit polynomial curve.')
    parser.add_argument('--increment', type=int, default=1, help='Increment value for x-axis')
    parser.add_argument('--degree', type=int, default=5, help='Degree of polynomial for fitting curve')
    args = parser.parse_args()

    # Get the path to the "results f" folder in the same directory as the script
    folder_path = os.path.join(os.path.dirname(__file__), "results FRDS")
    plotter_folder = os.path.join(folder_path, "plotter FRDS")
    os.makedirs(plotter_folder, exist_ok=True)  # Create "plotter" subdirectory if it doesn't exist

    # Locate the file "output f.txt"
    file_path = os.path.join(folder_path, "output FRDS.txt")

    # Check if the file exists
    if os.path.isfile(file_path):
        # Read the fifth word from each line
        fifth_words = read_fifth_word(file_path)

        # Generate x-axis values (increments of specified value starting from 0)
        x_values = generate_x_values(len(fifth_words), increment=args.increment)

        # Fit a polynomial curve
        coeffs = np.polyfit(x_values, fifth_words, args.degree)
        poly = np.poly1d(coeffs)
        y_fit = poly(x_values)

        # Display the coefficients of the polynomial fit
        print(f'Polynomial Fit Coefficients (degree={args.degree}):')
        for i in range(args.degree, -1, -1):
            print(f'x^{i}: {coeffs[args.degree - i]}')

        # Create a plot
        plt.plot(x_values, fifth_words, label='Data')
        plt.plot(x_values, y_fit, label=f'Polynomial Fit (degree={args.degree})')
        plt.xlabel('Degrees')
        plt.ylabel('Frame')
        plt.title('Least Squares Plot with Polynomial Fit')
        plt.legend()
        plt.grid(True)

        # Save the plot as a PNG file
        today = datetime.today().strftime('%Y_%m_%d')
        plot_filename = os.path.join(plotter_folder, f'plot_FRDS_{today}.png')
        plt.savefig(plot_filename)
        print(f'Plot saved as: {plot_filename}')

        # Write the coefficients of the polynomial fit to a text file
        polyfit_filename = os.path.join(plotter_folder, 'polynomial FRDS.txt')
        with open(polyfit_filename, 'w') as polyfit_file:
            polyfit_file.write(f'Polynomial Fit Coefficients (degree={args.degree}):\n')
            for i in range(args.degree, -1, -1):
                polyfit_file.write(f'x^{i}: {coeffs[args.degree - i]}\n')
        print(f'Polynomial coefficients saved as: {polyfit_filename}')

        # Display the plot
        plt.show()
    else:
        print("File 'output FRDS.txt' not found in 'results FRDS' folder.")

if __name__ == "__main__":
    main()


#i.e. python script.py --increment 30 --degree 5
