"""Entry point for ubahn_displayer."""

from datetime import datetime
import time

import dateutil.parser
import re
from .cli import main
import requests

import os

if __name__ == "__main__":
    main()

    UP = '\033[1A'
    CLEAR = '\x1b[2K'

    print(UP, end=CLEAR)
    
    while(1):

        x = requests.get("https://v5.bvg.transport.rest/stops/900000016201/departures?results=2").json()

        firstArrivalDiffInMinutes = dateutil.parser.isoparse(x[0]["when"]).minute - datetime.now().minute
        secondArrivalDiffInMinutes = dateutil.parser.isoparse(x[1]["when"]).minute - datetime.now().minute

        #Print 1st arrival
        if(firstArrivalDiffInMinutes != 0):
            print(f'\033[33;1;1m\n{x[0]["direction"]}\t\t{firstArrivalDiffInMinutes}\033[0m')
        else:
            print(f'\033[33;1;5m\n{x[0]["direction"]}\033[0m')
        
        #Print 2nd arrival
        if(secondArrivalDiffInMinutes != 0):
            print(f'\033[33;1;1m{x[1]["direction"]}\t\t{secondArrivalDiffInMinutes}\033[0m')
        else:
            print(f'\033[33;1;5m\n{x[0]["direction"]}\033[0m')

        #Print warning text
        # print(re.sub('<[^<]+?>', '', f'\n{x[0]["remarks"][2]["text"]}')) needs to be dynamically accessed

        print(UP, end=CLEAR)
        print(UP, end=CLEAR)
        print(UP, end=CLEAR)
        print(UP, end=CLEAR)

        time.sleep(2)

