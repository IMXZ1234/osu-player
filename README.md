# osu-player
A music player dedicated for playing osu! beatmap songs.

Since osu! beatmap songs are distributed in separate beatmap folders under osu! installation directory, many music players can not detect them. So this dedicated music player is written to address this problem.
# Preparation
Install required packages as below. You should install them in an Anaconda virtual environment.
```
conda create -n name_of_your_env
conda activate name_of_your_env
```
|  package   | cmd  | site |
|  ----  | ----  | ----  |
| PyQt5  | pip install PyQt5 | https://pypi.org/project/PyQt5/ |
| eyeD3  | pip install eyed3 | https://pypi.org/project/eyed3/ |
| pydub  | pip install pydub | https://pypi.org/project/PyAudio/ |
| PyAudio  | pip install PyAudio | https://pypi.org/project/pydub/ |
# Usage
## Start the player
* Open cmd and cd to project directory
```
cd 'C:\path_to_project_dir\osu_player'
```
* Activate anaconda environment which have packages above installed.
```
conda activate name_of_your_env
```
* run winmain.py
```
python winmain.py
```
## Browse the Songs folder under osu! installation directory.
Usually osu! Songs folder is:
```
%USERPROFILE%\AppData\Local\osu!\Songs
```
and osu_player assume that as default.

If you want to change that, press the menu button to open the menu and browse to osu! Songs directory on your pc.

System environment variable %USERPROFILE% = C:\Users\your_windows_user_name
# Advanced
* Type these characters at the beginning of search string to change search field. Search in title by default.

| char | field |
|  ----  | ---- |
| @  | artist |
| #  | source |
| $  | tags |
* Your can change format of songs displayed in the song list by editing *'Song info format'* option in setting dialogue.
Available fields include:
    - {artist_unicode}
    - {title_unicode}
    - {artist}
    - {title}
    - {source}
    - {tags}
