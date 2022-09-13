# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    mole.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: jre-gonz <jre-gonz@student.42madrid.com    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/09/12 23:01:26 by jre-gonz          #+#    #+#              #
#    Updated: 2022/09/12 23:03:28 by jre-gonz         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from Nanoshell import NanoShell
from whitenova import WhiteNova

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
        if len(c) < 2 or len(c) > 5:
            return self._usage(c)
        login = c[1]
        offset = 0
        full_report = False
        i = 2
        while i < len(c):
            if c[i] == self.FLAGS['WHITENOVA_FULL']:
                full_report = True
                i = i + 1
                continue
            elif i + 1 >= len(c):
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