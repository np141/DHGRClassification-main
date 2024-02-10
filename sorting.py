import cv2
import os
import shutil

def list_directories(path):
    return [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
mudra_folders = [
    "Alapadma", "Aral", "Ardhachandra", "Ardhapataka", "Bhramara",
    "Chandrakala", "Chatura", "Hamsapaksha", "Hamsasya", "Kangula",
    "Kapittha", "Kartarimukha", "Katakamukha", "Mayura", "Mrigashirsha",
    "Mukula", "Musti", "Padmakosha", "Pataka", "Sarpasirsha",
    "Shikhara", "Shukatunda", "Simhamukha", "Suchi", "Tamrachuda",
    "Tripataka", "Trishoola"
]

unsorted_base = 'unsortedDB'
sorted_base = 'Single_Hand_Dataset/Asamyukta Mudras'

if not os.path.exists(unsorted_base):
    print(f"Directory {unsorted_base} not found.")
    exit()
unsorted_folders = list_directories(unsorted_base)
if not unsorted_folders:
    print("No unsorted folders available.")
    exit()
print("Available unsorted folders:")
for i, folder in enumerate(unsorted_folders, 1):
    print(f"{i} - {folder}")
try:
    folder_number = int(input("Select the unsorted folder to process: ")) - 1
    selected_unsorted_folder = unsorted_folders[folder_number]
except (ValueError, IndexError):
    print("Invalid selection.")
    exit()
print("Mudra folders:")
for i, name in enumerate(mudra_folders, 1):
    print(f"{i} - {name}")
last_choice = None
for image_file in os.listdir(os.path.join(unsorted_base, selected_unsorted_folder)):
    full_image_path = os.path.join(unsorted_base, selected_unsorted_folder, image_file)
    if not os.path.isfile(full_image_path):
        continue
    img = cv2.imread(full_image_path)
    if img is None:
        print(f"Failed to load image: {image_file}")
        continue
    cv2.imshow("Image", img)
    cv2.waitKey(1)
    if last_choice is not None:
        use_last_choice = input(f"Send this image to '{mudra_folders[last_choice]}'? (Y/N/S for skip): ").strip().upper()
        if use_last_choice == 'S':
            print(f"Skipped {image_file}.")
            continue 
        elif use_last_choice == 'Y':
            choice = last_choice
        else:
            choice_input = input("Select the mudra folder number or press 'S' to skip: ").strip().upper()
            if choice_input == 'S':  
                print(f"Skipped {image_file}.")
                continue
            else:
                try:
                    choice = int(choice_input) - 1
                except ValueError:
                    print("Invalid input. Skipping this image.")
                    continue
    else:
        choice_input = input("Select the mudra folder number or press 'S' to skip: ").strip().upper()
        if choice_input == 'S':  
            print(f"Skipped {image_file}.")
            continue
        else:
            try:
                choice = int(choice_input) - 1
            except ValueError:
                print("Invalid input. Skipping this image.")
                continue
    last_choice = choice
    destination_folder = os.path.join(sorted_base, mudra_folders[choice])
    os.makedirs(destination_folder, exist_ok=True)
    shutil.move(full_image_path, destination_folder)
    print(f"Moved {image_file} to {mudra_folders[choice]}.")
cv2.destroyAllWindows()
print("Processing complete.")
