"""
    Creator: Caleb Shortt, Sept 2016

    Keyword Search.

    Given a root directory to start with and a list of keywords, this script opens up every subfile/subdirectory and
    tries to finds any instances of any of the specified keywords.

    Returns the keyword(s) found and filepath for each discovery

    NOTE: This script recursively traverses the filesystem from the given root directory. It may be slow based on what
            root you give it.

"""

import sys
import os


class Engine(object):

    keywords = []
    discoveries = []
    root = '~/'

    # will filter out ANY file with the text in the name or in its content (wide sweep)
    filters = []

    def __init__(self, filepath, root, filter_filepath=None):

        if root:
            self.root = root

        lines = []
        try:
            with open(filepath, 'r') as f:
                lines = f.readlines()
        except Exception:
            print "Could not open file %s" % (filepath, )
        self.keywords = [str(l).strip() for l in lines]

        if filter_filepath:
            f_data = []
            try:
                with open(filter_filepath, 'r') as f:
                    f_data = f.readlines()
            except Exception:
                print "Could not open file %s" % (filter_filepath, )
            self.filters = [str(l).strip() for l in f_data]

    def is_filtered(self, s):
        for fkw in self.filters:
            if fkw in s:
                return True
        return False

    def check_string(self, s):
        findings = []
        for kw in self.keywords:
            if kw in s and not self.is_filtered(s):
                findings.append(kw)

        return findings

    def print_finding(self, kw_list, file_name):
        kws = ', '.join(kw_list)
        print "%s: \t%s" % (kws, file_name)

    def execute(self):
        for root, dirs, files in os.walk(self.root):
            for name in files:

                file_path = os.path.join(root, name)

                # Check if name contains keyword
                findings = self.check_string(name)

                if len(findings) > 0:
                    self.print_finding(findings, file_path)

                # Check file contents
                contents = ''
                try:
                    with open(file_path, 'r') as f:
                        contents = f.read()
                except Exception, e:
                    print "Could not open %s" % (file_path, )
                    print str(e)

                findings = self.check_string(contents)
                if len(findings) > 0:
                    self.print_finding(findings, file_path)


def print_usage():
    print "Usage: ./base.py <root_directory> <keywordlist_file> [optional: <filterfile>]\n"


def main(args):

    if len(args) < 3 or len(args) > 4:
        print "Invalid Input"
        print_usage()
        return

    root = str(args[1])
    filepath = str(args[2])

    filterpath = None
    if len(args) == 4:
        filterpath = args[3]

    engine = Engine(filepath, root, filterpath)
    engine.execute()

if __name__ == "__main__":
    main(sys.argv)
