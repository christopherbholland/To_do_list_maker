import os
import shutil

def clear_output_directory(directory="output"):
    if os.path.exists(directory):
        # Remove all files and subdirectories in the directory
        shutil.rmtree(directory)
        print(f"Cleared all files and subdirectories in '{directory}'")
    else:
        print(f"Directory '{directory}' does not exist.")
    # Recreate the directory to ensure it's clean and ready for new output
    os.makedirs(directory, exist_ok=True)
    print(f"Recreated '{directory}' for new output.")

# Clear the output directory
clear_output_directory()