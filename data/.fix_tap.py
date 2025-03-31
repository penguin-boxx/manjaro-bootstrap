import subprocess

def run(*command):
    return subprocess.run(command, capture_output=True).stdout.decode("utf-8").split('\n')

def find(xs, p):
    for x in xs:
        if p(x):
            return x

def main():
    devices = run('xinput', 'list')
    ids = [word[3:]
        for device in devices
        for word in device.split()
        if word.startswith('id=')
    ]
    for id in ids:
        props = run('xinput', 'list-props', id)
        for prop in props:
            if 'Tapping Enabled (' in prop:
                prop_id = find(prop.split(), lambda x: x.startswith('(') and x.endswith(':'))[1:][:-2]
                print(f'Fixing ({id}, {prop_id})')
                run('xinput', 'set-prop', id, prop_id, '1')
                return
    print('ERROR: Tab fixing failed!')

if __name__ == '__main__':
    main()
