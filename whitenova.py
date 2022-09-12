# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    whitenova.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jre-gonz <jre-gonz@student.42madrid.com    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/09/12 15:37:56 by jre-gonz          #+#    #+#              #
#    Updated: 2022/09/12 22:59:12 by jre-gonz         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from Nanoshell import NanoShell
from AsciiGraph import AsciiGraph
from API42 import API42

import pytz
from datetime import datetime as dt, timedelta, timezone
from math import ceil

class WhiteNova():

    def __init__(self):
        self.api = API42()

    def _t_now(self):
        d = dt.now()
        pytz.timezone("UTC").localize(d)
        return d

    def _time_now(self, format:str = "%Y-%m-%d") -> str:
        return self._t_now().strftime(format)

    def _stodate(self, date: str, format: str = "%Y-%m-%dT%H:%M:%S.%fZ"):
        d = dt.strptime(date, format)
        pytz.timezone("UTC").localize(d)
        return d

    def _dateformat_date(self, date, format: str = "%H:%M:%S %d-%m-%Y") -> str:
        return date.replace(tzinfo=timezone.utc).astimezone(tz=pytz.timezone("Europe/Madrid")).strftime(format)

    def _dateformat(self, date: str, format: str = "%H:%M:%S %d-%m-%Y") -> str:
        return self._dateformat_date(self._stodate(date), format)

    def _whitenova_period(self, offset: int = 0) -> dict:
        REF = self._stodate("2022-07-29 8:00:00", "%Y-%m-%d %H:%M:%S") # ! UTC time
        P = timedelta(days=14)
        now = self._t_now() - offset * P
        time_between = now - REF
        periods = time_between // P
        start = REF + periods * P
        end = REF + (periods + 1) * P
        start_str = start.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        end_str = end.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        return {"start": start, "end": end, "start_str": start_str, "end_str": end_str}

    def _parse(self, user: str, period: dict, locations: list, corrections: list, full_report: bool = True) -> str:
        TIME_FORMAT = "%H:%M %d-%m"
        days = ceil((period['end'] - period['start']).total_seconds() / 3600 / 24)

        s = f"{user}'s {'whitenova' if days == 14 else str(days) + ' days period'}: (Time zone: Madrid)\n"
        s = f"{s}  - Start: {self._dateformat(period.get('start_str'), TIME_FORMAT)}\n"
        s = f"{s}  - End: {self._dateformat(period.get('end_str'), TIME_FORMAT)}\n\n"
        
        total_time = timedelta()
        time_days = [timedelta() for _ in range(days)]

        FIRST_DAY = period["start"].replace(hour = 0, minute = 0, second = 0, microsecond = 0)
        not_acurate = True # TODO Remove
        for l in locations:
            end_str = l['end_at']
            if l['end_at'] == None:
                end_str = self._time_now("%Y-%m-%dT%H:%M:%S.%fZ")
            start_date = self._stodate(l['begin_at'])
            end_date = self._stodate(end_str)

            amount_time = end_date - start_date
            
            # if full_report:
            s = f"{s}{self._dateformat(l['begin_at'], TIME_FORMAT)},"
            s = f"{s} -- {self._dateformat(end_str, TIME_FORMAT)}"
            s = f"{s} -> {amount_time}\n"

            # Time calculation
            total_time = total_time + amount_time

            day_end = (end_date.replace(hour = 0, minute = 0, second = 0, microsecond = 0) - FIRST_DAY).days

            time_days[day_end] = time_days[day_end] + (amount_time)

        s = f"{s}\nTotal time: {total_time}\n\n"

        keys = []
        values = []
        for d in time_days:
            values.append(round(d.total_seconds() / 3600))
        for i in range(days):
            date = FIRST_DAY + timedelta(days=i)
            keys.append(date.strftime('%d-%m'))
        graph = AsciiGraph.plot([{"values": values, "color": AsciiGraph.COLORS["YELLOW"]}], keys, dx=7)
        s = f"{s}{graph}\n\n"
        if not_acurate: # ! remove
            s = f"{s}****** Graph with errors ******\n\n"

        # Corrections
        s = s + f"Corrections: {len(corrections)}\n\n"
        if full_report:
            s = f"{s}{self._corrections_planned(corrections)}\n"
        s = f"{s}The official metrics are the only ones that are correct. This is just an approximation.\n"
        return s

    def _corrections_planned(cls, info: list):
        if len(info) == 0:
            return "Nothing to correct here :S\n"
        s = ""
        for correction in info:
            corrector = f"{correction['corrector']['login']} ({correction['corrector']['id']})"
            correcteds = ""
            for corrected in correction['team']['users']:
                correcteds = f"{correcteds}    - {corrected['login']} ({corrected['id']}){' Leader' if corrected['leader'] else ''}\n"
            project_name = correction['team']['project_gitlab_path']
            s = f"{s}******************************\n"
            s = f"{s} - Project name: {project_name}\n"
            s = f"{s} - Corrector: {corrector}\n"
            s = f"{s} - Correcteds:\n{correcteds}"
            s = f"{s} - Begins at: {cls.dateformat(correction['begin_at'])} -> {round(int(correction['scale']['duration']) / 60)}min.\n"
            # s = f"{s} - Repo url: {correction['team']['repo_url']}\n"
            s = f"{s} - Team name: {correction['team']['name']}\n"
            # s = f"{s} - Corrections required: {correction['scale']['correction_number']}\n"
            if correction['team']['closed?']:
                s = f"{s}---------  Feedback  ---------\n"
                s = f"{s}{correction['corrector']['login']}:\n{correction['comment']}\n\n"
                for feedbck in correction['feedbacks']:
                    if feedbck['user'] != None:
                        s = f"{s}{feedbck['user']['login']}: {feedbck['rating']}\n{feedbck['comment']}\n"
                    else:
                        s = f"{s}{feedbck['comment']} {feedbck['rating']}\n"
            s = f"{s}******************************\n\n"
        return s

    def __call__(self, login: str, offset: int, full_report: bool = False) -> str:
        '''
        Obtains the whitenova report of the given user_id in the given period.
        '''
        period = self._whitenova_period(offset)
        # Log times
        filterStart = f"range[begin_at]={period.get('start_str')},{period.get('end_str')}"
        filterEnd = f"range[end_at]={period.get('start_str')},{period.get('end_str')}"
        sortFilter = "sort=begin_at"

        locations = self.api.get(f"/v2/users/{login}/locations", [filterEnd, sortFilter])
        if len(locations) > 0:
            if locations[-1]["end_at"] == None:
                lend = self._t_now()
            else:
                lend = self._stodate(locations[-1]["end_at"])
            if lend > period.get("end"):
                locations[-1]["end_at"] = period.get("end").strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        # Corrections
        # corrections = self.corrections_as("as_corrector", self.get_id(login), [filterStart, sortFilter], True)
        # TODO
        corrections = []
        return self._parse(login, period, locations, corrections, full_report=full_report)

