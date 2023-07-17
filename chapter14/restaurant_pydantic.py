from typing import Literal

import yaml  # type: ignore[import]
from pydantic import PositiveInt, ValidationError, constr
from pydantic.dataclasses import dataclass


@dataclass
class AccountAndRoutingNumber:
    account_number: constr(min_length=9, max_length=9)
    routing_number: constr(min_length=8, max_length=12)


@dataclass
class BankDetails:
    bank_details: AccountAndRoutingNumber


@dataclass
class Address:
    address: constr(min_length=1)


AddressOrBankDetails = Address | BankDetails

Position = Literal["Chef", "Sous Chef", "Host", "Server", "Delivery Driver"]


@dataclass
class Employee:
    name: str
    position: Position
    payment_details: AddressOrBankDetails


@dataclass
class Dish:
    name: constr(min_length=1, max_length=16)
    price_in_cents: PositiveInt
    description: constr(min_length=1, max_length=80)
    picture: str | None = None


@dataclass
class Restaurant:
    name: constr(regex=r"^[a-zA-Z0-9 ]*$", min_length=1, max_length=16)
    owner: constr(min_length=1)
    address: constr(min_length=1)
    employees: list[Employee]
    dishes: list[Dish]
    number_of_seats: PositiveInt
    to_go: bool
    delivery: bool


def load_restaurant(filename: str) -> Restaurant:
    with open(filename) as yaml_file:
        data = yaml.safe_load(yaml_file)
        return Restaurant(**data)


if __name__ == "__main__":
    # restaurant = load_restaurant("restaurant.yaml")

    try:
        _ = Restaurant(
            **{  # type: ignore[arg-type]
                "name": "Dine-n-Dash",
                "owner": "Pat Viafore",
                "address": "123 Fake St.",
                "employees": [],
                "dishes": [],
                "number_of_seats": -5,
                "to_go": False,
                "delivery": True,
            }
        )
        assert False, "should not have been able to construct Restaurant"
    except ValidationError:
        pass

    try:
        _ = load_restaurant("missing.yaml")
        assert False, "should have failed"
    except ValidationError:
        pass

    try:
        _ = load_restaurant("wrong_type.yaml")
        assert False, "should have failed"
    except ValidationError:
        pass
