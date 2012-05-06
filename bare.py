#!/usr/bin/env python3

# Copyright 2012 Joey Ezechiëls (joey.ezechiels@gmail.com)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os.path, sys, re, glob, shutil, argparse

if not ('-h' in sys.argv or '--help' in sys.argv) \
        and not ('-p' in sys.argv and '-fn' in sys.argv):
    # Incorrect or no args given, so print help, then exit
    os.system('{0} --help'.format(sys.argv[0]))
    exit()

parser = argparse.ArgumentParser(
    description='Batch renames (bares) files based on search/replace '
    + 'patterns. For each specified file visited, every supplied '
    + 'pattern is checked for applicability, and if such a pattern '
    + 'is indeed applicable, the filename is changed accordingly. '
    + 'By default, before any filenames are changed, a list of changes '
    + 'is printed and the user is asked for confirmation.')

parser.add_argument('-p', nargs='+', metavar='P', type=str, dest='patterns',
                    help='the search/replace pattern(s) to use. The '
                    + 'format per pattern is <search regex>/'
                    + '<replacement string>. A search pattern terminating '
                    + 'in a slash is interpreted to mean deletion of the '
                    + 'matching parts from any matching filenames. Patterns '
                    + 'are seperated by whitespace, and act on all applicable '
                    + 'filenames.')
parser.add_argument('-fn', nargs='+', metavar='F', type=str, dest='filenames',
                    help='the file(s) to process. Globbing is supported.')
parser.add_argument('-cs', dest='case_sensitive', default=False,
                    action='store_const', const=True,
                    help='Make the search pattern match in a case sensitive '
                    + 'manner. By default it is case insensitive.')
parser.add_argument('-f', dest='force_perform_renames', default=False,
                    action='store_const', const=True,
                    help='Forces any changes to be applied without any '
                    + 'confirmation messages to be printed. The list of '
                    + 'changed is still printed.')

args = parser.parse_args()

class FileItem:
    def __init__(self, filepath):
        abspath = lambda fp: os.path.abspath(os.path.expanduser(fp))
        self.path = abspath(filepath)
        self.parent, self.name = os.path.split(self.path)
    def __repr__(self):
        return self.path

def ensure_list(xs):
    '''Ensures XS may be treated as a list.'''
    return xs if xs else []

def make_seare_tuples(xs):
    '''Turns the iterable XS into a list of
    (<compiled SEArch regex>, <REplace pattern>) tuples.'''
    patten_tuples = [tuple(pat.split('/')) for pat in xs]
    if args.case_sensitive:
        compile_func = re.compile
    else:
        compile_func = lambda p: re.compile(p, flags=re.I)
    search_patterns = map(compile_func, map(lambda x: x[0], patten_tuples))
    replace_patterns = map(lambda x: x[1], patten_tuples)
    return [x for x in zip(search_patterns, replace_patterns)]

def user_confirmation():
    ask_question = lambda: input('Proceed? [y/N] ').lower()
    answer = ask_question()
    while answer not in  ['y', 'yes', 'n', 'no', '']:
        answer = ask_question()
    return answer in ['y', 'yes']

def perform_renames(list_of_renames):
    '''Tries to perform the changes indicated in LIST_OF_RENAMES.
    If a given file can't be renamed, a warning is emitted and
    the file is skipped.'''
    for old_fp, new_fp in list_of_renames:
        if os.path.exists(old_fp): shutil.move(old_fp, new_fp)
        else: print("[WARN] {} not found; skipping.".format(old_fp))

def print_rename_feedback(num_subtitutions, fileitem, new_filepath):
    if num_subtitutions == 1:
        print('{} will be renamed to {} (1 substitution)'
              .format(fileitem.path, new_filepath))
    elif num_subtitutions > 1:
        print('{} will be renamed to {} ({} substitutions)'
              .format(fileitem.path, new_filepath, num_subs))

seare_tuples = make_seare_tuples(args.patterns)
renames = []

for fi in [FileItem(fp) for fp in ensure_list(args.filenames)]:
    for csrchpat, reppat in seare_tuples:
        new_filename, num_subs = re.subn(csrchpat, reppat, fi.name)
        new_filepath = os.path.join(fi.parent, new_filename)

        if num_subs >= 1:
            print_rename_feedback(num_subs, fi, new_filepath)
            renames += [(fi.path, new_filepath)]

if args.force_perform_renames:
    perform_renames(renames)
else:
    if len(renames) == 0:
        print('No search pattern matches.')
        exit()
    if user_confirmation():
        perform_renames(renames)
    else: print('Cancelling.')
