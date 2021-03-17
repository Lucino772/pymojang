import requests
import validators
import os
import re

class Cape:

    def __init__(self, filename: str):
        self.__filename = filename
        self.__extension = None

    @property
    def extension(self):
        return self.__extension

    @property
    def exists(self):
        do_exists = False

        if validators.url(self.__filename) == True:
            response = requests.head(self.__filename, allow_redirects=True)
            if response.status_code == 200:
                do_exists = True
        elif os.path.exists(self.__filename):
            do_exists = True

        return do_exists

    @property
    def data(self):
        image_bytes = None
        if validators.url(self.__filename) == True:
            response = requests.get(self.__filename)
            if response.ok:
                filenames = re.findall('filename=(.+)', response.headers.get('content-disposition'))
                if len(filenames) > 0:
                    self.__extension = os.path.splitext(filenames[0].replace('"','').strip())[1]
                image_bytes = response.content
        elif os.path.exists(self.__filename):
            self.__extension = os.path.splitext(self.__filename)[1]
            with open(self.__filename,'rb') as fp:
                image_bytes = fp.read()

        return image_bytes

    def to_file(self, filename: str):
        file_data = self.data
        file_path = filename + self.__extension
        
        if file_data is not None and self.__extension is not None:
            with open(file_path, 'wb') as fp:
                fp.write(file_data)
