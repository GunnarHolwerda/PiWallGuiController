"""
    This script is used to setup Raspberry Pi's for PiWall usage for either a master
    or tile
"""

from subprocess import call
from piwallcontroller import wall
from argparse import ArgumentParser

PACKAGES_TO_INSTALL = ['libav-tools', 'xrdp', 'sshpass']

ARGPARSE = ArgumentParser(description="Setup a Raspberry Pi for a Piwall")
ARGPARSE.add_argument('pi_type', type=str, help="The type of Pi to set up (tile, master)")
ARGPARSE.add_argument('--num', '-n', type=int, help="The number tile to be setting up")
args = ARGPARSE.parse_args()

def cleanup_preexisting_piwall():
    """
        Removes scripts from a preexisting PiWall
    """
    print("Removing preexisting PiWall scripts")
    call("sudo rm -rf /home/pi/scripts", shell=True)

def set_keyboard_to_us():
    """
        Sets the Pi's keyboard to the United States configuration
    """
    print("Setting keyboard to US")
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

def install_necessary_packages():
    """
        Installs necessary for the PiWallGUI
    """
    for package in PACKAGES_TO_INSTALL:
        print("Installing {}".format(package))
        call("sudo apt-get install {} -y > /dev/null".format(package), shell=True)

def install_pwlibs():
    """
        Install pwlibs
    """
    print("Installing pwlibs")
    call("wget http://dl.piwall.co.uk/pwlibs1_1.7_armhf.deb", shell=True)
    call("sudo dpkg -i /home/pi/pwlibs1_1.7_armhf.deb", shell=True)
    call("sudo rm -rf /home/pi/pwlibs1_1.7_armhf.deb", shell=True)

def install_pwomxplayer():
    """
        Install pwomxplayer
    """
    call("wget http://dl.piwall.co.uk/pwomxplayer_20130815_armhf.deb", shell=True)
    call("sudo dpkg -i /home/pi/pwomxplayer*", shell=True)
    call("sudo rm -rf /home/pi/pwomxplayer_20130815_armhf.deb", shell=True)

def set_static_ip_address(ip_addr):
    """
        Sets IP address of the Pi to the paramter passed in

        :ip_addr : str, the ip_adress to set
    """
    print("Setting static IP to {0}".format(ip_addr))
    # Edit /etc/network/interfaces
    call("sudo chown pi /etc/network/interfaces", shell=True)
    interfaces_file = open("/etc/network/interfaces", "w")
    interfaces_file.write(wall.replace_str.format(ip_addr))
    interfaces_file.close()
    call("sudo chown root /etc/network/interfaces", shell=True)

def create_and_copy_pitile(tile_id):
    """
        Creates the .pi_tile file and copies it to the tile

        :tile_id : int, the id for the current tile
    """
    print("Creating .pitile and copying .piwall...")
    # Creating .pitile
    dot_pitile = open(".pitile", "w")
    dot_pitile.write("[tile]\n")
    dot_pitile.write("id=" + str(id))
    dot_pitile.close()
    # Copy piwall config, pitile, and startTile script to the directory
    call("sudo mv .pitile /home/pi", shell=True)
    call("sudo cp .piwall /home/pi", shell=True)

if __name__ == "__main__":
    if args.pi_type not in ['tile', 'master']:
        print("Pi type must be either master or tile")
        exit()

    if args.pi_type == "tile" and not args.num:
        print("The -n option must be specified when setting up a tile")
        exit()

    cleanup_preexisting_piwall()

    if args.pi_type == "tile":
        tile_id = wall.configs['tiles'][args.num]['id']
        ip_address = wall.configs['tiles'][args.num]['ip']
        call("python3 setup/dotpiwallsetup.py", shell=True)
    else:
        ip_addresss = wall.master_ip

    call("chmod +x main.py", shell=True)
    call("sudo apt-get update -y > /dev/null", shell=True)
    call("sudo apt-get upgrade -y > /dev/null", shell=True)
    set_keyboard_to_us()

    install_necessary_packages()
    if args.pi_type == "tile":
        install_pwlibs()
        install_pwomxplayer()

    set_static_ip_address(ip_address)

    if args.pi_type == "tile":
        create_and_copy_pitile(tile_id)


    print("Config completed")
