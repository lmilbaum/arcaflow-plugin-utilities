#!/usr/bin/env python3

import sys
import typing
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from arcaflow_plugin_sdk import plugin, validation, schema, annotations
import subprocess
import datetime
import yaml

@dataclass
class InputParams:
    """
    This is the data structure for the input parameters of the uuid plugin.
    """

@dataclass
class SuccessOutputUUID:
    """
    This is the output data structure for the success case.
    """

    uuid: str = field(
        metadata={
            "name": "UUID", 
            "description": "UUID generated for a workload run"
        }
    )
    

@dataclass
class ErrorOutput:
    """
    This is the output data structure in the error case.
    """
    exit_code: int = field(
        metadata={
            "name": "Exit Code", 
            "description": "Exit code returned by the program in case of a failure"
        }
    )
    error: str = field(
        metadata={
            "name": "Failure Error", 
            "description": "Reason for failure"
        }
    )

@plugin.step(
    id="uuid",
    name="Generate UUID",
    description="Generates a UUID which can be used by a workload",
    outputs={"success": SuccessOutputUUID, "error": ErrorOutput},
)
def generate_uuid(params: InputParams) -> typing.Tuple[str, typing.Union[SuccessOutputUUID, ErrorOutput]]:

    try:
        cmd=['uuidgen']
        uuid = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        uuid = uuid.decode("utf-8")
        uuid=uuid.strip()

        return "success", SuccessOutputUUID(uuid)
    except:
        return "error", ErrorOutput(1, "Failure generating UUID")


if __name__ == "__main__":
    sys.exit(
        plugin.run(
            plugin.build_schema(
                generate_uuid,
            )
        )
    )