import datetime as dt
import typing

import requests

ROOT_URL = "https://launchermeta.mojang.com/mc/game/version_manifest.json"

VersionMeta = typing.NamedTuple(
    "VersionMeta",
    [
        ("id", str),
        ("type", str),
        ("url", str),
        ("time", dt.datetime),
        ("release_time", dt.datetime),
    ],
)

_cached_meta = None


def _load_meta() -> typing.Tuple[typing.Iterable["VersionMeta"], str, str]:
    global _cached_meta

    def _parse_meta_item(meta: dict):
        return VersionMeta(
            id=meta["id"],
            type=meta["type"],
            url=meta["url"],
            time=dt.datetime.strptime(meta["time"], "%Y-%m-%dT%H:%M:%S%z"),
            release_time=dt.datetime.strptime(
                meta["releaseTime"], "%Y-%m-%dT%H:%M:%S%z"
            ),
        )

    if _cached_meta is not None:
        return _cached_meta

    data = requests.get(ROOT_URL).json()
    latest_release = data["latest"]["release"]
    latest_snapshot = data["latest"]["snapshot"]

    _cached_meta = (
        list(map(_parse_meta_item, data["versions"])),
        latest_release,
        latest_snapshot,
    )
    return _cached_meta


def get_versions():
    """Returns a list of all the available versions

    :Example:

    >>> from mojang.minecraft import launchermeta
    >>> launchermeta.get_versions()
    (['22w18a', '22w17a', '22w16b', ..., 'rd-20090515', 'rd-132328', 'rd-132211'], '1.18.2', '22w18a')
    """
    versions, latest_rel, latest_snap = _load_meta()
    version_list = list(map(lambda meta: meta.id, versions))
    return version_list, latest_rel, latest_snap


def get_version(
    version: str = "latest", snapshot: bool = False
) -> typing.Optional["VersionMeta"]:
    """Returns information about a specific version

    :param str version: The version you want to retrieve (default: 'latest')
    :param bool snapshot: If True include latest snapshot. Only used when version is set to 'latest'

    :Example:

    >>> from mojang.minecraft import launchermeta
    >>> launchermeta.get_version("1.18.1")
    VersionMeta(
        id='1.18.2',
        type='release',
        url='https://launchermeta.mojang.com/v1/packages/86f9645f8398ec902cd17769058851e6fead68cf/1.18.2.json',
        time=datetime.datetime(2022, 2, 28, 10, 48, 16, tzinfo=datetime.timezone.utc),
        release_time=datetime.datetime(2022, 2, 28, 10, 42, 45, tzinfo=datetime.timezone.utc)
    )
    """
    versions, latest_rel, latest_snap = _load_meta()

    if version == "latest":
        version = latest_snap if snapshot is True else latest_rel

    match = list(filter(lambda meta: meta.id == version, versions))
    if len(match) > 0:
        return match[0]

    return None
