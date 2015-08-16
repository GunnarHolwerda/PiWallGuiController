# Network information
master_ip = "169.254.219.10"

# Wall.py for PiWall
configs = {
    'walls': {
        'burning_man_wall': {
            'name': 'burning_man_wall',
            'height': '270',
            'width': '1080',
            'master_ip': '169.254.219.10'
        }
    },
    'num_of_tiles': 4,
    'tiles': [
        {
            'name': 'left_1',
            'wall': 'burning_man_wall',
            'width': '270',
            'height': '270',
            'x': '0',
            'y': '0',
            'ip': '169.254.219.5',
            'id': 'left1'
        },
        {
            'name': 'left_2',
            'wall': 'burning_man_wall',
            'width': '270',
            'height': '270',
            'x': '270',
            'y': '0',
            'ip': '169.254.219.6',
            'id': 'left2'
        },
        {
            'name': 'right_1',
            'wall': 'burning_man_wall',
            'width': '270',
            'height': '270',
            'x': '540',
            'y': '0',
            'ip': '169.254.219.7',
            'id': 'right1'
        },
        {
            'name': 'right_2',
            'wall': 'burning_man_wall',
            'width': '270',
            'height': '270',
            'x': '810',
            'y': '0',
            'ip': '169.254.219.8',
            'id': 'right2'
        }
    ],
    'config': [
        {
            'name': 'burning_man_config',
            'tile': [
                {
                    'id': 'left1'
                },
                {
                    'id': 'left2'
                },
                {
                    'id': 'right1'
                },
                {
                    'id': 'right2'
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
"""