class Mole(NanoShell):

    LOGIN_USAGE = "<LOGIN>"

    CMDS = NanoShell.CMDS | {
        "WHITENOVA": ["whitenova", "wnova"],
    }

    FLAGS = NanoShell.FLAGS | {
        # WHITENOVA
        "WHITENOVA_OFFSET": "-p",
        "WHITENOVA_FULL": "--full",
    }

    USAGE = NanoShell.USAGE | {
        "WHITENOVA": f"{LOGIN_USAGE} [{FLAGS['WHITENOVA_OFFSET']} N] [{FLAGS['WHITENOVA_FULL']}]",
    }

    DESCRIPTION = NanoShell.DESCRIPTION | {
        "WHITENOVA": "Show the whitenova of the given user.",
    }

    def __init__(self, debug: bool = False):
        super().__init__(debug)
        self.nova = WhiteNova()

    def _handle_cmd(self, cmd: list) -> bool:
        if super()._handle_cmd(cmd):
            return True
        if cmd[0] in self.CMDS["WHITENOVA"]:
            self.whitenova(cmd)
        else:
            return False
        return True

    # ******* COMMANDS LOGIC *******

    def whitenova(self, c: list) -> None:
        if len(c) < 2 or len(c) > 4:
            return self._usage(c)
        login = c[1]
        offset = 0
        full_report = False
        i = 2
        while i < len(c):
            if i + 1 >= len(c):
                if c[i] == self.FLAGS['WHITENOVA_FULL']:
                    full_report = True
                    i = i + 1
                    continue
                return self._usage(c)
            elif c[i] == self.FLAGS['WHITENOVA_OFFSET'] and\
                c[i + 1].isnumeric():
                offset = int(c[i + 1])
            else:
                return self._usage(c)
            i = i + 2
        self.print(self.nova(login, offset, full_report))


    def _title(self):
        return f"""
███    ███  ██████  ██      ███████
████  ████ ██    ██ ██      ██     
██ ████ ██ ██    ██ ██      █████  
██  ██  ██ ██    ██ ██      ██     
██      ██  ██████  ███████ ███████

"""

if __name__ == "__main__":
    w = Mole()
    # w.run()
    w.whitenova(["whitenova", "jre-gonz"])
    # w.whitenova(["whitenova", "jre-gonz", "-p", "1", "--full"])