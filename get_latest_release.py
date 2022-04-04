from pathlib import Path

import requests
from more_itertools import tail


def main() -> None:
    latest_release = get_latest_release()
    write_latest_release(latest_release)
    print(latest_release)


def get_latest_release() -> str:
    """Returns the latest release of the AWS CLI version 1.x branch."""
    tags = requests.get("https://api.github.com/repos/aws/aws-cli/git/refs/tags").json()
    version_1_tags = (t for t in tags if t["ref"].startswith("refs/tags/1."))

    try:
        last_tag = next(tail(1, version_1_tags))
        return last_tag["ref"].rsplit("/", maxsplit=1)[1]
    except StopIteration:
        raise AssertionError(tags)


def write_latest_release(release_version: str) -> None:
    Path("aws_cli_release").write_text(release_version)


if __name__ == "__main__":
    main()
