from pydantic import BaseModel, Field, model_validator, ValidationError
from typing_extensions import Self
from enum import Enum
from datetime import datetime


class ContactType(Enum):
    radio = 1
    visual = 2
    physical = 3
    telepathic = 4


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode='after')
    def validate_contact(self) -> Self:
        errors: list[str] = []

        if self.contact_id[:2] != "AC":
            errors.append('Contact ID must start with "AC"')
        if (
            self.contact_type == ContactType.physical
            and self.is_verified is not True
        ):
            errors.append("Physical contact reports must be verified")
        if (
            self.contact_type == ContactType.telepathic
            and self.witness_count < 3
        ):
            errors.append("Telepathic contact requires at least 3 witnesses")
        if self.signal_strength > 7.0 and self.message_received is None:
            errors.append(
                "Strong signals (> 7.0) should include received messages")

        if errors:
            raise ValueError("\n".join(errors))

        return self


def print_contact(AC: AlienContact) -> None:
    print("Valid contact report:")
    print(f"ID: {AC.contact_id}")
    print(f"Type: {AC.contact_type.name}")
    print(f"Location: {AC.location}")
    print(f"Signal: {AC.signal_strength}/10")
    print(f"Duration: {AC.duration_minutes} minutes")
    print(f"Witnesses: {AC.witness_count}")
    print(f"Contact Time: {AC.timestamp.strftime('%d/%m/%Y')}")
    if AC.message_received:
        print(f"Message: {AC.message_received}")
    if AC.is_verified:
        print("Report: Verified")
    else:
        print("Report: Not Verified")


def main():

    print("\nAlien Contact Log Validation")
    print("========================================")
    try:
        contact1 = AlienContact(
            contact_id="AC_2026_001",
            timestamp=datetime.now(),
            location="Antarctic Research Station",
            contact_type=ContactType.radio,
            signal_strength=8.8,
            duration_minutes=2,
            witness_count=5,
            message_received="Wow!: 6EQUJ5",
            is_verified=True
        )
        print_contact(contact1)
    except ValidationError as error:
        for each in error.errors():
            print(f"{each['msg']}")

    print("\n========================================")
    try:
        contact1 = AlienContact(
            contact_id="Ac_2026_001",
            timestamp=datetime.now(),
            location="Antarctic Research Station",
            contact_type=ContactType.telepathic,
            signal_strength=8.8,
            duration_minutes=2,
            witness_count=1,
            is_verified=False
        )
        print_contact(contact1)
    except ValidationError as error:
        for each in error.errors():
            print("Expected validation error:")
            print(f"{each['msg']}")


if __name__ == '__main__':
    main()
