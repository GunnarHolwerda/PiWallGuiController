# PiWallGuiController
A small Python program that allows control of a [PiWall](piwall.co.uk) through a graphical user interface from the Master Pi. This program also supports the ability to create playlists of videos to play through your PiWall for a set amount of time.

## Setup
Download this project as a .zip file and copy to the Raspberry Pi's home directory.

Unzip the project, and open up **piwallcontroller/wall.py**.
This file holds all of the configurations for the tiles and master Pi. Add as many tiles as you want, this is a Python file so make sure to follow Python syntax when editing.

To set up the Master Pi run:
```
$ python3 setup.py master -a
```
To setup up a Tile Pi run:
```
$ python3 setup.py tile -a <tile_num>
```
Where **tile_num** is the number tile you are configuring from wall.py. (Use 1 if you are editing the first tile in the list, not 0)

The setup goes through and sets static IP addresses for the Pi's entered in the wall.py file, installs all necessary programs it uses to run, and creates .piwall and .pitile files for the Pi's.

## Adding Videos
To add videos to the dropdown in the interface, copy your video files into the videos/ folder in the base directory of the project.

## How to Use
Run the main.py script either from the command line in the base directory of the project:
```
$ python3 main.py
```
OR
Make main.py executable
```
$ chmod +x main.py
$ ./main.py
```

### Interface
![Image of Base GUI](http://i.imgur.com/JeqrHiA.png)

#### Video Dropdown
This displays all files listed in the PiWallGuiController/videos/ directory in a dropdown list.

#### Timeout Dropdown
This gives you the option of how long you want the video to play. 1, 2 and 3 hour options are default. More can be added if you edit the TIMEOUTS dictionary in main.py in the SelectorWindow class.

#### Add Button
This button takes the current video from the dropdown and the current timeout and adds them to the ListBox on the right.

#### Delete Button
If you click a Playlist item in the ListBox on the right and click delete, it will remove it from the list.

#### Submit Button
When pressed this button will start the PiWall using the playlist being displayed in the ListBox.

#### Reboot Tiles Button
Sometimes things can go wrong. The PiWall is very finicky in that the Tiles must be started before the master is started. If anything seems to have gotten out of order, pressing this button will send reboot commands to all of the Pi's.

#### Stop Playing Button
This button will stop the playing of the videos to the tiles.

#### Status Label
Displays the current status of the PiWall
Display when the wall is not playing:

![Not Playing](http://i.imgur.com/EbkwDGz.png)

Display when the wall is playing:

![Playing](http://i.imgur.com/ZmMZayn.png)
