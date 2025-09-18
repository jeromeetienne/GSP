from typing import Any
import numpy as np
from .transform_base import TransformBase

from .links import TransformAssertShape
from .links import TransformImmediate
from .links import TransformLoad
from .links import TransformMathOp

class TransformSerialisation:

    @staticmethod
    def to_json(transformBase: TransformBase) -> list[dict[str, Any]]:
        """
        Convert the transformation chain to a JSON-serializable array.
        """

        # Find the first transform in the chain
        first_transform = transformBase
        while first_transform.previous_transform is not None:
            first_transform = first_transform.previous_transform

        # Traverse the chain and build the JSON array
        json_array = []
        current_transform = first_transform
        while current_transform is not None:
            # Convert this transform to JSON
            json_array.append(current_transform._to_json())
            # Move to the next transform
            current_transform = current_transform.next_transform

        return json_array


    @staticmethod
    def from_json(json_array: list[dict[str, Any]]) -> "TransformBase":
        """
        Convert a JSON-serializable array to a transformation chain.
        """

        if not json_array:
            raise ValueError("JSON array MUST NOT be empty")

        def get_link_instance(json_dict: dict) -> TransformBase:
            class_type = json_dict.get("type")
            if class_type is None:
                raise ValueError("JSON dictionary MUST contain a 'type' field")

            # FIXME those hardcoded strings are error-prone and should be avoided - have that to be dynamic - similar in transform_helper.py
            if class_type == "TransformLoad":
                link_instance = TransformLoad._from_json(json_dict)
            elif class_type == "TransformMathOp":
                link_instance = TransformMathOp._from_json(json_dict)
            elif class_type == "TransformImmediate":
                link_instance = TransformImmediate._from_json(json_dict)
            elif class_type == "TransformAssertShape":
                link_instance = TransformAssertShape._from_json(json_dict)
            else:
                raise ValueError(f"Unknown transform type: {class_type}")

            return link_instance

        # Create the first transform
        current_transform = get_link_instance(json_array[0])

        # Create and chain the remaining transforms
        for json_dict in json_array[1:]:
            next_transform = get_link_instance(json_dict)
            current_transform = current_transform.chain(next_transform)

        # Find the first transform in the chain
        first_transform = current_transform
        while first_transform.previous_transform is not None:
            first_transform = first_transform.previous_transform

        return first_transform
