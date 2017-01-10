#!/usr/bin/env python 

import os
import glob 
import subprocess
import argparse
import shutil

parser = argparse.ArgumentParser()
parser.add_argument("dir", help = "Input directory")

args = parser.parse_args()

def convert2wav(inputfile,logdir='log'):
	if not os.path.exists(logdir):
		os.mkdir(logdir)
	extension = os.path.splitext(inputfile)[1]
	if os.path.exists(inputfile.replace(extension,'.wav',1)) == False:
		subprocess.call(['ffmpeg', '-i', inputfile, inputfile.replace(extension,'.wav',1)])
		
	shutil.move(inputfile,logdir)

# Make the output directories if they don't exist already 
if not os.path.exists("mp3"):
	os.mkdir("mp3")

if os.path.exists(args.dir):
	os.chdir(args.dir) 

    # get files with extension .mp4 into a list
	mp4_list = glob.glob("*.mp4") 

    # get files with extension .webm into a list
	webm_list = glob.glob("*.webm")
	
    # get files with extension .mkv into a list
	mkv_list = glob.glob("*.mkv")

	for inputfile in mp4_list:
		convert2wav(inputfile)				

	for inputfile in webm_list:
		convert2wav(inputfile)

	for inputfile in mkv_list:
		convert2wav(inputfile)

    # get all WAV files into a list 
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

