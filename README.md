# AWS CLI for multiple regions

This is a prototype for an AWS CLI that queries multiple regions in a single invocation.

## Examples

There's a new required argument called `--region-list`.

```text
$ poetry run awsmr ec2 describe-availability-zones

usage: aws [options] <command> <subcommand> [<subcommand> ...] [parameters]
To see help text, you can run:

  aws help
  aws <command> help
  aws <command> <subcommand> help
aws: error: the following arguments are required: --region-list
```

## You can still query a single region.

But the format is different. The response now shows the queried region name.

```text
$ poetry run awsmr ec2 describe-availability-zones --region-list eu-west-1
[
    {
        "RegionName": "eu-west-1",
        "Response": {
            "AvailabilityZones": [
                {
                    "State": "available",
                    "OptInStatus": "opt-in-not-required",
                    "Messages": [],
                    "RegionName": "eu-west-1",
                    "ZoneName": "eu-west-1a",
                    "ZoneId": "euw1-az3",
                    "GroupName": "eu-west-1",
                    "NetworkBorderGroup": "eu-west-1",
                    "ZoneType": "availability-zone"
                },
                {
                    "State": "available",
                    "OptInStatus": "opt-in-not-required",
                    "Messages": [],
                    "RegionName": "eu-west-1",
                    "ZoneName": "eu-west-1b",
                    "ZoneId": "euw1-az1",
                    "GroupName": "eu-west-1",
                    "NetworkBorderGroup": "eu-west-1",
                    "ZoneType": "availability-zone"
                },
                {
                    "State": "available",
                    "OptInStatus": "opt-in-not-required",
                    "Messages": [],
                    "RegionName": "eu-west-1",
                    "ZoneName": "eu-west-1c",
                    "ZoneId": "euw1-az2",
                    "GroupName": "eu-west-1",
                    "NetworkBorderGroup": "eu-west-1",
                    "ZoneType": "availability-zone"
                }
            ]
        }
    }
]
```

## Each region's results are returned as an item in a list.

```text
$ poetry run awsmr ec2 describe-availability-zones --region-list eu-west-1 eu-central-1
[
    {
        "RegionName": "eu-west-1",
        "Response": {
            "AvailabilityZones": [
                {
                    "State": "available",
                    "OptInStatus": "opt-in-not-required",
                    "Messages": [],
                    "RegionName": "eu-west-1",
                    "ZoneName": "eu-west-1a",
                    "ZoneId": "euw1-az3",
                    "GroupName": "eu-west-1",
                    "NetworkBorderGroup": "eu-west-1",
                    "ZoneType": "availability-zone"
                },
                {
                    "State": "available",
                    "OptInStatus": "opt-in-not-required",
                    "Messages": [],
                    "RegionName": "eu-west-1",
                    "ZoneName": "eu-west-1b",
                    "ZoneId": "euw1-az1",
                    "GroupName": "eu-west-1",
                    "NetworkBorderGroup": "eu-west-1",
                    "ZoneType": "availability-zone"
                },
                {
                    "State": "available",
                    "OptInStatus": "opt-in-not-required",
                    "Messages": [],
                    "RegionName": "eu-west-1",
                    "ZoneName": "eu-west-1c",
                    "ZoneId": "euw1-az2",
                    "GroupName": "eu-west-1",
                    "NetworkBorderGroup": "eu-west-1",
                    "ZoneType": "availability-zone"
                }
            ]
        }
    },
    {
        "RegionName": "eu-central-1",
        "Response": {
            "AvailabilityZones": [
                {
                    "State": "available",
                    "OptInStatus": "opt-in-not-required",
                    "Messages": [],
                    "RegionName": "eu-central-1",
                    "ZoneName": "eu-central-1a",
                    "ZoneId": "euc1-az2",
                    "GroupName": "eu-central-1",
                    "NetworkBorderGroup": "eu-central-1",
                    "ZoneType": "availability-zone"
                },
                {
                    "State": "available",
                    "OptInStatus": "opt-in-not-required",
                    "Messages": [],
                    "RegionName": "eu-central-1",
                    "ZoneName": "eu-central-1b",
                    "ZoneId": "euc1-az3",
                    "GroupName": "eu-central-1",
                    "NetworkBorderGroup": "eu-central-1",
                    "ZoneType": "availability-zone"
                },
                {
                    "State": "available",
                    "OptInStatus": "opt-in-not-required",
                    "Messages": [],
                    "RegionName": "eu-central-1",
                    "ZoneName": "eu-central-1c",
                    "ZoneId": "euc1-az1",
                    "GroupName": "eu-central-1",
                    "NetworkBorderGroup": "eu-central-1",
                    "ZoneType": "availability-zone"
                }
            ]
        }
    }
]
```

