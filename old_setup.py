# Original author: Gunnar Holwerda
# This script is made to automatically set up the configuration for a
# Raspberry Pi to be used in a piwall

from subprocess import call
from piwallcontroller import wall
import sys

approved_input = False
type_of_config = ""
dotpiwall_exists = False
configs = wall.configs


def print_help():
    print("Please enter a valid command when running the script")
    print("python <tile_type> -<options> <tile_num for tiles>")
    print("Configure Everything (first time setup)")
    print("master - configure the master pi")
    print("tile - configure a tile pi")
    print("help - print this help config")
    print("(A number must be entered with a tile (i.e. tile 1) to specify which " +
        "tile is being configured\n")
    print("Specific Configurations (must include a type of pi m or t)")
    print("a - run all configurations")
    print("i - configure ip address")
    print("u - update and upgrade")
    print("k - set keyboard to US")
    print("c - install needed components")
    print("y - copy start scripts")
    print("z - make main.py executable")
    print("h - print help screen")
    sys.exit()

# Tell the user they have started the initialization script
while not approved_input:
    print("You have started the Raspberry Pi Wall Configuration Script")
    if len(sys.argv) == 1:
        print_help()
    else:
        if sys.argv[1] == "tile" and len(sys.argv) < 4:
            print("You must specify which tile is being configured (i.e. tile -a 5 for " +
            "the 5th tile in the Pi Wall)")
            sys.exit()
        elif sys.argv[1] == "help":
            print_help()
        elif sys.argv[1] != "master" and sys.argv[1] != "tile":
            print("Please enter a valid type of config (tile or master)")
            sys.exit()
        else:
            approved_input = True

# Clean existing scripts
call("sudo rm -rf /home/pi/scripts", shell=True)

if sys.argv[1] == "master":
    print("Configuring master...")
elif sys.argv[1] == "tile":
    print("Configuring tile...")
    tile_num = int(sys.argv[3]) - 1

# Get data for the Raspberry Pi
if sys.argv[1] == "tile":
    tile_id = configs['tiles'][tile_num]['id']
    ip_address = configs['tiles'][tile_num]['ip']
    print("Running .piwall config...")
    call("python3 setup/dotpiwallsetup.py", shell=True)
    print(".piwall file created...")
else:
    ip_address = wall.master_ip

if sys.argv[2].find('z') != -1 or sys.argv[2].find('a') != -1:
    print("Making main.py executable")
    call("chmod +x main.py", shell=True)

# UPDATE and UPGRADE
if sys.argv[2].find('a') != -1 or sys.argv[2].find('u') != -1:
    print("Updating...")
    call("sudo apt-get update" + " -y", shell=True)
    print("Upgrading...")
    call("sudo apt-get upgrade" + " -y", shell=True)

# SET THE KEYBOARD TO US
if sys.argv[2].find('a') != -1 or sys.argv[2].find('k') != -1:
    print("Setting the keyboard to US...")
    # Change owner of config file to pi to be able to edit
    call("sudo chown pi /etc/default/keyboard", shell=True)
    # Get all text that is in the file
    keyboard_config_file = open("/etc/default/keyboard", "r")
    keyboard_config_text = keyboard_config_file.read()
    # Replace the GB with US
    keyboard_config_text = keyboard_config_text.replace("gb", "us")
    keyboard_config_file.close()

    # Write out the text to the file
    keyboard_config_file = open("/etc/default/keyboard", "w")
    keyboard_config_file.write(keyboard_config_text)
    keyboard_config_file.close()
    # Change the owner of the file back to root
    call("sudo chown root /etc/default/keyboard", shell=True)

# # INSTALL LIBAV-TOOLS, SSHPASS, XRDP on master only
if sys.argv[1] == "master" and (sys.argv[2].find('a') != -1 or sys.argv[2].find('c') != -1):
    print("Getting libav-tools...")
    call("sudo apt-get install libav-tools" + " -y", shell=True)
    print("Installing xrdp...")
    call("sudo apt-get install xrdp -y", shell=True)
    call("sudo apt-get install sshpass -y", shell=True)

# DOWNLOAD AND INSTALL PWLIBS and PWOMXPLAYER on tiles only
if sys.argv[1] == "tile" and (sys.argv[2].find('a') != -1 or sys.argv[2].find('c') != -1):
    print("Downloading pwlibs...")
    call("wget http://dl.piwall.co.uk/pwlibs1_1.7_armhf.deb", shell=True)
    print("dpkg pwlibs...")
    call("sudo dpkg -i /home/pi/pwlibs1_1.7_armhf.deb", shell=True)
    print("Downloading pwomxplayer...")
    call("wget http://dl.piwall.co.uk/pwomxplayer_20130815_armhf.deb", shell=True)
    print("dpkg pwomxplayer...")
    call("sudo dpkg -i /home/pi/pwomxplayer*", shell=True)
    print("Removing .deb files...")
    # Remove the .deb files to save space
    call("sudo rm -rf /home/pi/pwlibs1_1.7_armhf.deb && " +
    "sudo rm -rf /home/pi/pwomxplayer_20130815_armhf.deb", shell=True)

# SET STATIC IP ADDRESS
if sys.argv[2].find('a') != -1 or sys.argv[2].find('i') != -1:
    print("Setting static IP to {0}".format(ip_address))
    # Edit /etc/network/interfaces
    call("sudo chown pi /etc/network/interfaces", shell=True)
    interfaces_file = open("/etc/network/interfaces", "w")
    interfaces_file.write(wall.replace_str.format(ip_address))
    interfaces_file.close()
    call("sudo chown root /etc/network/interfaces", shell=True)

# CREATE .pitile AND COPY .piwall
if sys.argv[2].find('a') != -1 or sys.argv[2].find('y') != -1:
    if sys.argv[1] == "tile":
        print("Creating .pitile and copying .piwall...")
        # Creating .pitile
        dot_pitile = open(".pitile", "w")
        dot_pitile.write("[tile]\n")
        dot_pitile.write("id=" + configs['tiles'][tile_num]['id'])
        dot_pitile.close()
        # Copy piwall config, pitile, and startTile script to the directory
        call("sudo cp .piwall /home/pi", shell=True)
        call("sudo mv .pitile /home/pi", shell=True)

# Configuration complete
print("Config completed...")
