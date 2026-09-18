"""optimizer.py -- Stage 3: Dynamic Programming room allocator."""

from typing import Dict, List, Tuple

from src.data_loader import Class, Problem, Room
from src.schedule import Schedule


# A skip must be far more expensive than any possible waste, so the DP
# only skips a class when no room can physically accommodate it.
SKIP_PENALTY = 10 ** 9


def _dp_slot(
    classes: List[Class],
    rooms: List[Room],
) -> Tuple[List[Tuple[Class, Room]], List[Class]]:
    """
    Bitmask DP for one time slot.

    State : dp[i][mask] = min total waste after assigning the first i
            classes using exactly the rooms represented by `mask`.
    Base  : dp[0][0] = 0
    Trans : either skip class i (cost += SKIP_PENALTY) or assign it to
            some free room r that fits (cost += room[r].cap - enrolled).
    """
    n = len(classes)
    R = len(rooms)
    size = 1 << R
    INF = float("inf")

    prev = [INF] * size
    prev[0] = 0
    parents: List[List] = []

    for i in range(n):
        curr = [INF] * size
        parent_i = [None] * size
        cls = classes[i]

        for mask in range(size):
            if prev[mask] == INF:
                continue

            # Option 1: skip class i
            skip_cost = prev[mask] + SKIP_PENALTY
            if skip_cost < curr[mask]:
                curr[mask] = skip_cost
                parent_i[mask] = (mask, None)

            # Option 2: assign class i to a free, feasible room
            for r in range(R):
                if mask & (1 << r):
                    continue
                if rooms[r].capacity < cls.enrolled:
                    continue
                new_mask = mask | (1 << r)
                waste = rooms[r].capacity - cls.enrolled
                cost = prev[mask] + waste
                if cost < curr[new_mask]:
                    curr[new_mask] = cost
                    parent_i[new_mask] = (mask, r)

        parents.append(parent_i)
        prev = curr

    best_mask = min(range(size), key=lambda m: prev[m])

    # Reconstruct
    assignments: List[Tuple[Class, Room]] = []
    unassigned: List[Class] = []
    mask = best_mask
    for i in range(n - 1, -1, -1):
        p = parents[i][mask]
        if p is None:
            unassigned.append(classes[i])
            continue
        prev_mask, r = p
        if r is None:
            unassigned.append(classes[i])
        else:
            assignments.append((classes[i], rooms[r]))
        mask = prev_mask

    assignments.reverse()
    unassigned.reverse()
    return assignments, unassigned


def allocate_rooms(problem: Problem, coloring: Dict[str, str]) -> Schedule:
    schedule = Schedule(problem)

    # Group classes by their Stage-2 slot
    slot_classes: Dict[str, List[Class]] = {s: [] for s in problem.time_slots}
    for cid, slot in coloring.items():
        slot_classes[slot].append(problem.class_by_id[cid])

    # Uncoloured classes (Stage 2 could not assign a slot)
    for cls in problem.classes:
        if cls.id not in coloring:
            schedule.mark_unscheduled(cls.id)

    rooms = sorted(problem.rooms, key=lambda r: r.capacity)

    for slot, classes in slot_classes.items():
        if not classes:
            continue
        classes = sorted(classes, key=lambda c: (-c.enrolled, c.id))
        assignments, skipped = _dp_slot(classes, rooms)

        for cls, room in assignments:
            schedule.assign(cls, slot, room, stage="dp")
        for cls in skipped:
            schedule.mark_unscheduled(cls.id)

    return schedule


def report(problem, dp_schedule, greedy_wasted) -> str:
    saved = greedy_wasted - dp_schedule.total_wasted()
    lines = []
    lines.append("  DP Room Allocator Report")
    lines.append("  " + "-" * 55)
    lines.append(f"  Classes scheduled      : {dp_schedule.scheduled_count()}")
    lines.append(f"  Classes unscheduled    : {dp_schedule.unscheduled_count()}")
    lines.append(f"  Total wasted seats     : {dp_schedule.total_wasted()}")
    lines.append(f"  Greedy wasted seats    : {greedy_wasted}")
    lines.append(f"  Waste saved vs greedy  : {saved}")
    return "\n".join(lines)