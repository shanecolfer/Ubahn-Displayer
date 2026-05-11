"""Entry point for ubahn_displayer."""

from datetime import datetime
import os
import sys
import time

import dateutil.parser
from .cli import main
import requests


def search_stops(query):
    response = requests.get(f"https://v6.bvg.transport.rest/locations?query={query}&results=5&stops=true&addresses=false&poi=false")
    return response.json()


def select_stop():
    while True:
        sys.stdout.write('\033[2J\033[H')
        sys.stdout.write('\n\033[1;97m  S-Bahn Departures\033[0m\n\n')
        sys.stdout.write('\033[1;37m  Search for a stop:\033[0m\n\n')
        sys.stdout.write('\033[33;1m  > \033[0m')
        sys.stdout.flush()

        query = input().strip()
        if not query:
            continue

        sys.stdout.write('\033[2J\033[H')
        sys.stdout.write('\n\033[1;97m  S-Bahn Departures\033[0m\n\n')
        sys.stdout.write(f'\033[2;37m  Searching for "{query}"...\033[0m\n')
        sys.stdout.flush()

        stops = [s for s in search_stops(query) if s.get("type") == "stop"]

        if not stops:
            sys.stdout.write('\n\033[31m  No stops found. Press enter to try again.\033[0m\n')
            sys.stdout.flush()
            input()
            continue

        sys.stdout.write('\033[2J\033[H')
        sys.stdout.write('\n\033[1;97m  S-Bahn Departures\033[0m\n\n')
        sys.stdout.write('\033[1;37m  Select a stop:\033[0m\n\n')
        for i, stop in enumerate(stops):
            sys.stdout.write(f'\033[33;1m  {i + 1}.  \033[0m{stop["name"]}\n\n')
        sys.stdout.write('\033[1;37m  > \033[0m')
        sys.stdout.flush()

        choice = input().strip()
        if choice.isdigit() and 1 <= int(choice) <= len(stops):
            return stops[int(choice) - 1]


def get_platform_direction(departures):
    platforms = {}
    for d in departures:
        p = d.get("platform") or d.get("plannedPlatform")
        if p:
            platforms.setdefault(p, [])
    platform_list = sorted(platforms.keys())
    if len(platform_list) >= 2:
        return platform_list[1], platform_list[0]
    return platform_list[0] if platform_list else None, None


def minutes_until(when_str):
    when = dateutil.parser.isoparse(when_str)
    now = datetime.now(tz=when.tzinfo)
    return int((when - now).total_seconds() / 60)


if __name__ == "__main__":
    main()

    stop = select_stop()
    stop_id = stop["id"]
    stop_name = stop["name"]

    last_fetch = 0
    departures = []
    north_platform = None
    south_platform = None

    while True:

        now = time.time()
        if now - last_fetch >= 2:
            response = requests.get(f"https://v6.bvg.transport.rest/stops/{stop_id}/departures?results=20").json()
            departures = response.get("departures", [])
            if north_platform is None:
                north_platform, south_platform = get_platform_direction(departures)
            last_fetch = now

        northbound = [d for d in departures if (d.get("platform") or d.get("plannedPlatform")) == north_platform and not d.get("cancelled")][:2]
        southbound = [d for d in departures if (d.get("platform") or d.get("plannedPlatform")) == south_platform and not d.get("cancelled")][:2]

        out = '\033[2J\033[H'
        out += f'\n\033[1;97m  {stop_name}\033[0m\n\n'

        for label, trains in [("North", northbound), ("South", southbound)]:
            out += f'\033[1;37m  ── {label} ──\033[0m\n\n'
            for departure in trains:
                when = departure["when"] or departure["plannedWhen"]
                diff = minutes_until(when)
                line = departure["line"]["name"]
                direction = departure["direction"]
                delay = departure.get("delay") or 0
                alerts = [r["text"] for r in departure.get("remarks", []) if r["type"] in ("status", "warning")]

                time_str = f"{diff} min" if diff > 0 else ""
                delay_str = f'\033[31m  +{delay//60}m\033[33;1m' if delay > 0 else ""
                style = '\033[33;1;5m' if diff <= 0 else '\033[33;1m'
                out += f'{style}  {line:<5}{direction:<38}{time_str:<10}{delay_str}\033[0m\n'

                for alert in alerts:
                    out += f'\033[31m    ⚠ {alert}\033[0m\n'
                out += '\n'

        sys.stdout.write(out)
        sys.stdout.flush()

        time.sleep(0.1)
