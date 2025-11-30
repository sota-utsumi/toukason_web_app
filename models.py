# models.py
from dataclasses import dataclass, asdict
from typing import Literal

Role = Literal["代表", "開発", "イベント企画", "SNS広報", "学び舎", "外部連携"]

ROLE_COLORS: dict[Role, str] = {
    "代表": "#ff99cc",
    "開発": "#66cc66",
    "イベント企画": "#ffeb66",
    "SNS広報": "#ff6666",
    "学び舎": "#6699ff",
    "外部連携": "#aaaaaa",
}

ROLE_ORDER: list[Role] = ["代表", "開発", "イベント企画", "SNS広報", "学び舎", "外部連携"]


@dataclass
class Member:
    id: int
    name: str
    role: Role
    grade: str = ""
    faculty: str = ""
    department_course: str = ""
    lab: str = ""
    likes: str = ""
    skills: str = ""
    belongs: str = ""
    wanna_learn: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "Member":
        # 足りないキーがあっても落ちないように補完
        defaults = {
            "grade": "",
            "faculty": "",
            "department_course": "",
            "lab": "",
            "likes": "",
            "skills": "",
            "belongs": "",
            "wanna_learn": "",
        }
        merged = {**defaults, **data}
        return cls(**merged)
