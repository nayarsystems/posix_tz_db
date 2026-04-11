#!/usr/bin/env python

import sys
import argparse
import json
import zoneinfo

ZONES_DIR = "/usr/share/zoneinfo/"
ZONES = sorted(zoneinfo.available_timezones())
if "localtime" in ZONES:
    ZONES.remove("localtime")

def get_tz_string(timezone):
    data = open(ZONES_DIR + timezone, "rb").read().split(b"\n")[-2]
    return data.decode("utf-8")


def make_timezones_dict():
    result = {}
    for timezone in ZONES:
        timezone = timezone.strip()
        result[timezone] = get_tz_string(timezone)
    return result


def print_csv(timezones_dict):
    for name, tz in timezones_dict.items():
        print('"{}","{}"'.format(name, tz))


def print_json(timezones_dict):
    json.dump(timezones_dict, sys.stdout, indent=0, sort_keys=True, separators=(",", ":"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generates POSIX timezones strings reading data from " + ZONES_DIR)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-j", "--json", action="store_true", help="outputs JSON")
    group.add_argument("-c", "--csv", action="store_true", help="outputs CSV")
    data = parser.parse_args()

    timezones = make_timezones_dict()

    if data.json:
        print_json(timezones)
    else:
        print_csv(timezones)
