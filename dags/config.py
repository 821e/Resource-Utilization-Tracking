DEVICES = {
    'host': {
        'type': 'local',
        'name': 'host_machine'
    },
    'remote_devices': [
        {
            'name': 'server1',
            'host': '192.168.1.100',
            'port': 22,
            'username': 'admin',
            'key_file': '/path/to/ssh/key'  # or use password authentication
        },
        # Add more devices as needed
    ]
}