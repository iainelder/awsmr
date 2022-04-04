import json
from textwrap import dedent
from typing import Callable, Generator, List

import httpretty  # type: ignore[import]
import pytest
from typing_extensions import TypedDict

from get_latest_release import get_latest_release


class Ref(TypedDict):
    ref: str


RefFactory = Callable[[List[Ref]], None]


@pytest.fixture()
def register_refs() -> Generator[RefFactory, None, None]:

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


def test_error_when_no_1_version(register_refs: RefFactory) -> None:
    register_refs([Ref(ref="refs/tags/2.0")])
    with pytest.raises(AssertionError):
        get_latest_release()


def test_get_one_release(register_refs: RefFactory) -> None:
    register_refs([Ref(ref="refs/tags/1.0")])
    assert get_latest_release() == "1.0"


def test_get_later_release(register_refs: RefFactory) -> None:
    register_refs([Ref(ref="refs/tags/1.0"), Ref(ref="refs/tags/1.1")])
    assert get_latest_release() == "1.1"
