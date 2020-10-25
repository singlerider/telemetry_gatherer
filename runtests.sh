#!/usr/bin/env bash
./build.sh
docker run -ti cockpit pytest
