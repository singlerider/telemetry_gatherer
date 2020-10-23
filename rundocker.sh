#!/usr/bin/env bash
touch db.sqlite3
docker run -ti -v $(pwd)/db.sqlite3:/app/db.sqlite3 -p 8000:8000 cockpit
