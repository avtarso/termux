Simple automatic replacement of photos and bios in Telegram according to schedule on python and telethon/

1.  Install Termux from Google Play
https://play.google.com/store/apps/details?id=com.termux

2. Start Termux

3. Prepare Termux:
 
    pkg update
    pkg upgrade
    pkg install python
    pkg install pip
    pkg install git

3. Create requirements.txt

    nano requirements.txt

and paste the contents of the file requirements.txt from this repository

4. Tune python

    pip install -r requirements.txt

5. Create settings.py

    nano requirements.txt

and paste application's own settings

API_ID = 1111111111
API_HASH = "*****************************"

6. Install this repository

    git clone https://github.com/avtarso/termux

7. Run

    cd termux
    python main.py


