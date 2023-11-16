# f2-migration-db
Database for tracking the migration of content from old repository to new.

## Preparing Data

The following command converts a migration-utils metadata CSV (not included here due to size) into files representing repository items and their constituent parts (i.e. pages).

```
% python3 data-prep.py <inputfile>
```

## Loading Data to SQLite3

To load the data tables into a sqlite database, use the following commands to parse the input CSV data and create a table from each input file: 

```% sqlite3 ~/Desktop/test.sqlite
SQLite version 3.39.5 2022-10-14 20:58:05
Enter ".help" for usage hints.
sqlite> .import --csv collections.csv collections
sqlite> .import --csv items.csv items
sqlite> .import --csv componenets.csv components
```
Note: The collections file included in this repository was not created by the data-prep.py script, but was exported from Solr directly to get collection pids and titles.
