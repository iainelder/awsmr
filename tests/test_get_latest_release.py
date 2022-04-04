import json
from os import chdir
from pathlib import Path
from typing import Callable, Generator, List

import httpretty  # type: ignore[import]
import pytest
from typing_extensions import TypedDict

from get_latest_release import get_latest_release, main, write_latest_release


class Ref(TypedDict):
    ref: str


RefRegistrar = Callable[[List[Ref]], None]


@pytest.fixture()
def register_refs() -> Generator[RefRegistrar, None, None]:

    httpretty.enable(allow_net_connect=False, verbose=True)

    def factory(refs: List[Ref]) -> None:
        response = json.dumps(refs, indent=2)
        httpretty.register_uri(
            httpretty.GET,
            "https://api.github.com/repos/aws/aws-cli/git/refs/tags",
            body=response,
        )

    yield factory

    httpretty.reset()
    httpretty.disable()


@pytest.fixture()
def tmp_cwd(tmp_path: Path):
    old_cwd = Path.cwd()
    chdir(tmp_path)
    yield tmp_path
    chdir(old_cwd)


def test_error_when_no_1_version(register_refs: RefRegistrar) -> None:
    register_refs([Ref(ref="refs/tags/2.0")])
    with pytest.raises(AssertionError):
        get_latest_release()


def test_get_one_release(register_refs: RefRegistrar) -> None:
    register_refs([Ref(ref="refs/tags/1.0")])
    assert get_latest_release() == "1.0"


def test_get_later_release(register_refs: RefRegistrar) -> None:
    register_refs([Ref(ref="refs/tags/1.0"), Ref(ref="refs/tags/1.1")])
    assert get_latest_release() == "1.1"


def test_write_latest_release(tmp_cwd: Path):
    write_latest_release("1.23.45")
    assert (tmp_cwd / "aws_cli_release").read_text() == "1.23.45"


def test_main(register_refs: RefRegistrar, tmp_cwd: Path):
    register_refs([Ref(ref="refs/tags/1.0"), Ref(ref="refs/tags/1.1")])
    main()
    assert (tmp_cwd / "aws_cli_release").read_text() == "1.1"
