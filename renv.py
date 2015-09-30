import argparse
from logger.app_logger import AppLogger


class RenvException(Exception):
    pass


class Application():
    def __init__(self, args):
        self.logger = AppLogger().logger
        self.parse_command(args)

    def list(self):
        pass

    def parse_command(self, args):
        if args.command == 'list':
            if args.list_what == 'installed':
                self.list_installed()
            elif args.list_what == 'available':
                self.list_available(refresh=args.refresh)
            elif args.list_what == 'all':
                self.list_all(refresh=args.refresh)
            else:
                raise RenvException('Unknown list argument')
        elif args.command == 'install':
            self.install(version=args.version)
        elif args.command == 'remove':
            self.remove(version=args.version)
        elif args.command == 'use':
            self.use(version=args.version)
        else:
            raise RenvException('Unknown command')

    def list_installed(self):
        self.logger.info('list_installed')

    def list_available(self, refresh):
        self.logger.info('list_available(refresh: {0})'.format(refresh))

    def list_all(self, refresh):
        self.logger.info('list_all(refresh: {0})'.format(refresh))

    def install(self, version):
        self.logger.info('install(version: {0})'.format(version))

    def remove(self, version):
        self.logger.info('remove(version: {0})'.format(version))

    def use(self, version):
        self.logger.info('use(version: {0})'.format(version))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    # list command
    list_parser = subparsers.add_parser('list', help='list ruby version')
    list_parser.add_argument('list_what', nargs='?', choices=['installed', 'available', 'all'],
                             default='installed', help='installed, available or all versions (default: installed)')
    list_parser.add_argument('-r', '--refresh', action="store_true",
                             help='parse available versions from site with no cache (default: false)')
    # install command
    install_parser = subparsers.add_parser('install', help='install a specific version')
    install_parser.add_argument('version', type=str, help='ruby version to install')

    # remove command
    remove_parser = subparsers.add_parser('remove', help='remove a specific version')
    remove_parser.add_argument('version', type=str, help='ruby version to remove')

    # use command
    install_parser = subparsers.add_parser('use', help='use a specific version for the current path')
    install_parser.add_argument('version', nargs='?', type=str,
                                help='ruby version to use. If none specified will look in the .renv_version file')

    Application(parser.parse_args())