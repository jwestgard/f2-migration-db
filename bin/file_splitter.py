#!/usr/bin/env python3

import csv
from lxml import etree
import pathlib
import requests
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
        output = []
        for row in self.data:
            files = [f for f in row['FILES'].split('|') if f != ""]
            output.extend([ImageAsset(f) for f in files])
        return output

    def write(self):
        fieldnames = list(set().union(*[d.keys() for d in self.data]))
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        for row in self.data:
            writer.writerow(row)


class Component:

    def __init__(self, sequence, pid):
        pass


class ImageAsset:

    def __init__(self, n, path):
        self.seq = n
        self.path = pathlib.Path(path)
        self.umdm = self.path.parts[0]
        self.umam = self.path.parts[1].replace('_', ':')
        self.filename = self.path.name
        self.base = self.path.stem
        self.ext  = self.path.suffix.replace('.','').upper()
        #print(self.umdm, self.umam, self.base, self.ext)

    def __lt__(self, other): 
        return self.seq < other.seq


def get_page_sort(path):

    ns = {"mets": "http://www.loc.gov/METS/"}
    filesec = '//mets:mets/mets:fileSec/mets:fileGrp/mets:file'
    structmap = '//mets:mets/mets:structMap/mets:div[@ID="images"]'
    file_to_pid = {}
    results = []

    with open(path) as handle:
        tree = etree.parse(handle)

    for node in tree.xpath(filesec, namespaces=ns):
        fileid = node.get('ID')
        pid = node.xpath('mets:FLocat', namespaces=ns)[0].get(
            '{http://www.w3.org/1999/xlink}href'
            )
        file_to_pid[fileid] = pid

    for node in tree.xpath(structmap, namespaces=ns):
        for child in node:
            seq = int(child.get('ORDER'))
            label = child.get('LABEL')
            fileid = child.xpath('mets:div/mets:fptr', namespaces=ns)[0].get('FILEID')
            results.append((seq, label, file_to_pid[fileid]))

    return sorted(results)


def main():

    inputcsv = ArchelonBatchCsv(sys.argv[1])
    fieldnames = ['umdm', 'seq', 'umam', 'basename', 'ext', 'path']
    with open('output.csv', 'w+') as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()

        for row in inputcsv.data:
            structure = StructMap(row['umdm'])
            filelist = [f for f in row['FILES'].split('|') if f != ""]
            assets = [ImageAsset(n, f) for n, f in enumerate(filelist)]
            sequence = {}
            for a in assets:
                sequence.setdefault(a.umam, []).append(a)
            for k, v in sequence.items():
                if len(v) == 1:
                    continue
                elif len(v) == 2:
                    sequence[k] = [f for f in v if f.base != 'image']
                else:
                    print("component with three images!")

            all_images = []
            for vals in sequence.values():
                all_images.extend(vals)
            for n, f in enumerate(sorted(all_images), 1):
                writer.writerow({
                    'umdm':     row['F2 PID'],
                    'seq':      n,
                    'umam':     f.umam, 
                    'basename': f.base, 
                    'ext':      f.ext,
                    'path':     f.path
                    })


if __name__ == "__main__":
    print(get_page_sort(sys.argv[1]))