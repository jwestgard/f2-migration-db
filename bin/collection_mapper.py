#!/usr/bin/env python3

import csv
import sys

with open(sys.argv[1]) as handle:
    collections = {row['pid']: row for row in csv.DictReader(handle)}

with open(sys.argv[2]) as inputhandle, open(sys.argv[3], 'w+') as outputhandle:
    reader = csv.DictReader(inputhandle)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outputhandle, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        pids = row['F2 COLLECTIONS'].split('|')
        # print(f'before: {pids}')
        while '' in pids:
            pids.remove('')
        if len(pids) > 1:
            if 'umd:3392' in pids:
                pids.remove('umd:3392')
            if 'umd:15237' in pids:
                pids = ['umd:15237']
        if len(pids) > 1:
            #print(f'after: {pids}')
            if row['F2 STATUS'] != 'Deleted':
                row['F2 COLLECTIONS'] = '|'.join(pids)
        writer.writerow(row)