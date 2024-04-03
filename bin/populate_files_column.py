#!/usr/bin/env python3

import csv
import pathlib
import sys


class ArchelonBatchCsv:

    def __init__(self, path):
        self.path = path
        with open(self.path, 'r') as handle:
            self.data = [row for row in csv.DictReader(handle)]

    def add_files_column(self, filelist):
        for row in self.data:
            if not 'FILES' in row:
                row['FILES'] = ';'.join(
                    sorted([f for f in filelist if f.startswith(row['Identifier'])])
                    )

    def read_files_column(self):
        files = []
        for row in self.data:
            files.extend([ImageAsset(f) for f in row['FILES'].split(';')])
        return files

    def write(self):
        fieldnames = list(set().union(*[d.keys() for d in self.data]))
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        for row in self.data:
            writer.writerow(row)


class FileList:

    def __init__(self, path):
        with open(path) as handle:
            self.files = set([pathlib.Path(f).stem for f in handle.read().split('\n')])


class ImageAsset:

    def __init__(self, path):
        self.path = pathlib.Path(path)
        self.umdm = self.path.parts[0]
        self.umam = self.path.parts[1]
        self.filename = self.path.name
        self.base = self.path.stem
        self.ext  = self.path.suffix
        #print(self.umdm, self.umam, self.base, self.ext)


if __name__ == "__main__":
    inputcsv = ArchelonBatchCsv(sys.argv[1])
    filelist = FileList(sys.argv[2])

    for row in inputcsv.data:
        files = [pathlib.Path(f) for f in row['FILES'].split(';')]
        output = []
        for path in files:
            if path.stem in filelist.files:
                output.append(str(path)[:-4] + '.tif')
            else:
                output.append(str(path))
        row['FILES'] = ';'.join(output)

    inputcsv.write()

'''
    print(f'{len(assets)} assets listed in {sys.argv[1]}')
    with open(sys.argv[2]) as handle:
        filelist = [f.strip() for f in handle.readlines()]
        print(f'{len(filelist)} files in {sys.argv[2]}')
        files = {pathlib.Path(f).stem: f for f in filelist}
        for asset in assets:
            if asset.base not in files:
                print(asset.umdm, asset.filename)
'''