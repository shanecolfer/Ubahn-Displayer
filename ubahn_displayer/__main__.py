"""Entry point for ubahn_displayer."""

from datetime import datetime
import os
import sys
import time

import dateutil.parser
from .cli import main
import requests

if __name__ == "__main__":
    main()

    last_fetch = 0
    departures = []
    station_name = "S-Bahn"

    while(1):

        now = time.time()
        if now - last_fetch >= 2:
            response = requests.get("https://v6.bvg.transport.rest/stops/900110003/departures?results=20&suburban=true&subway=false&tram=false&bus=false&ferry=false&express=false&regional=false").json()
            departures = response["departures"]
            station_name = departures[0]["stop"]["name"] if departures else "S-Bahn"
            last_fetch = now

        northbound = [d for d in departures if (d.get("platform") or d.get("plannedPlatform")) == "2" and not d.get("cancelled")][:2]
        southbound = [d for d in departures if (d.get("platform") or d.get("plannedPlatform")) == "1" and not d.get("cancelled")][:2]

        out = '\033[2J\033[H'
        out += f'\n\033[1;97m  {station_name}\033[0m\n\n'

        for label, trains in [("North", northbound), ("South", southbound)]:
            out += f'\033[1;37m  ── {label} ──\033[0m\n\n'
            for departure in trains:
                when = departure["when"] or departure["plannedWhen"]
                diff = dateutil.parser.isoparse(when).minute - datetime.now().minute
                line = departure["line"]["name"]
                direction = departure["direction"]
                delay = departure.get("delay") or 0
                alerts = [r["text"] for r in departure.get("remarks", []) if r["type"] in ("status", "warning")]

                time_str = f"{diff} min" if diff != 0 else ""
                delay_str = f'\033[31m  +{delay//60}m\033[33;1m' if delay > 0 else ""
                style = '\033[33;1;5m' if diff == 0 else '\033[33;1m'
                out += f'{style}  {line:<5}{direction:<38}{time_str:<10}{delay_str}\033[0m\n'

                for alert in alerts:
                    out += f'\033[31m    ⚠ {alert}\033[0m\n'
                out += '\n'

        sys.stdout.write(out)
        sys.stdout.flush()

        time.sleep(0.1)
