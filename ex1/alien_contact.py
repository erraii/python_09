from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field, model_validator, ValidationError
from typing_extensions import Self


class ContactType(str, Enum):
    radio = "radio"
    visual = "visual"
    physical = "physical"
    telepathic = "telepathic"


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

        if not self.contact_id.startswith("AC"):
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


def print_contact(contact: AlienContact) -> None:
    print("Valid contact report:")
    print(f"ID: {contact.contact_id}")
    print(f"Type: {contact.contact_type.value}")
    print(f"Location: {contact.location}")
    print(f"Signal: {contact.signal_strength}/10")
    print(f"Duration: {contact.duration_minutes} minutes")
    print(f"Witnesses: {contact.witness_count}")
    print(f"Contact Time: {contact.timestamp.strftime('%d/%m/%Y')}")
    if contact.message_received:
        print(f"Message: {contact.message_received}")
    if contact.is_verified:
        print("Report: Verified")
    else:
        print("Report: Not Verified")


def main() -> None:

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
            message_received="Wow!-> 6EQUJ5",
            is_verified=True
        )
        print_contact(contact1)
    except ValidationError as error:
        for each in error.errors():
            if each["loc"]:
                print(f"{each['loc'][0]}: {each['msg']}")
            else:
                print(each["msg"].removeprefix("Value error, "))

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
            if each["loc"]:
                print(f"{each['loc'][0]}: {each['msg']}")
            else:
                print(each["msg"].removeprefix("Value error, "))


if __name__ == '__main__':
    main()
