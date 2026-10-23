from dataclasses import asdict, dataclass
from typing import Any

@dataclass
class Student:
    student_id:int
    name:str
    email:str
    marks:float

    def to_dict(self) -> dict[str,Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls,data:dict[str,Any]) -> "Student":
        return cls(
            student_id=int(data["student_id"]),
            name=str(data["name"]),
            email=str(data["email"]),
            marks=float(data["marks"]),
        )   