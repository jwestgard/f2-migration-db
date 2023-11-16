#!/usr/bin/env python3

import csv
import os
import sys

inputhandle = open(sys.argv[1])
umdmshandle = open('umdms.csv', 'w+')
umamshandle = open('umams.csv', 'w+')
fileshandle = open('files.csv', 'w+')


def parse_identifier_field(inputdata):
    ids = inputdata.split('|')
    handle = next((i for i in ids if i.startswith('hdl:')), None)
    pid = next((i for i in ids if i.startswith('umd:')), None)
    return handle


def parse_filepath(inputdata):
    dirs = inputdata.split('/')
    if len(dirs) > 1:
        pid = dirs[1].replace('_', ':')
        base, ext = os.path.splitext(dirs[-1])
        return pid, base
    else:
        return ('', '')



def main():

    umdmfields = ['collection', 'status', 'type', 'pid', 'handle', 'title']
    umamfields = ['pid', 'umdm_pid', 'filename']

    umdms = csv.DictWriter(umdmshandle, fieldnames=umdmfields)
    umams = csv.DictWriter(umamshandle, fieldnames=umamfields)
    umdms.writeheader()
    umams.writeheader()

    for row in csv.DictReader(inputhandle):
        umdm_row = {
               'handle': parse_identifier_field(row['Identifier']),
           'collection': row['F2 COLLECTIONS'],
                  'pid': row['F2 PID'],
                 'type': row['F2 TYPE'],
               'status': row['F2 STATUS'],
                'title': row['Title']
            }
        if umdm_row['status'] == 'Complete':
            umdms.writerow(umdm_row)

        for filepath in row['FILES'].split(';'):
            pid, filename = parse_filepath(filepath)
            umam_row = {
                'pid': pid,
                'umdm_pid': umdm_row['pid'],
                'filename': filename
                }
            umams.writerow(umam_row)


if __name__ == "__main__":
    main()
