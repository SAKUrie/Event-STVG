import os
import time
from tqdm import tqdm
from scenedetect import SceneManager, open_video, AdaptiveDetector, ThresholdDetector, ContentDetector
from scenedetect.video_splitter import split_video_ffmpeg
import csv
from shutil import copy2

def intoCSV(l):
    csv_columns = ['Video', 'st_time', 'ed_time']

    with open('event.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)

        csv_writer.writerow(csv_columns)

        for item in l:
            Video_id = item[0].split('/')[2] if '/' in item[0] else 'Not Found'
            st_time = item[1] if len(item) > 1 else 'N/A'
            ed_time = item[2] if len(item) > 2 else 'N/A'
            csv_writer.writerow([Video_id, st_time, ed_time])

    print("CSV file 'event.csv' has been created successfully.")


def get_event(video_path, output_folder="event"):
    video = open_video(video_path)
    manager = SceneManager()
    manager.add_detector(AdaptiveDetector())
    manager.detect_scenes(video)
    scene_list = manager.get_scene_list()

    if not scene_list:
        return [-1, 0.00, video.duration.get_seconds()]

    max_span = 0
    event = None

    for scene in scene_list:
        start_time, end_time = scene
        span = end_time - start_time
        if span > max_span:
            event = scene
            max_span = span

    events = [event]
    # print(f"video:{video_path},start time:{(event[0].get_seconds()):.2f}s")
    s = split_video_ffmpeg(video_path, events, output_dir=output_folder,
                           output_file_template="$VIDEO_NAME.mp4")
    return [0, event[0].get_seconds(), event[1].get_seconds()]


folder_path = ''
output_file_path = 'event'
video_files = []
event_list = []

folder_path = os.getcwd()
entries = os.listdir(folder_path)

for root, dirs, files in os.walk("."):
    for file in files:
        if file.endswith(".mp4"):
            video_files.append(os.path.join(root, file))

# for entry in entries:
#     full_path = os.path.join(folder_path, entry)
#     if os.path.isfile(full_path) and entry.lower().endswith(('.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm')):
#         video_files.append(entry)

video_files.sort()
for v in tqdm(video_files, desc="Processing videos", unit="file"):
    status = get_event(v, output_file_path)
    event_list.append([v, status[1], status[2]])
    if status[0] == -1:
        copy2(v,output_file_path)


intoCSV(event_list)
print(len(event_list))
