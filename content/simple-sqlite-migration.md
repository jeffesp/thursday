Title: Simple SQLite Database Migration
Category: Code
Date: 2019-06-18
Slug: simple-sqlite-db-migration
Authors: Jeff Esp
Summary: A simple SQLite migration script written in Python

I had to write a migration for a SQLite database the other day, and decided
to do some yak-shaving and write the world's simplest db migration utility.
It only migrates one direction, and you have to write migration scripts by
hand. But it seems to work, so here it is.

```python
import sqlite3
import os

def migrate_schema():
    migrations_path = "./migrations"
    # find the database 'user_version'
    data = sqlite3.connect('./db.sqlite3', detect_types=sqlite3.PARSE_DECLTYPES)
    current_version = data.execute("PRAGMA user_version").fetchone()[0]

    # iterate files in schema dir and find right file to start with
    files = sorted([
        f
        for f in os.listdir(migrations_path)
        if os.path.isfile(os.path.join(migrations_path, f))
        and int(os.path.splitext(f)[0]) > current_version
    ], key=lambda file: int(os.path.splitext(f)[0]))

    if len(files) > 0:
        try:
            with data:
                for migration in files:
                    with open(os.path.join(migrations_path, migration)) as f:
                        data.executescript(f.read())
                data.execute(f"PRAGMA user_version = {current_version + 1}").fetchone()
        except sqlite3.Error as err:
            print(f"Could not execute script {migration}:\n{err}")
    else:
        print(f"Database schema up to date at version {current_version}")

```

It looks in the current path for a directory named `migrations` and will run
the files there in number order if the there is named as an integer. This is 
fragile and I'm sure it's going to bite me at some point, but is working so
far. 

The `PRAGMA` stuff could be replaced by a table that keeps track of what the
version, or even has a list of the scripts applied and some tracking data 
about that. For now, `user_version` is going to work fine.
