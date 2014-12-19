#!/usr/bin/env python 

import os
import glob 
import subprocess
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("dir", help = "Input directory")

args = parser.parse_args()

# Make the output directories if they don't exist already 
if not os.path.exists("mp3"):
	os.mkdir("mp3")

if not os.path.exists("mp4"):
	os.mkdir("mp4")

if os.path.exists(args.dir):
	os.chdir(args.dir) 

	# get files with extension .mp4 into a list
	file_list = glob.glob("*.mp4") 

	for inputfile in file_list:
		if os.path.exists(inputfile.replace('.mp4','.wav',1)) == False:
			subprocess.call(['ffmpeg', '-i', inputfile, inputfile.replace('.mp4','.wav',1)])
			subprocess.call(['mv', inputfile , "mp4"])

	wav_files = glob.glob("*.wav")

	for l in wav_files: 
		if os.path.exists(l.replace('.wav','.mp3',1)) == False:
			subprocess.call(['lame', '-h', l, l.replace('.wav','.mp3',1)])

	mp3_files = glob.glob("*.mp3")
	for n in mp3_files:
		subprocess.call(['mv',n, "mp3"])
			
	for w in wav_files:
		os.remove(w)

else:
	print "Path not found. Exiting."

