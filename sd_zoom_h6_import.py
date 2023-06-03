import os
import glob
import shutil
import simpleaudio as sa
import time
import sys

source_dir = "/Volumes/H6_SD/FOLDER01"
dest_dir = sys.argv[1]

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

for root, dirs, files in os.walk(source_dir):
    wav_files = glob.glob(os.path.join(root, '*.WAV'))
    if wav_files:
        wav_files.sort()  # make sure we're getting the first wav file
        first_wav = wav_files[0]
        print(f"Playing first 5 sec of {first_wav}")
        wave_obj = sa.WaveObject.from_wave_file(first_wav)
        play_obj = wave_obj.play()
        time.sleep(5)  # play for 5 sec
        play_obj.stop()

        label = input("Enter a label to prepend to all .WAV files in the directory: ")

        for f in wav_files:
            new_name = os.path.join(root, label + os.path.basename(f))
            print(f"Renaming {f} to {new_name}")
            os.rename(f, new_name)
            print(f"Copying {new_name} to {dest_dir}")
            shutil.copy(new_name, dest_dir)

confirmation = input(f"Do you want to remove all contents in {source_dir}? [yes/no]: ")
if confirmation.lower() == 'yes':
    for root, dirs, files in os.walk(source_dir, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.exists(file_path):
                print(f"Removing {file_path}")
                os.remove(file_path)
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if os.path.exists(dir_path):
                print(f"Removing {dir_path}")
                os.rmdir(dir_path)
else:
    print("Operation cancelled.")

