# -*- coding: utf-8 -*-

from __future__ import print_function
import time
from django.conf import settings
from watchtower.db import orm, influx
from watchtower.conf import DBS


def dispatch(hits, events=None, verbosity=0):
    global DBS
    for key in DBS:
        db = DBS[key]
        if "hits_db" in db:
            if db["type"] == "django":
                try:
                    djdb = db["hits_db"]
                except:
                    print("Database ", db, "not found")
                orm.write(djdb, hits, verbosity)
            elif db["type"] == "influxdb":
                influx.process_hits(hits)
                if events is not None:
                    influx.process_events(events)
                    print_summary(num_events=len(events), verbosity=verbosity)
    print_summary(num_hits=len(hits))


def print_summary(num_hits=0, num_events=0, verbosity=0):
    if verbosity > 0:
        if num_hits > 0:
            s = "s"
            if num_hits == 1:
                s = ""
            t = time.strftime('%X')
            print(t, ":", "processed", num_hits, "hit" + s)
    if num_events > 0:
        s = "s"
        if num_events == 1:
            s = ""
        t = time.strftime('%X')
        print(t, ":", "processed", num_events, "event" + s)
