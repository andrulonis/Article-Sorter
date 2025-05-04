# Description
This is a script for sorting articles out of a directory based on entries in a CSV file. Some semi-hardcoded solutions (mostly the directory changes) are needed due to the limitations when creating applications for Mac and also for the user to have no options to break the code and have easier use (it was preferred to have an executable/shortcut on desktop for quick access instead of calling from terminal).

# article-sorter.py
The base version of the app that assumes the folder with the article files is placed right next to the scripts executable on the desktop.

# article-sorter-dbox.py
Upgraded version that allows to directly download from an open DropBox folder in order to download only the article files that are needed rather than relying on downloading the entire folder before sorting it.
