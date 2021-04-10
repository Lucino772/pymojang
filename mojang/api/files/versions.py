import datetime as dt
import json
import os
from os import path

import requests

from ...utils import web
from ..urls import MC_VERSIONS
from .arguments import Arguments
from .assets import AssetIndex
from .libraries import Librairies


class ServerInstallation:

    def __init__(self, version: 'MinecraftVersion', **kwargs):
        self.__version = version
        self.__system = kwargs.get('system')

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def install(self, directory: str, filename=None):
        if not path.exists(directory):
            return

        if not filename:
            filename = f'server-{self.__version.id}.jar'
        
        filepath = path.join(directory, filename)

        server = self.__version.server[0]
        if self.__system == 'windows' and self.__version.server[1]:
            server = self.__version.server[1]
        
        response = requests.get(server[0])
        with open(filepath, 'wb') as fp:
            fp.write(response.content)    

    def create_config(self, config_path: str):
        pass


class ClientInstallation:

    def __init__(self, version: 'MinecraftVersion', **kwargs):
        self.__version = version
        self.__system = kwargs.get('system', None)
        self.__sys_version = kwargs.get('version', None)
        self.__arch = kwargs.get('arch', None)

    def __enter__(self):
        self.__asset_dir = None
        self.__libs_dir = None
        self.__client_path = None
        return self

    def __exit__(self, *args):
        self.__asset_dir = None
        self.__libs_dir = None
        self.__client_path = None

    def _ensure_dir(self, directory: str):
        if not path.exists(directory):
            os.makedirs(directory, exist_ok=True)
        
        return directory

    def install(self, directory: str):
        if not path.exists(directory):
            return

        assets_dir = self._ensure_dir(path.join(directory, 'assets'))
        libs_dir = self._ensure_dir(path.join(directory, 'libraries'))
        client_dir = self._ensure_dir(path.join(directory, 'versions', self.__version.id))
        client_path = path.join(client_dir, f'client-{self.__version.id}.jar')

        print('Downloading assets...')
        self.download_assets(assets_dir)
        print('Downloading libraries...')
        self.download_libs(libs_dir)
        print('Downloading client...')
        self.download_client(client_path)

    def download_assets(self, directory: str):
        self.__version.asset_index.download(directory)
        self.__asset_dir = directory
    
    def download_libs(self, directory: str):
        self.__version.libraries.download_all(directory, self.__system)
        self.__libs_dir = directory
    
    def download_client(self, filepath: str):
        response = requests.get(self.__version.client[0])
        with open(filepath, 'wb') as fp:
            fp.write(response.content)
        
        self.__client_path = filepath

    def create_config(self, config_path: str, game_directory: str):
        # Assets
        index_file = path.join(self.__asset_dir, 'indexes', f'{self.__version.asset_index.id}.json')

        # Libraries
        installed_libs = []
        installed_natives = []

        filtered = filter(lambda lib: lib.required(self.__system), self.__version.libraries.all)
        for lib in filtered:
            if not lib.is_native:
                installed_libs.append(path.join(self.__libs_dir, lib.path, lib.filename))
            else:
                installed_natives.append(path.join(self.__libs_dir, lib.path, lib.filename))

        # Game Argument
        game_args = {}
        for garg in self.__version.arguments.game_args:
            game_args[garg.argument] = {
                'allowed': dict(garg.allowed_features),
                'disallowed': dict(garg.disallowed_features)
            }

        jvm_args = []
        for jarg in self.__version.arguments.jvm_args:
            if jarg.required(self.__system, self.__sys_version, self.__arch):
                jvm_args.append(jarg.argument)

        # Create config
        config = {
            'assets': {
                'id': self.__version.asset_index.id,
                'directory': self.__asset_dir,
                'index_file': index_file
            },
            'libraries': installed_libs,
            'natives': installed_natives,
            'client': {
                'id': self.__version.id,
                'type': self.__version.type,
                'main_class': self.__version.main_class
            },
            'game_directory': game_directory,
            'arguments': {
                'game': game_args,
                'jvm': jvm_args
            }
        }
        with open(config_path, 'w') as fp:
            json.dump(config, fp)


