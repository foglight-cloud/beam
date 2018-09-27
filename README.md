# Beam (the client)

This is a python application. Pipe your application logging through it to look for matches against the [foglight](https://foglight.cloud) database.

# Installation

It's just a single script, for now.

Perhaps stick it at `/usr/local/bin/beam` so it's on your path.

Then run:

```
$ pip install -r requirements.txt
$ ./run-my-app.sh | beam

