import shutil
import os, sys

def clear_pycache(path):
    for root, dirs, files in os.walk(path):
        if '__pycache__' in dirs:
            shutil.rmtree(os.path.join(root, '__pycache__'))
            print(f"Deleted: {os.path.join(root, '__pycache__')}")



##### MAIN FUNCTION #####
def main():
    try:
        # Call the function with the path to your project's root directory
        clear_pycache('.') # Deletes from the current directory

    except ValueError as ve:
        return str(ve)

if __name__ == "__main__":
    sys.exit(main())