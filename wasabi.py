from __future__ import unicode_literals
from os.path import expanduser
from shutil import copyfile
from datetime import datetime

import youtube_dl
import sqlite3
import os
import argparse
import sys
import subprocess

home = expanduser("~") 
temp_db_path = os.path.join(os.getcwd(),str(datetime.utcnow()))

def _run(cmd):
    p = subprocess.Popen([cmd], shell=True, stdout=subprocess.PIPE)
    result = p.communicate()[0][0:-2]
    return str(result, 'utf-8')

def _get_firefox_history_db():
    if sys.platform == 'darwin':
        cmd = f"ls -d {home}/Library/Application\ Support/Firefox/Profiles/*.default/"
        firefox_profile_path = _run(cmd)
    
    elif sys.platform in ['linux', 'linux2']:
        cmd = f"ls -d {home}/.mozilla/firefox/*.default/"
        firefox_profile_path = _run(cmd)

    elif sys.platform == 'win32':  # Untested
        import glob
        APPDATA = os.getenv('APPDATA')
        firefox_profile = "%s\\Mozilla\\Firefox\\Profiles\\" % APPDATA
        pattern = firefox_profile + "*default*"
        firefox_profile_path = glob.glob(pattern)[0]    

    else:
        print(f"System {sys.platform} not supported")
        sys.exit(2)

    return firefox_profile_path + '/places.sqlite'

def _get_chrome_history_db():
	if sys.platform == 'darwin':
		return f"{home}/Library/Application Support/Google/Chrome/Default/History"
	elif sys.platform in ['linux', 'linux2']:
		return f"{home}/.config/google-chrome/Default/History"
	else:
		# TODO: win32
		print(f"System {sys.platform} not supported")
		sys.exit(2)

def _get_brave_history_db():
	if sys.platform == 'darwin':
		return f"{home}/Library/Application Support/BraveSoftware/BraveSoftware/Default/History"
	elif sys.platform in ['linux', 'linux2']:
		return f"{home}/.config/BraveSoftware/Brave-Browser/Default/History"
	else:
		# TODO: win32
		print(f"System {sys.platform} not supported")
		sys.exit(2)

browser_dictionary = {
	'firefox' : [_get_firefox_history_db(), "moz_places"] ,
	'chrome' : [_get_chrome_history_db(), "urls"],
	'brave'  : [_get_brave_history_db(), "urls"]
    }

parser = argparse.ArgumentParser()

parser.add_argument('browser', help = "chrome for Chrome, firefox for Firefox, brave for Brave.")
parser.add_argument('-k','--key', default='', help = "Only fetch titles containing this search key.")
parser.add_argument('-dr','--dryrun', action='store_true' ,help = "Show selected titles. Do not download or convert.")

args = parser.parse_args()

try:
	database_path = browser_dictionary[args.browser][0]
	table_name = browser_dictionary[args.browser][1]
except KeyError:
	sys.exit("Browser not supported. Type firefox, chrome or brave.")

select_query = "select * from " + table_name 
select_query_key = "select * from " + table_name + " where title like ?"

if not os.path.exists(database_path):
    print (f"File not found: {database_path}\n")
    sys.exit(1)

copyfile(database_path,temp_db_path)

try:
    conn = sqlite3.connect(temp_db_path)
except:
    sys.exit("Cannot open database.\n")

c = conn.cursor()

if args.key:
    c.execute(select_query_key,('%'+args.key+'%',))
else:
    c.execute(select_query)

history_list = c.fetchall()

conn.close() 
os.remove(temp_db_path)
print('Removing temporary db file: ',temp_db_path)

ydl_options = {
    'outtmpl': '%(title)s-%(id)s.%(ext)s',
    'format': 'bestaudio',
    'postprocessors': [{
    'key': 'FFmpegExtractAudio',
    'preferredcodec': 'mp3',
    'preferredquality': '320',
    }],
    'continuedl': True,
    'restrictfilenames':True
    }

with youtube_dl.YoutubeDL(ydl_options) as ydl:
    for tuple_item in history_list:
        if "youtube.com" in tuple_item[1] and "watch?" in os.path.basename(tuple_item[1]):
            video_url = tuple_item[1]
            if args.dryrun:
                print (tuple_item[2])
            else:
                try:
                    result = ydl.download([video_url])
                except:
                    continue
