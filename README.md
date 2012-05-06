1. Purpose:

The script fulfills a simple itch I've been having for a while:
Make it easy to batch rename large amounts of files by specifying
regexes as search pattens, and an option to provide replacement strings.
As a free feature, it also means you can remove parts of a filename,
simply by not specifying a replacement string.

2. Requirements

All the script needs to run is Python 3.2+. This requirement is due to the
fact that argparse, which is used for parsing the cli arguments, was only
introduced in Python 3.2.

Note: the script assumes that the python3 binary is located within /usr/bin/.
      This of course won't work for OS X, Windows and custom Linux installs, 
      but it works out of the box on disto's such as Ubuntu and friends, and
      Fedora.