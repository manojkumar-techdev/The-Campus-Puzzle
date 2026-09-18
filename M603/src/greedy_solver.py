"""greedy_solver.py -- Stage 1: Greedy baseline scheduler."""

from typing import Dict, List

from src.data_loader import Problem
from src.schedule import Schedule


def solve(problem: Problem) -> Schedule:
    """
    Greedy baseline: sort classes by enrolment descending (with class ID
    tiebreak), then place each into the first valid (slot, room) pair.

    The greedy scheduler deliberately does NOT enforce professor or
    student-group constraints -- it is a naive baseline. Later stages
    (graph colouring, DP, backtracking) enforce the full hard-constraint
    set. This is why the greedy conflict count is non-zero and why the
    later stages represent a substantial improvement.
    """
    schedule = Schedule(problem)

    classes_sorted = sorted(
        problem.classes, key=lambda c: (-c.enrolled, c.id)
    )
    rooms_asc = sorted(problem.rooms, key=lambda r: r.capacity)

    for cls in classes_sorted:
        placed = False
        for slot in problem.time_slots:
            for room in rooms_asc:
                if room.capacity < cls.enrolled:
                    continue
                if schedule._room_taken(slot, room.id):
                    continue
                schedule.assign(cls, slot, room, stage="greedy")
                placed = True
                break
            if placed:
                break
        if not placed:
            schedule.mark_unscheduled(cls.id)

    return schedule


def analyse_student_conflicts(schedule: Schedule) -> Dict:
    """Count student-group conflicts: pairs in the same slot sharing a group."""
    assignments = list(schedule.assignments.values())
    conflicts = []
    for i in range(len(assignments)):
        for j in range(i + 1, len(assignments)):
            a, b = assignments[i], assignments[j]
            if a.slot != b.slot:
                continue
            cls_a = schedule.problem.class_by_id[a.class_id]
            cls_b = schedule.problem.class_by_id[b.class_id]
            if set(cls_a.student_groups) & set(cls_b.student_groups):
                conflicts.append((a.class_id, b.class_id))
    return {"conflict_count": len(conflicts), "conflicts": conflicts}


def report(schedule: Schedule) -> str:
    lines = []
    lines.append("  Greedy Baseline Report")
    lines.append("  " + "-" * 55)
    lines.append(f"  Classes scheduled      : {schedule.scheduled_count()}")
    lines.append(f"  Classes unscheduled    : {schedule.unscheduled_count()}")
    lines.append(f"  Total wasted seats     : {schedule.total_wasted()}")
    info = analyse_student_conflicts(schedule)
    lines.append(f"  Student-group conflicts: {info['conflict_count']}")
    return "\n".join(lines)