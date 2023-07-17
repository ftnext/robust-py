from pydantic import StrictInt, ValidationError
from pydantic.dataclasses import dataclass


@dataclass
class Model:
    value: int


@dataclass
class Model2:
    value: StrictInt


if __name__ == "__main__":
    print(f'{Model(value="123")=}')  # type: ignore[arg-type]

    # Pydantic V2では int_from_float error
    # https://docs.pydantic.dev/latest/usage/validation_errors/#int_from_float
    try:
        print(f"{Model(value=0.5)=}")  # type: ignore[arg-type]
    except ValidationError:
        pass

    try:
        Model2(value="0023")  # type: ignore[arg-type]
        assert False, "Model should have failed to parse"
    except ValidationError:
        pass
