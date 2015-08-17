# Network information
master_ip = "0.0.0.0"

# Wall.py for PiWall
configs = {
    'walls': {
        'wall_name': {
            'name': 'wall_name',
            'height': '270',
            'width': '1080',
            'master_ip': '0.0.0.0'
        }
    },
    'num_of_tiles': 4,
    'tiles': [
        {
            'name': 'tile_name',
            'wall': 'wall_name',
            'width': '270',
            'height': '270',
            'x': '0',
            'y': '0',
            'ip': '0.0.0.0',
            'id': 'tile1'
        },
        {
            'name': 'tile_name',
            'wall': 'wall_name',
            'width': '270',
            'height': '270',
            'x': '270',
            'y': '0',
            'ip': '0.0.0.0',
            'id': 'tile2'
        },
        {
            'name': 'tile_name',
            'wall': 'wall_name',
            'width': '270',
            'height': '270',
            'x': '540',
            'y': '0',
            'ip': '0.0.0.0',
            'id': 'tile3'
        },
        {
            'name': 'tile_name',
            'wall': 'wall_name',
            'width': '270',
            'height': '270',
            'x': '810',
            'y': '0',
            'ip': '0.0.0.0',
            'id': 'tile4'
        }
    ],
    'config': [
        {
            'name': 'wall_config',
            'tile': [
                {
                    'id': 'tile1'
                },
                {
                    'id': 'tile2'
                },
                {
                    'id': 'tile3'
                },
                {
                    'id': 'tile4'
                }
            ]
        }
    ]
}

# String new /etc/network/interfaces
replace_str = """auto lo

iface lo inet loopback
iface eth0 inet static
	address {0}
	netmask 255.255.255.0
	up route add -net 224.0.0.0 netmask 240.0.0.0 eth0
"""
