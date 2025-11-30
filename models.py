# models.py
from dataclasses import dataclass
from typing import Optional, Dict, Any, Literal

# 元の役割（app.py にあったものをそのまま採用）
Role = Literal["代表", "開発", "イベント企画", "SNS広報", "学び舎", "外部連携"]

# 役割ごとの色（カード表示などに使える）
ROLE_COLORS: dict[Role, str] = {
    "代表": "ff99cc",
    "開発": "66cc66",
    "イベント企画": "ffeb66",
    "SNS広報": "ff6666",
    "学び舎": "6699ff",
    "外部連携": "aaaaaa",
}

# 表示順
ROLE_ORDER: list[Role] = ["代表", "開発", "イベント企画", "SNS広報", "学び舎", "外部連携"]


@dataclass
class Member:
    id: Optional[int] = None
    name: str = ""
    role: Optional[Role] = None
    grade: Optional[str] = None
    faculty: Optional[str] = None
    department_course: Optional[str] = None
    lab: Optional[str] = None
    likes: Optional[str] = None
    skills: Optional[str] = None
    belongs: Optional[str] = None
    wanna_learn: Optional[str] = None

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Member":
        return Member(
            id=data.get("id"),
            name=data.get("name", ""),
            role=data.get("role"),
            grade=data.get("grade"),
            faculty=data.get("faculty"),
            department_course=data.get("department_course"),
            lab=data.get("lab"),
            likes=data.get("likes"),
            skills=data.get("skills"),
            belongs=data.get("belongs"),
            wanna_learn=data.get("wanna_learn"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "grade": self.grade,
            "faculty": self.faculty,
            "department_course": self.department_course,
            "lab": self.lab,
            "likes": self.likes,
            "skills": self.skills,
            "belongs": self.belongs,
            "wanna_learn": self.wanna_learn,
        }
