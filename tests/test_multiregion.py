import pytest

from multiregion import multiregion, response_or_exception


@pytest.fixture
def scalar_function():
    def scalar(*, region_name):
        return f"scalar from {region_name}"

    return scalar


@pytest.fixture
def scalar_failing_in_toybox():
    def scalar(*, region_name):
        if "toybox" in region_name:
            raise ServiceError(f"Failed in {region_name}")
        return f"scalar from {region_name}"

    return scalar


class ServiceError(RuntimeError):
    pass


def test_one_region_scalar(scalar_function):
    expected = [{"RegionName": "eu-toybox-1", "Response": "scalar from eu-toybox-1"}]
    mr_scalar = multiregion(scalar_function, region_names=["eu-toybox-1"])
    assert mr_scalar() == expected


@pytest.mark.parametrize(
    "input",
    [[], tuple(), (r for r in []), None],
    ids=["empty list", "empty tuple", "empty generator", "None"],
)
def test_invalid_regions(scalar_function, input):
    with pytest.raises(
        ValueError, match="region_names must be an iterable of at least one region name"
    ):
        multiregion(scalar_function, region_names=input)


def test_two_regions_scalar(scalar_function):
    expected = [
        {
            "RegionName": "us-sandpit-1",
            "Response": "scalar from us-sandpit-1",
        },
        {"RegionName": "eu-toybox-1", "Response": "scalar from eu-toybox-1"},
    ]
    mr_scalar = multiregion(
        scalar_function, region_names=["us-sandpit-1", "eu-toybox-1"]
    )
    assert mr_scalar() == expected


def test_failure_in_toybox(scalar_failing_in_toybox):
    expected = [
        {
            "RegionName": "eu-toybox-1",
            "Exception": repr(ServiceError(f"Failed in eu-toybox-1")),
        }
    ]
    mr_func = multiregion(scalar_failing_in_toybox, region_names=["eu-toybox-1"])
    assert mr_func() == expected


def test_format_scalar_response():
    assert response_or_exception(lambda: "OK") == {"Response": "OK"}


def test_format_none_response():
    assert response_or_exception(lambda: None) == {"Response": None}


def test_format_exception():
    def fail():
        raise ServiceError("toybox on fire")

    assert response_or_exception(fail) == {"Exception": repr(Exception("toybox on fire"))}
