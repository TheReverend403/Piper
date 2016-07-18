Pyper - A Python Telegram bot
=============================

# Requirements
Python 3.4  
[pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) (requirements.txt)

# Install
First, acquire a bot token from https://telegram.me/BotFather

```sh
git clone https://github.com/TheReverend403/Pyper
cd Pyper
virtualenv .venv -p python3
source .venv/bin/activate
pip install -r requirements.txt
cp config.ini.sample config.ini
nano config.ini # Add your bot token
python -m pyper.main
```

# Upgrade
```sh
cd Pyper
git pull
source .venv/bin/activate
pip install -r requirements.txt
cat config.ini.sample # Check for any new values, add them to config.ini
```

# systemd service
To run Pyper as a systemd user service:

```sh
cp pyper.service ~/.config/systemd/user
nano ~/.config/systemd/user/pyper.service # Edit as needed
systemctl --user daemon-reload
systemctl --user enable pyper
systemctl --user start pyper
sudo loginctl enable-linger $USER # To allow user services to run on startup and stay after logout.
```

To run Pyper as a systemd system service (not recommended):

```sh
sudo cp pyper.service /etc/systemd/system
sudo nano /etc/systemd/system/pyper.service # Edit as needed
sudo systemctl daemon-reload
sudo systemctl enable pyper
sudo systemctl start pyper
```