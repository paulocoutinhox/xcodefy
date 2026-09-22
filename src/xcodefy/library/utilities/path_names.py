import os.path


class PathNames:
    @staticmethod
    def path_components(path: str) -> list[str]:
        if not path:
            return []
        components = [component for component in path.split("/") if component]
        return ["/", *components] if path.startswith("/") else components

    @staticmethod
    def last_path_component(path: str) -> str:
        components = PathNames.path_components(path)
        return components[-1] if components else ""

    @staticmethod
    def expanding_tilde(path: str) -> str:
        return os.path.expanduser(path)
