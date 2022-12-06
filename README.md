# MoleWakaMole [DEPRECATED]:

**Note**: This repository has no longer support.

Application written in Python3 with a simple terminal to obtain data from the 42Network API.

## Running the program:
- Setup the credentials.
- Execute `python3 main.py`.
- Use the command `help` to see the available commands and enjoy.

## Credentials setup:
1. Create an API42 application in the intranet.
    - Go to `settings -> api -> new`.
    - Fill the name of the application.
    - Enter a URL. MoleWakaMole will not need this, so enter the URL you want.
2. Execute the ```./install.sh``` script and enter the data required from the intranet.
    - This will store the credentials and install the dependencies needed.
    - Once done the first time, the script will not ask for the credentials again. However, if they become invalid or you want to modify them, run ```./install.sh --reset```.
