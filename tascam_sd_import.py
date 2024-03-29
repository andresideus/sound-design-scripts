#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import re
from shutil import copyfile
import pprint
import datetime

dest_path = os.path.expanduser('~/music_creation/samples')
sd_mount = '/Volumes/DR-40X'
recorded_file_dir = sd_mount + '/' + 'MUSIC'
ch_12_label = 'dr40x'
ch_34_label = 'ntg3'
human_label = ''
cp_manifest = {}

def eject(mount):
    if raw_input('eject card?: ') == 'y':
	os.system('diskutil eject ' + mount)	
    sys.exit()

# check if sd card is there and non empty

if os.path.exists(recorded_file_dir):
    sd_files = os.listdir(recorded_file_dir)
    if len(sd_files) == 0:
        print 'exiting: directory empty'
	eject(sd_mount)

    for f in sd_files:

    # which track pair?

        if re.match(r'.+12.wav$', f) is not None:

      # play a 5 sec preview & ask for name

            print 'Playing ' + f + ':'
            os.system('afplay -t 5 ' + recorded_file_dir + '/' + f)
            human_label = raw_input('type a label : '
                                    ).lower().replace(' ', '')

      # set up filenames

            file_root = f[:-6]
            old_ch12_file = file_root + '12.wav'
            old_ch34_file = file_root + '34.wav'
	    timestamp = os.path.getmtime(recorded_file_dir + '/' + f)
	    value = datetime.datetime.fromtimestamp(timestamp)
	    mtime_str = (value.strftime('%Y-%d-%b_%H%M-%Ss')).lower()
            new_ch12_file = (human_label + '_' + mtime_str + '_' + ch_12_label + '.wav').lower()
            new_ch34_file = (human_label + '_' + mtime_str + '_' + ch_34_label + '.wav').lower()
            cp_manifest.update({old_ch12_file: new_ch12_file})
            cp_manifest.update({old_ch34_file: new_ch34_file})
else:
    print 'exiting; didnt find ' + recorded_file_dir
    eject(sd_mount)

# copy the files

if not os.path.exists(dest_path):
    os.makedirs(dest_path)
print 'from ' + recorded_file_dir + ' -> ' + dest_path
pprint.pprint(cp_manifest)

if raw_input('copy files?: ') == 'y':
    for (key, value) in cp_manifest.items():
	src = recorded_file_dir + '/' + key
	dst = dest_path + '/' + value

	dst = dst[:-4] + '_' \
	    + dst[-4:]
	copyfile(src, dst)
	print 'copied: ' + src + ' -> ' + dst

if raw_input('remove files?: ') == 'y':
    for f in os.listdir(recorded_file_dir):
        os.remove(recorded_file_dir + '/' + f)
        print 'removed: ' + f

eject(sd_mount)
