# Import modules from parent folder
import os
import sys
CURRENT_FOLDER = os.path.dirname (__file__)
PARENT_FOLDER = os.path.dirname (CURRENT_FOLDER)
sys.path.append (PARENT_FOLDER)

from manga_downloader import MangaDownloader

downloader = MangaDownloader ()
downloader.download ()