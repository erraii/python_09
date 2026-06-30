from pydantic import BaseModel, Field, ValidationError
from datetime import datetime


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(default=None, max_length=200)


def print_station(station: SpaceStation) -> None:
    print("Valid station created:")
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")
    # print(f"Last Maint.: {station.last_maintenance.strftime('%d/%m/%Y')}")
    if station.is_operational:
        print("Status: Operational")
    else:
        print("Status: Maintenance")
    if station.notes:
        print(f"notes: {station.notes}")


def main() -> None:
    print("\nSpace Station Data Validation")
    print("========================================")

    # STATION 1 - Valid Data
    try:
        station1 = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime.now(),
            # last_maintenance="2026-06-29T00:00:00"
            # notes="All systems nominal"
            )
        print_station(station1)
        print("\n========================================")

    except ValidationError as error:
        print("Expected validation error:")
        print(error.errors()[0]["msg"])

    # STATION 2 - Invalid data
    try:
        station2 = SpaceStation(
            station_id="TMO001",
            name="Titan Mining Outpost",
            # crew_size=20,
            crew_size=26,
            power_level=-5.8,
            # oxygen_level=62.3,
            oxygen_level=120.9,
            last_maintenance="5 July 2345",
            # last_maintenance="2026-04-25T00:00:00"
            # notes="Scheduled maintenance completed"
            )
        print_station(station2)
        print("\n========================================")

    except ValidationError as error:
        print("Expected validation error:")
        for each in error.errors():
            print(f"{each['loc'][0]}: {each['msg']}")

    # # STATION 3 - Valid, attribute init with with dictionary
    # try:
    #     external_data = {
    #         "station_id": "QCH001",
    #         "name": "Quantum Communications Hub",
    #         "crew_size": 16,
    #         "power_level": 55.1,
    #         "oxygen_level": 99.3,
    #         "last_maintenance": datetime.now(),
    #         # "last_maintenance": "2024-02-17T00:00:00",
    #         "is_operational": False
    #         notes="Power system requires inspection"
    #     }
    #     station3 = SpaceStation(**external_data)
    #     print_station(station3)
    #     print("\n========================================")

    # except ValidationError as error:
    #     print("Expected validation error:")
    #     print(error.errors()[0]["msg"])


if __name__ == '__main__':

    # Setup:
    # python3 -m venv .venv
    # source .venv/bin/activate
    # pip install "pydantic>=2,<3"
    # pip show pydantic
    main()
