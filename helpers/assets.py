"""
The load_asset function loads assets based on the information in the models.assets.Asset object.
It sets the mimetype, reads the asset value from the corresponding file, and handles exceptions.
"""

import pathlib
import exceptions.assets
import exceptions.universal
import models.assets

mimetypes = {
    "css": "text/css",
    "gif": "image/gif",
    "html": "text/html",
    "htm": "text/html",
    "ico": "image/vnd.microsoft.icon",
    "jpeg": "image/jpeg",
    "jpg": "image/jpeg",
    "js": "text/javascript",
    "json": "application/json",
    "mp3": "audio/mpeg",
    "mp4": "video/mp4",
    "png": "image/png",
    "txt": "text/plain",
    "weba": "audio/webm",
    "webm": "video/webm",
    "webp": "image/webp",
    "xml": "application/xml",
}

read_modes = {
    "r": ["css", "html", "htm", "js", "json", "txt", "xml"],
    "rb": ["gif", "ico", "jpeg", "jpg", "mp3", "mp4", "png", "weba", "webm", "webp"]
}


def load_asset(asset: models.assets.Asset) -> models.assets.Asset:
    if not asset.filetype or not asset.name:
        raise exceptions.universal.InvalidArgumentsException("'filetype', 'name' have to be specified.")

    if not asset.mimetype:
        try:
            asset.mimetype = mimetypes[asset.filetype.__str__()]
        except KeyError:
            raise exceptions.assets.FileTypeNotFoundException(f"filetype '{asset.filetype}' is not supported.")

    if not asset.value:
        read_mode = next(i for i, modes in read_modes.items() if asset.filetype.__str__() in modes)
        try:
            with open(f"{str(pathlib.Path(__file__).parent.parent.resolve())}/assets/"
                      f"{asset.filetype.__str__()}/{asset.name.__str__()}.{asset.filetype.__str__()}",
                      read_mode, encoding="utf-8" if not "b" in read_mode else None) as f:
                asset.value = f.read()
        except FileNotFoundError:
            raise exceptions.assets.FileNotFoundException(
                f"file '{asset.filetype.__str__()}/{asset.name.__str__()}.{asset.filetype.__str__()}' was not found.")

    return asset
