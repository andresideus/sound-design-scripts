mport os
import shutil
import simpleaudio as sa
import time
import yaml

# Read the configuration from config.yaml
with open('config.yaml', 'r') as config_file:
    config = yaml.safe_load(config_file)

# The base folder is the sd_card from the config
folder = os.path.join('/Volumes', config['sd_card'])

for sub_dir in os.listdir(folder):
    sub_path = os.path.join(folder, sub_dir)
    if os.path.isdir(sub_path):
        wav_files = [f for f in os.listdir(sub_path) if f.lower().endswith('.wav')]
        if wav_files:  # If there are .wav files in the directory
            print(f'Previewing: {wav_files[0]}')
            wave_obj = sa.WaveObject.from_wave_file(os.path.join(sub_path, wav_files[0]))
            play_obj = wave_obj.play()
            time.sleep(5)  # Play the first 5 seconds
            play_obj.stop()

            label = input(f'Please type in a label for all files in directory {sub_dir}: ')

            for file in wav_files:
                new_file_name = f'{label}_{file}'
                new_file_path = os.path.join(config['destination_folder'], new_file_name)

                shutil.copy(os.path.join(sub_path, file), new_file_path)
                print(f'Copied: {new_file_path}')

                os.rename(os.path.join(sub_path, file), os.path.join(sub_path, new_file_name))
                print(f'Renamed: {new_file_name}')

delete_folder = input('Do you want to delete everything in the directories on the SD card? (yes/no) ')
if delete_folder.lower() == 'yes':
    for sub_dir in os.listdir(folder):
        shutil.rmtree(os.path.join(folder, sub_dir))
        print(f'Deleted: {os.path.join(folder, sub_dir)}')

