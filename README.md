wasabi
======

Python command line utility that extracts MP3 audio tracks
from MP4 video files downloaded from the Internet. 

It relies on the following 3rd party packages: 

- ffmpeg http://ffmpeg.org 
- lame http://lame.sourceforge.net 
 
which must be installed on your machine before you can run Wasabi. 

This is how Wasabi works: assuming all your MP4 video files are in
a directory 'input folder': 

	python wasabi.py <input folder>

This will create an mp3 folder with the audio files created by 
Wasabi and an mp4 folder with the original mp4 files, both as 
sub-folders of input_folder .

Platforms
--------------
* GNU/Linux 
* MAC OS X 

Contributors
--------------
* Salvatore Rinaldo - Wrote the initial version. 
