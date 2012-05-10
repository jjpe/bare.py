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

Note: the script assumes that both the env and python3 binaries are located
      within /usr/bin/. This of course won't work for vanilla Windows (it
      might work for cygwin but I haven't tested that) but it works
      out of the box on distributions such as Ubuntu and Fedora.
