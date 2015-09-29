import argparse


class Application():
    def __init__(self, args):
        print args

    def list(self):
        pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    parser.add_argument('-l', '--list', action="store_true", help='list installed versions')
    parser.add_argument('-g', '--get', action="store_true", help='list available versions')
    group.add_argument('-i', '--install', type=str, help='install a specific version')
    # group.add_argument('-u', '--uninstall', type=str, help='uninstall a specific version')
    # group.add_argument('-a', '--add', type=str, help='add installed version')
    # group.add_argument('-c', '--clone', type=str, help='clone installed version')
    # todo: add versions_cache
    # todo: refresh cache

    Application(parser.parse_args())