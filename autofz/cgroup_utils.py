#!/usr/bin/env python3
'''
used to test cgroup (V1)
'''


def get_cgroup_path(private=True):
    '''
    get the current cgroup path for the container
    '''
    if private:
        return '/'
    p = None
    with open('/proc/1/cpuset', 'r') as f:
        p = f.read().strip()
    assert p
    return p


if __name__ == '__main__':
    cgroup_path = get_cgroup_path()
    print(cgroup_path)
