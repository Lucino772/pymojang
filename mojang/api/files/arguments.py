import platform
import re

class Arguments:

    def __init__(self, game_args: list, jvm_args: list):
        self.game_args = self._parse_args(game_args, GameArgument)
        self.jvm_args = self._parse_args(jvm_args, JvmArgument)
        self.all = self.game_args + self.jvm_args
    
    def _parse_args(self, args: list, cls):
        _args = []

        if isinstance(args, list):
            for arg in args:
                if isinstance(arg, dict):
                    rules = arg.get('rules', None)

                    if isinstance(arg['value'], str):
                        values = [arg['value']]
                    else:
                        values = arg['value']

                    for value in values:
                        _args.append(cls(value, rules))
                else:
                    _args.append(cls(arg, None))
        
        return tuple(_args)

class GameArgument:

    def __init__(self, argument: str, rules=None):
        self.argument = argument
        self._parse_rules(rules)

    def _parse_rules(self, rules: list):
        _allowed_features = {}
        _disallowed_features = {}
        if rules:
            
            rules.sort(key=lambda item: item['action'])

            for rule in rules:
                features = rule.get('features', {})
                if rule['action'] == 'allow':
                    _allowed_features.update(features)
                else:
                    _disallowed_features.update(features)
        
        self.allowed_features = tuple(_allowed_features.items())
        self.disallowed_features = tuple(_disallowed_features.items())


class JvmArgument:

    def __init__(self, argument: str, rules=None):
        self.argument = argument
        self._parse_rules(rules)
    
    def _parse_rules(self, rules: list):
        _os = {'windows', 'linux', 'darwin'}
        _version = dict.fromkeys(_os)
        _arch = {'x86','x64'}
        
        if rules:
            
            rules.sort(key=lambda item: item['action'])

            for rule in rules:
                os = rule.get('os', {})
                os_name = os.get('name', None)
                os_name = 'darwin' if os_name == 'osx' else os_name
                os_version = os.get('version', None)
                os_arch = os.get('arch', None)

                if rule['action'] == 'allow':
                    if os_name:
                        _os = {os_name}
                        _version[os_name] = os_version
                    
                    if os_arch:
                        _arch = {os_arch}
                else:
                    if os_name:
                        _os.remove(os_name)
                        _version.pop(os_name)
                    
                    if os_arch:
                        _arch.remove(os_arch)

                    if not os:
                        _os = set()
                        _arch = set()


        self.allowed_os = tuple(_os)
        self.allowed_versions = tuple(_version.items())
        self.allowed_arch = tuple(_arch)

    def required(self, system=None, version=None, architecture=None):
        if not system:
            system = platform.system().lower()
        if not version:
            version = platform.version()
        if not architecture:
            architecture = 'x86' if platform.architecture()[0] == 32 else 'x64'
        
        is_system_ok = system in self.allowed_os
        is_version_ok = [(item[1] is None or re.match(item[1], version)) for item in self.allowed_versions if item[0] == system]
        is_arch_ok = architecture in self.allowed_arch

        return is_system_ok and is_version_ok and is_arch_ok
