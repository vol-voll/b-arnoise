import os

# Ask the user for the directory path
folder_path = input("Enter the directory path where the file should be saved: ")

# Check if the provided directory exists
if not os.path.exists(folder_path):
    print("The specified directory does not exist.")
else:
    # Ask the user for the filename
    file_name = input("Enter the filename (including .txt extension): ")

    # Combine the folder path and file name to get the full file path
    full_file_path = os.path.join(folder_path, file_name)

    # Check if the file exists
    if os.path.exists(full_file_path):
        # If the file exists, open it in append mode
        file = open(full_file_path, 'a')
    else:
        # If the file doesn't exist, create and open it in write mode
        file = open(full_file_path, 'w')

    # Write some text to the file
    file.write('Hello, this is some text!\n')

    # Close the file
    file.close()

    print(f"Text has been written to {full_file_path}")
