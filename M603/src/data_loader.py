"""data_loader.py -- Loads and validates constraints.json."""

import json
import os
from dataclasses import dataclass, field
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class Room:
    id: str
    capacity: int


@dataclass(frozen=True)
class Class:
    id: str
    enrolled: int
    professor_id: str
    student_groups: Tuple[str, ...] = ()


@dataclass
class Problem:
    classes: List[Class]
    rooms: List[Room]
    time_slots: List[str]
    class_by_id: Dict[str, Class] = field(default_factory=dict)
    room_by_id: Dict[str, Room] = field(default_factory=dict)

    def __post_init__(self):
        if not self.class_by_id:
            self.class_by_id = {c.id: c for c in self.classes}
        if not self.room_by_id:
            self.room_by_id = {r.id: r for r in self.rooms}

    def summary(self) -> str:
        total_students = sum(c.enrolled for c in self.classes)
        total_capacity = sum(r.capacity for r in self.rooms)
        lines = [
            f"    Classes       : {len(self.classes)}",
            f"    Rooms         : {len(self.rooms)}",
            f"    Time slots    : {len(self.time_slots)}",
            f"    Total students: {total_students}",
            f"    Total capacity: {total_capacity}",
        ]
        return "\n".join(lines)


DEFAULT_PATH = os.path.join("data", "constraints.json")


def load(path: str = None) -> Problem:
    if path is None:
        path = DEFAULT_PATH

    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    rooms = [
        Room(id=r["id"], capacity=int(r["capacity"]))
        for r in raw["rooms"]
    ]

    classes = [
        Class(
            id=c["id"],
            enrolled=int(c["enrolled"]),
            professor_id=c["professor_id"],
            student_groups=tuple(c.get("student_groups", [])),
        )
        for c in raw["classes"]
    ]

    time_slots = list(raw["time_slots"])

    return Problem(
        classes=classes,
        rooms=rooms,
        time_slots=time_slots,
    )