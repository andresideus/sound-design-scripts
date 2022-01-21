#!/usr/bin/env python

import os
import sys
import re
import pprint

pattern = sys.argv[1]
sampledir='/Users/q/music_creation/samples/'
files = os.listdir(sampledir)
infiles = []

for f in files:
    if re.match(r'.+'+ pattern +'_\.wav$',f):
        infiles.append(f)

print('found:')
pprint.pprint(infiles)

if raw_input('create new mono files?: ') == 'y':
    for f in infiles:
        fpath = sampledir + f
        outfile = f[:-4]+'mono.wav'
        command = 'sox '+sampledir+f+' '+sampledir+outfile+' remix 1'
        os.system(command)
        print(f+' -> '+outfile)

if raw_input('remove original files?: ') == 'y':
    for f in infiles:
        os.remove(sampledir+f)
        print('removed '+sampledir+f)
