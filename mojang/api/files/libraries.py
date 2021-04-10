import os
import platform
from os import path

import requests


class Librairies:

    def __init__(self, data: dict):
        librairies = {}
        natives = {}
        
        for item in data:
            name  = item['name']
            rules = item.get('rules', None)
            artifact = item['downloads'].get('artifact', None)
            if artifact:
                librairies[artifact['sha1']] = Library(name, artifact['path'], artifact['sha1'], artifact['size'], artifact['url'], False, None, rules)

            natives_artifact = item['downloads'].get('classifiers', {})
            for native_name, native in natives_artifact.items():
                natives[native['sha1']] = Library(name, native['path'], native['sha1'], native['size'], native['url'], True, native_name, rules)

        self.librairies = tuple(librairies.values())
        self.natives = tuple(natives.values())
        self.all = self.librairies + self.natives

    def download_all(self, directory: str, system=None):
        for lib in self.all:
            lib.download(directory, system)
    
    def paths(self, directory: str, system=None):
        return [path.join(directory,lib.path,lib.filename) for lib in self.all if lib.required(system)]

class Library:

    def __init__(self, name: str, _path: str, _hash: str, size: int, url: str, is_native=False, native_name=None, rules=None):
        self.name = name
        self.path, self.filename = path.split(_path)
        self.hash = _hash
        self.size = size
        self.url = url
        self.native_name = native_name
        self.is_native = is_native
        
        self._parse_rules(rules)
    
    def _parse_rules(self, rules: list):
        _os = {'windows','linux','darwin'}

        if rules:
            # allowed will be processed before disallowed
            rules.sort(key=lambda item: item['action'])

            for rule in rules:
                os_name = rule.get('os', {}).get('name', None)
                os_name = 'darwin' if os_name == 'osx' else os_name

                if rule['action'] == 'allow':
                    if os_name:
                        _os = {os_name}
                else:
                    if os_name:
                        _os.remove(os_name)
                    else:
                        _os = set()

        if self.is_native:
            if 'windows' in self.native_name and 'windows' in _os:
                _os = {'windows'}
            elif 'linux' in self.native_name and 'linux' in _os:
                _os = {'linux'}
            elif ('macos' in self.native_name or 'osx' in self.native_name) and 'darwin' in _os:
                _os = {'darwin'}
            else:
                _os = set()

        self.allowed_os = _os

    def required(self, system=None):
        if not system:
            system = platform.system().lower()
        
        return system in self.allowed_os

    def download(self, directory: str, system=None):
        if self.required(system) and path.exists(directory):
            _path = path.join(directory, self.path)
            if not path.exists(_path):
                os.makedirs(_path)
            
            file_path = path.join(_path, self.filename)

            response = requests.get(self.url)
            with open(file_path, 'wb') as fp:
                fp.write(response.content)
