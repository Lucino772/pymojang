import json
import os
from os import path

import requests

from ...utils import web
from ..urls import MC_VERSIONS, RESOURCES_DOWNLOAD


class AssetIndex:

    def __init__(self, id: str, size: int, total_size: int, url: str):
        self.id = id
        self.size = size
        self.total_size = total_size
        self.url = url

    @property
    def _data(self):
        return web.request('get', self.url)

    def download(self, directory: str):
        # Retrieve asset index
        data = self._data

        # Create index.json in /indexes
        indexes_dir = path.join(directory, 'indexes')
        if not path.exists(indexes_dir):
            os.mkdir(indexes_dir)
        
        index_file = path.join(indexes_dir, f'{self.id}.json')
        with open(index_file, 'w') as fp:
            json.dump(data, fp)

        # Create hash files in /objects
        objects_dir = path.join(directory, 'objects')
        if not path.exists(objects_dir):
            os.mkdir(objects_dir)

        for _, value in data['objects'].items():
            resources_hash = value['hash']
            response = requests.get(RESOURCES_DOWNLOAD.format(resources_hash[:2], resources_hash))
            
            resource_dir = path.join(objects_dir, resources_hash[:2])
            if not path.exists(resource_dir):
                os.mkdir(resource_dir)

            resource_file = path.join(resource_dir, resources_hash)
            with open(resource_file, 'wb') as fp:
                fp.write(response.content)
