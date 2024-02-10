import cv2
import mediapipe as mp
import os
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)

hand_directory_base = 'unsortedDB'
if not os.path.exists(hand_directory_base):
    os.makedirs(hand_directory_base)

def list_videos(directory):
    video_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.mp4', '.avi', '.mov')):
                video_files.append(os.path.join(root, file))
    return video_files

video_directory = 'videos'
video_files = list_videos(video_directory)
print("Available Videos:")
for i, file in enumerate(video_files):
    print(f"{i + 1}: {file}")

video_number = int(input("Enter Video list number you need to process123456789: ")) - 1
video_path = video_files[video_number]
video_name = os.path.splitext(os.path.basename(video_path))[0]

video_frames_directory = os.path.join(hand_directory_base, video_name)
if not os.path.exists(video_frames_directory):
    os.makedirs(video_frames_directory)

cap = cv2.VideoCapture(video_path)
if not cap.isOpened():
    print(f"Failed to Open Video: {video_path}")
    exit()

frame_count = 0
processed_frame_count = 0
frame_rate = cap.get(cv2.CAP_PROP_FPS)
print("Frame Rate =", frame_rate)

frame_skip = int(input("Enter Number of frames to skip between processes. 0-29/No skipping-Every 30th frame"))

def get_hand_bbox(frame, hand_landmarks):
    height, width, _ = frame.shape
    x_min, y_min, x_max, y_max = width, height, 0, 0
    for landmark in hand_landmarks.landmark:
        x, y = int(landmark.x * width), int(landmark.y * height)
        x_min, y_min, x_max, y_max = min(x_min, x), min(y_min, y), max(x_max, x), max(y_max, y)
    padding = 50
    return max(0, x_min-padding), min(width, x_max+padding), max(0, y_min-padding), min(height, y_max+padding)

def detect_and_crop_hands(frame, frame_number):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            x_min, x_max, y_min, y_max = get_hand_bbox(frame, hand_landmarks)
            hand_crop = frame[y_min:y_max, x_min:x_max]
            hand_filename = f'{video_frames_directory}/hand_{frame_number}_{x_min}.jpg'
            cv2.imwrite(hand_filename, hand_crop)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Finished processing.")
        break
    if frame_count % (frame_skip + 1) == 0:
        detect_and_crop_hands(frame, processed_frame_count)
        processed_frame_count += 1
        print(f"Processed frame {processed_frame_count}")
    frame_count += 1

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
