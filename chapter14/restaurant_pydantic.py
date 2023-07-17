from typing import Literal

import yaml  # type: ignore[import]
from pydantic import ValidationError
from pydantic.dataclasses import dataclass


@dataclass
class AccountAndRoutingNumber:
    account_number: str
    routing_number: str


@dataclass
class BankDetails:
    bank_details: AccountAndRoutingNumber


@dataclass
class Address:
    address: str


AddressOrBankDetails = Address | BankDetails

Position = Literal["Chef", "Sous Chef", "Host", "Server", "Delivery Driver"]


@dataclass
class Employee:
    name: str
    position: Position
    payment_details: AddressOrBankDetails


@dataclass
class Dish:
    name: str
    price_in_cents: int
    description: str
    picture: str | None = None


@dataclass
class Restaurant:
    name: str
    owner: str
    address: str
    employees: list[Employee]
    dishes: list[Dish]
    number_of_seats: int
    to_go: bool
    delivery: bool


def load_restaurant(filename: str) -> Restaurant:
    with open(filename) as yaml_file:
        data = yaml.safe_load(yaml_file)
        return Restaurant(**data)


if __name__ == "__main__":
    restaurant = load_restaurant("restaurant.yaml")

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