class MinecraftVersions:
    __instance = None

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = object.__new__(cls)
        
        return cls.__instance

    def __init__(self):
        self.__versions = []
        self.__last_release = None
        self.__last_snapshot = None

    def refresh(self):
        data = web.request('get', MC_VERSIONS)

        versions = []
        for version in data['versions']:
            obj = MinecraftVersion(version['id'], version['url'], version['type'])
            
            if obj.is_snapshot and obj.id == data['latest']['snapshot']:
                self.__last_snapshot = obj               
            elif obj.is_release and obj.id == data['latest']['release']:
                self.__last_release = obj 
            
            versions.append(obj)
        
        self.__versions = versions

    @property
    def last_release(self) -> 'MinecraftVersion':
        return self.__last_release

    @property
    def last_snapshot(self) -> 'MinecraftVersion':
        return self.__last_snapshot

    @property
    def all(self) -> list:
        return self.__versions

    def get(self, _id: str) -> 'MinecraftVersion':
        version = [v for v in self.__versions if v.id == _id]
        if len(version) > 0:
            version[0]._load()
            return version[0]

    def __getitem__(self, key: str):
        return self.get(key)


class MinecraftVersion:

    def __init__(self, _id: str, url: str, _type: str):
        self.__id = _id
        self.__url = url
        self.__type = _type
        self.__loaded = False

        self.__time = None
        self.__release_time = None

        self.__main_class = None
        self.__minimum_launcher_version = None

        self.__client = None
        self.__server = None
        self.__win_server = None

        self.__java_version = None

        self.__asset_index = None
        self.__libraries = None

        self.__arguments = None

    def _load(self):
        if not self.__loaded:
            data = web.request('get', self.__url)

            # Load release time
            self.__time = dt.datetime.strptime(data['time'], '%Y-%m-%dT%H:%M:%S%z')
            self.__release_time = dt.datetime.strptime(data['releaseTime'], '%Y-%m-%dT%H:%M:%S%z')

            # Load basic info
            self.__main_class = data['mainClass']
            self.__minimum_launcher_version = data['minimumLauncherVersion']

            # Load Java version
            _java_version = data.get('javaVersion', None)
            if _java_version:
                self.__java_version = (_java_version['component'], _java_version['majorVersion'])

            # Load Downloads
            _downloads = data.get('downloads', None)
            if _downloads:
                client = _downloads['client']
                client_mappings = _downloads.get('client_mappings', dict.fromkeys(['url', 'size'], None))

                self.__client = (client['url'], client['size'], client_mappings['url'], client_mappings['size'])

                server = _downloads.get('server', None)
                if server:
                    server_mappings = _downloads.get('server_mappings', dict.fromkeys(['url', 'size'], None))

                    self.__server = (server['url'], server['size'], server_mappings['url'], server_mappings['size'])

                win_server = _downloads.get('windows_server', None)
                if win_server:
                    self.__win_server = (win_server['url'], win_server['size'], None, None)

            # Load asset index
            asset_index = data['assetIndex']
            self.__asset_index = AssetIndex(asset_index['id'], asset_index['size'], asset_index['totalSize'], asset_index['url'])

            # Load Libraries
            self.__libraries = Librairies(data['libraries'])

            # Load Arguments
            if 'arguments' in data:
                self.__arguments = Arguments(data['arguments']['game'], data['arguments']['jvm'])
            else:
                self.__arguments = Arguments(data['minecraftArguments'].split(' '), None)

            # Prevent from loading again
            self.__loaded = True

    # Properties
    @property
    def url(self):
        return self.__url

    @property
    def id(self):
        return self.__id

    @property
    def type(self):
        return self.__type

    @property
    def is_release(self):
        return self.__type == 'release'

    @property
    def is_snapshot(self):
        return self.__type == 'snapshot'

    @property
    def is_alpha(self):
        return self.__type == 'old_alpha'

    @property
    def is_beta(self):
        return self.__type == 'old_beta'

    @property
    def main_class(self):
        return self.__main_class

    @property
    def asset_index(self):
        return self.__asset_index

    @property
    def libraries(self):
        return self.__libraries

    @property
    def arguments(self):
        return self.__arguments

    @property
    def client(self):
        return self.__client

    @property
    def server(self):
        return self.__server, self.__win_server

    # Context manager
    def create_client(self, **kwargs) -> ClientInstallation:
        return ClientInstallation(self, **kwargs)

    def create_server(self, **kwargs) -> ServerInstallation:
        return ServerInstallation(self, **kwargs)
