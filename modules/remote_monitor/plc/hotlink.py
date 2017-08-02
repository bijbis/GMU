import urllib.request


class Hotlink:

    def __init__(self, url):
        url_data = urllib.request.urlopen(url).read()
        self._data = self.decode(url_data)

    def decode(self, url_data):
        return int(url_data.decode("utf-8").split('RVI')[1].split('*')[0], 16)

    @property
    def data(self):
        return self._data
