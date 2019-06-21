Title: World's simplest database migration utility
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
import os
```

The `PRAGMA` stuff could be replaced by a table that keeps track of what the
version, or has a list of the scripts applied. For now, `user_version` is
going to work fine.
