from importlib.metadata import version

PACKAGE_NAME = "xcodefy"


class Version:
    @staticmethod
    def current() -> str:
        return version(PACKAGE_NAME)
