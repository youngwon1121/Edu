class UnsupportedURL(Exception):
    def __init__(self, url):
        super().__init__(f"{url} is not supported.")