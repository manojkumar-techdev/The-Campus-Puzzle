"""schedule.py -- Schedule and Assignment data structures."""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from src.data_loader import Class, Problem, Room


@dataclass
class Assignment:
    class_id: str
    slot: str
    room_id: str
    stage: str = ""
    waste: int = 0

    def fit_label(self) -> str:
        if self.waste == 0:
            return "Perfect Fit"
        return f"Wasted {self.waste} seats"


class Schedule:
    def __init__(self, problem: Problem):
        self.problem = problem
        self.assignments: Dict[str, Assignment] = {}
        self.unscheduled: List[str] = []

    # ---------------- internal ----------------
    def _room_taken(self, slot: str, room_id: str) -> bool:
        for a in self.assignments.values():
            if a.slot == slot and a.room_id == room_id:
                return True
        return False

    # ---------------- validity ----------------
    def is_valid_placement(
        self,
        cls: Class,
        slot: str,
        room: Room,
        check_student_groups: bool = True,
        check_professor: bool = True,
    ) -> Tuple[bool, str]:
        if room.capacity < cls.enrolled:
            return False, "capacity"

        if self._room_taken(slot, room.id):
            return False, "room_occupied"

        for a in self.assignments.values():
            if a.slot != slot:
                continue
            other = self.problem.class_by_id[a.class_id]
            if check_professor and other.professor_id == cls.professor_id:
                return False, "professor_conflict"
            if check_student_groups and (
                set(other.student_groups) & set(cls.student_groups)
            ):
                return False, "student_group_conflict"

        return True, "ok"

    # ---------------- mutations ----------------
    def assign(self, cls: Class, slot: str, room: Room, stage: str = "") -> None:
        waste = max(0, room.capacity - cls.enrolled)
        self.assignments[cls.id] = Assignment(
            class_id=cls.id,
            slot=slot,
            room_id=room.id,
            stage=stage,
            waste=waste,
        )
        if cls.id in self.unscheduled:
            self.unscheduled.remove(cls.id)

    def unassign(self, cls: Class) -> None:
        self.assignments.pop(cls.id, None)

    def mark_unscheduled(self, class_id: str) -> None:
        if class_id not in self.unscheduled:
            self.unscheduled.append(class_id)

    # ---------------- metrics ----------------
    def scheduled_count(self) -> int:
        return len(self.assignments)

    def unscheduled_count(self) -> int:
        return len(self.unscheduled)

    def total_wasted(self) -> int:
        return sum(a.waste for a in self.assignments.values())

    # ---------------- reports ----------------
    def conflict_report(self) -> str:
        lines = []
        lines.append("=" * 65)
        lines.append("  FINAL CONFLICT REPORT")
        lines.append("=" * 65)
        lines.append(
            f"  {'Status':<12} {'Class':<10} {'Slot':<8} {'Room':<8} Fit"
        )
        lines.append("  " + "-" * 61)

        for a in sorted(
            self.assignments.values(), key=lambda x: (x.slot, x.class_id)
        ):
            lines.append(
                f"  {'Scheduled':<12} {a.class_id:<10} {a.slot:<8} "
                f"{a.room_id:<8} {a.fit_label()}"
            )

        for cid in sorted(self.unscheduled):
            lines.append(
                f"  {'Unscheduled':<12} {cid:<10} {'N/A':<8} {'N/A':<8} "
                f"-- FLAG FOR MANUAL REVIEW"
            )

        lines.append("=" * 65)
        return "\n".join(lines)