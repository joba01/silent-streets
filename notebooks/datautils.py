import os


def create_folders(folder_list):
    """
    Creates folders from a list of folder paths if they do not already exist.
    Args:
        folder_list (list of str): A list of folder paths to be created.
    Returns:
        None
    Side Effects:
        Creates directories on the filesystem if they do not exist.
        Prints a message indicating whether each folder was created or already existed.
    """

    for folder in folder_list:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Folder '{folder}' created.")
        else:
            print(f"Folder '{folder}' already exists.")


class DataPaths:
    """
    A class to manage and organize data paths for various datasets and cache directories.

    Attributes:
    -----------
    data_path : str
        The base directory for data storage.
    cache : str
        The directory path for cached data.
    wikipedia : str
        The directory path for Wikipedia data.
    osm : str
        The directory path for OpenStreetMap (OSM) data.
    statistik_austria : str
        The directory path for Statistik Austria data.
    maps : str
        The directory path for map data.
    html : str
        The directory path for HTML data.

    Methods:
    --------
    __init__(base_dir: str = "data"):
        Initializes the DataPaths object with the specified base directory and creates necessary folders.
    """

    def __init__(self, base_dir: str = "data"):
        self.data_path = base_dir
        self.cache = f"{base_dir}/cache"
        self.wikipedia = f"{base_dir}/external/wikipedia"
        self.osm = f"{base_dir}/external/osm"
        self.statistik_austria = f"{base_dir}/external/statistik_austria"
        self.maps = f"{base_dir}/maps"
        self.html = f"{base_dir}/html"
        create_folders(
            [
                self.cache,
                self.wikipedia,
                self.osm,
                self.statistik_austria,
                self.maps,
                self.html,
            ]
        )
