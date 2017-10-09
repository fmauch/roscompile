import zipfile
import collections
import os
import tempfile
import shutil

class ROSCompileTestCase:
    def __init__(self, package_name, input_files, output_files):
        self.package_name = package_name
        self.input_files = input_files
        self.output_files = output_files

    def get_input_root(self):
        return os.path.join(tempfile.gettempdir(), self.package_name)

    def write(self):
        base_folder = self.get_input_root()
        if os.path.exists(base_folder):
            shutil.rmtree(base_folder)
        os.mkdir(base_folder)
        for fn, contents in self.input_files.iteritems():
            outfile = os.path.join(base_folder, fn)
            parts = outfile.split(os.sep)
            for i in range(4, len(parts)):
                os.mkdir(os.sep.join(parts[:i]))
            with open(outfile, 'w') as f:
                f.write(contents)

    def __repr__(self):
        return 'TestCase(%s)' % self.package_name

def get_test_cases(zip_filename):
    file_data = collections.defaultdict(lambda: collections.defaultdict(dict))
    zf = zipfile.ZipFile(zip_filename)
    for file in zf.filelist:
        if file.compress_type == 0:
            continue
        parts = file.filename.split(os.path.sep)
        io = parts[0]
        package = parts[1]
        path = apply(os.path.join, parts[2:])
        file_data[package][io][path] = zf.read(file)

    test_data = {}
    for package, D in file_data.iteritems():
        test_data[package] = ROSCompileTestCase(package, D['input'], D['output'])
    return test_data
