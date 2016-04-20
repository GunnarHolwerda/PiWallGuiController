"""
    This script creates the .piwall file based off of the wall.py file
"""

print("Create .piwall configuration file:")
print("Wall info:")

from os.path import dirname, abspath
import sys

BASE_PATH = dirname(dirname(abspath(__file__))) + "/"
sys.path.insert(0, BASE_PATH)
from piwallcontroller import wall

configs = wall.configs
walls = configs['walls']

# Create .piwall file
dot_piwall = open(".piwall", "w")

# Wall definition
dot_piwall.write("#Wall definition\n")
for key in walls:
    dot_piwall.write("[" + walls[key]['name'] + "]\n")
    dot_piwall.write("width=" + walls[key]['width'] + "\n")
    dot_piwall.write("height=" + walls[key]['height'] + "\n")
    dot_piwall.write("x=0\n")
    dot_piwall.write("y=0\n\n")

# Tile definitions
dot_piwall.write("#Tile definitions\n")
for x in range(0, configs['num_of_tiles']):
    # Gather data for tile
    print("New tile\n")
    name_of_tile = configs['tiles'][x]['name']
    name_of_wall = configs['tiles'][x]['wall']
    tile_id = configs['config'][0]['tile'][x]['id']
    height_of_tile = configs['tiles'][x]['height']
    width_of_tile = configs['tiles'][x]['width']
    x_start = configs['tiles'][x]['x']
    y_start = configs['tiles'][x]['y']

    # Write out the tile to the file
    dot_piwall.write("[" + name_of_tile + "]\n")
    dot_piwall.write("wall=" + name_of_wall + "\n")
    dot_piwall.write("width=" + width_of_tile + "\n")
    dot_piwall.write("height=" + height_of_tile + "\n")
    dot_piwall.write("x=" + x_start + "\n")
    dot_piwall.write("y=" + y_start + "\n")

# Configuration Definition
name_of_config = configs['config'][0]['name']
dot_piwall.write("#Configuration\n")
for config in configs['config']:
    dot_piwall.write("\n[" + config['name'] + "]\n")
    for x in range(0, configs['num_of_tiles']):
        dot_piwall.write(configs['config'][0]['tile'][x]['id'] + "=" + configs['tiles'][x]['name'] + "\n")
    dot_piwall.write("\n")

# Close file, we are done
dot_piwall.close()
