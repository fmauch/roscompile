import argparse
from zipfile_interface import get_test_cases
from roscompile.package import Package
from roscompile.main import roscompile_one
import os

def get_files(root):
    the_files = []
    for folder, _, files in os.walk(root):
        short_folder = folder.replace(root, '')
        for fn in files:
            the_files.append(os.path.join(short_folder, fn))
    return the_files

parser = argparse.ArgumentParser()
parser.add_argument('zipfile')
args = parser.parse_args()
cases = get_test_cases(args.zipfile)

for package, case in cases.iteritems():
    case.write()
    pkg = Package(case.get_input_root())
    roscompile_one(pkg)
    output_files = set(case.output_files.keys())
    for fn in get_files(case.get_input_root()):
        if not fn in output_files:
            print 'Should have deleted %s' % fn
            continue
        output_files.remove(fn)
    for fn in output_files:
        print 'Failed to generate %s' % fn