## You can use JMESPath as usual.

```
$ poetry run awsmr ec2 describe-availability-zones --region-list eu-west-1 eu-central-1 --query '[].Response[].AvailabilityZones[]'
[
    {
        "State": "available",
        "OptInStatus": "opt-in-not-required",
        "Messages": [],
        "RegionName": "eu-west-1",
        "ZoneName": "eu-west-1a",
        "ZoneId": "euw1-az3",
        "GroupName": "eu-west-1",
        "NetworkBorderGroup": "eu-west-1",
        "ZoneType": "availability-zone"
    },
    {
        "State": "available",
        "OptInStatus": "opt-in-not-required",
        "Messages": [],
        "RegionName": "eu-west-1",
        "ZoneName": "eu-west-1b",
        "ZoneId": "euw1-az1",
        "GroupName": "eu-west-1",
        "NetworkBorderGroup": "eu-west-1",
        "ZoneType": "availability-zone"
    },
    {
        "State": "available",
        "OptInStatus": "opt-in-not-required",
        "Messages": [],
        "RegionName": "eu-west-1",
        "ZoneName": "eu-west-1c",
        "ZoneId": "euw1-az2",
        "GroupName": "eu-west-1",
        "NetworkBorderGroup": "eu-west-1",
        "ZoneType": "availability-zone"
    },
    {
        "State": "available",
        "OptInStatus": "opt-in-not-required",
        "Messages": [],
        "RegionName": "eu-central-1",
        "ZoneName": "eu-central-1a",
        "ZoneId": "euc1-az2",
        "GroupName": "eu-central-1",
        "NetworkBorderGroup": "eu-central-1",
        "ZoneType": "availability-zone"
    },
    {
        "State": "available",
        "OptInStatus": "opt-in-not-required",
        "Messages": [],
        "RegionName": "eu-central-1",
        "ZoneName": "eu-central-1b",
        "ZoneId": "euc1-az3",
        "GroupName": "eu-central-1",
        "NetworkBorderGroup": "eu-central-1",
        "ZoneType": "availability-zone"
    },
    {
        "State": "available",
        "OptInStatus": "opt-in-not-required",
        "Messages": [],
        "RegionName": "eu-central-1",
        "ZoneName": "eu-central-1c",
        "ZoneId": "euc1-az1",
        "GroupName": "eu-central-1",
        "NetworkBorderGroup": "eu-central-1",
        "ZoneType": "availability-zone"
    }
]
```

The above example is convenient because the describe-availability-zones command includes the RegionName in the description of each zone. Most APIs don't do this.

If you did the same sort of flattening on other APIs, you'd lost the region information. As JMESPath doesn't yet support dynamic keys (see [jmespath.py issue #152](https://github.com/jmespath/jmespath.py/issues/152)), I don't think it's possible to retain this information in the flattened form without using another tool such as jq.

## Exceptions raised when running a regional command are captured.

```
$ poetry run awsmr workmail list-organizations --region-list eu-west-1 eu-central-1
[
    {
        "RegionName": "eu-west-1",
        "Response": {
            "OrganizationSummaries": []
        }
    },
    {
        "RegionName": "eu-central-1",
        "Exception": "EndpointConnectionError('Could not connect to the endpoint URL: \"https://workmail.eu-central-1.amazonaws.com/\"')"
    }
]
```

awsmr should never fail because of an exception raised by running a command in a region. The exception will be returned in that region's result object in place of the response.

# Generic formatter that includes exceptions

Use this jq filter to make the format more familiar. It returns the main key to the expected place and rolls up results from multiple regions into a single list.

```jq
.
| (map(select(.Response)) | map(.Response|keys[0])[0]) as $main_key
| {
    ($main_key): map(select(.Response)),
    "Exceptions": map(select(.Exception))
  }
| .[$main_key] |= (
    map(
        .
        | .RegionName as $rn
        | .Response[$main_key]
        | map(.RegionName = $rn)
    )
  )
'
```

```text

```

## TODO

* document installation using pipx
* more unit tests for exceptions
* packaging
* markdown linting
* integration tests in a real AWS account
* automatic build and test when awscli publishes a new version
* top level keys for the main result key and exceptions
