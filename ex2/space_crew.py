from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, model_validator, ValidationError
from typing_extensions import Self


class CrewRanks(str, Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: CrewRanks
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def validate_mission(self) -> Self:
        errors: list[str] = []
        leader_satisfied: bool = False
        experienced_member = 0
        total_member = len(self.crew)
        not_active_found = False

        # check crew member requirements
        for member in self.crew:
            if (
                member.rank == CrewRanks.commander
                or member.rank == CrewRanks.captain
            ):
                leader_satisfied = True
            if member.years_experience >= 5:
                experienced_member += 1
            if not member.is_active:
                not_active_found = True

        if not self.mission_id.startswith("M"):
            errors.append('Mission ID must start with "M"')
        if not leader_satisfied:
            errors.append(
                "Mission must have at least one "
                "Commander or Captain"
            )
        if (
            self.duration_days > 365 and
            experienced_member * 2 < total_member
        ):
            errors.append(
                "Long missions (> 365 days) need 50% "
                "experienced crew (5+ years)"
            )
        if not_active_found:
            errors.append("All crew members must be active")

        if errors:
            raise ValueError("\n".join(errors))

        return self


def print_mission(mission: SpaceMission) -> None:
    print("Valid mission created:")
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew members:")
    for member in mission.crew:
        print(
            f"- {member.name} ({member.rank.value}) - "
            f"{member.specialization}"
        )


def main() -> None:

    print("\nSpace Mission Crew Validation")
    print("========================================")
    try:
        crew_member1 = CrewMember(
            member_id="CM0001",
            name="Sarah Connor",
            rank=CrewRanks.commander,
            age=58,
            specialization="Mission Command",
            years_experience=37,
            is_active=True
        )

        crew_member2 = CrewMember(
            member_id="CM0002",
            name="John Smith",
            rank=CrewRanks.lieutenant,
            age=45,
            specialization="Navigation",
            years_experience=23,
            is_active=True
        )

        crew_member3 = CrewMember(
            member_id="CM0003",
            name="Alice Johnson",
            rank=CrewRanks.officer,
            age=33,
            specialization="Engineering",
            years_experience=15,
            is_active=True
        )

        mission1 = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime.now(),
            duration_days=900,
            crew=[crew_member1, crew_member2, crew_member3],
            mission_status="in planning",
            budget_millions=2500.0
        )
        print_mission(mission1)
    except ValidationError as error:
        for each in error.errors():
            if each["loc"]:
                print(f"{each['loc'][0]}: {each['msg']}")
            else:
                print(each["msg"].removeprefix("Value error, "))

    print("\n========================================")
    try:
        crew_member4 = CrewMember(
            member_id="CM0004",
            name="Thomas Brown",
            rank=CrewRanks.cadet,
            age=25,
            specialization="Security",
            years_experience=3,
            is_active=True
        )

        mission2 = SpaceMission(
            mission_id="M2026_Europa",
            mission_name="Europa Research Data Collection",
            destination="Europa",
            launch_date=datetime.now(),
            duration_days=1001,
            crew=[crew_member2, crew_member3, crew_member4],
            mission_status="in planning",
            budget_millions=5500.0
        )
        print_mission(mission2)
    except ValidationError as error:
        for each in error.errors():
            print("Expected validation error:")
            if each["loc"]:
                print(f"{each['loc'][0]}: {each['msg']}")
            else:
                print(each["msg"].removeprefix("Value error, "))


if __name__ == '__main__':
    main()
