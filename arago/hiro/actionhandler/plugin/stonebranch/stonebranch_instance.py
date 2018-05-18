class StonebranchInstance:
    def __init__(self, host: str, username: str, password: str, port=443) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    @property
    def authority(self) -> str:
        return '%s:%s' % (self.host, self.port)
