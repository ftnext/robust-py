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
    print(f"{Model(value=0.5)=}")  # type: ignore[arg-type]

    try:
        Model2(value="0023")  # type: ignore[arg-type]
        assert False, "Model should have failed to parse"
    except ValidationError:
        pass
