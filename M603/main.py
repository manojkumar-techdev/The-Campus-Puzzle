"""
main.py
=======
Entry point for the M603 University Timetabling System.

Orchestrates all four algorithmic stages in sequence and prints
the final conflict report.

Usage
-----
    python main.py                  # uses default data/constraints.json
    python main.py --data path.json # use a custom constraints file

Output format (as specified in assessment brief)
------------------------------------------------
    Scheduled   CS101   09:00   R-101   Perfect Fit
    Scheduled   MATH202 10:00   R-105   Wasted 5 seats
    Unscheduled HIST101 N/A     N/A     -- FLAG FOR MANUAL REVIEW
"""

import argparse
import sys
import time

import src.data_loader as loader

# Stage imports — each raises NotImplementedError until implemented
from src.greedy_solver import solve as greedy_solve, report as greedy_report, analyse_student_conflicts
from src.graph_engine   import build_conflict_graph, welsh_powell_coloring, report as graph_report
from src.optimizer      import allocate_rooms, report as dp_report
from src.backtracker    import solve as backtrack_solve, report as bt_report


BANNER = """
╔══════════════════════════════════════════════════════════════╗
║      M603 Advanced Algorithms — University Timetabler        ║
║      Gisma University of Applied Sciences                    ║
╚══════════════════════════════════════════════════════════════╝
"""


def run(data_path: str = None):
    print(BANNER)

    # ------------------------------------------------------------------ #
    # 0. Load problem                                                      #
    # ------------------------------------------------------------------ #
    print("[0] Loading problem from constraints.json ...")
    problem = loader.load(data_path)
    print(problem.summary())

    # ------------------------------------------------------------------ #
    # 1. Stage 1 — Greedy Baseline                                         #
    # ------------------------------------------------------------------ #
    print("\n[1] Stage 1: Greedy Baseline Scheduler")
    t0 = time.perf_counter()
    try:
        greedy_schedule = greedy_solve(problem)
        elapsed = time.perf_counter() - t0
        print(f"    Completed in {elapsed*1000:.2f} ms")
        print()
        print(greedy_report(greedy_schedule))
    except NotImplementedError:
        print("    [STUB] Stage 1 not yet implemented.")
        greedy_schedule = None

    # ------------------------------------------------------------------ #
    # 2. Stage 2 — Graph Theory Conflict Engine                            #
    # ------------------------------------------------------------------ #
    print("\n[2] Stage 2: Graph Theory — Conflict Detection & Coloring")
    try:
        t0 = time.perf_counter()
        conflict_graph = build_conflict_graph(problem)
        coloring, uncolored = welsh_powell_coloring(conflict_graph, problem.time_slots)
        elapsed = time.perf_counter() - t0
        print(f"    Completed in {elapsed*1000:.2f} ms")
        print()
        # Pass greedy conflict count for the comparison table
        greedy_conflicts = (
            analyse_student_conflicts(greedy_schedule)["conflict_count"]
            if greedy_schedule is not None else 0
        )
        print(graph_report(problem, conflict_graph, coloring, uncolored, greedy_conflicts))
    except NotImplementedError:
        print("    [STUB] Stage 2 not yet implemented.")
        conflict_graph = None
        coloring       = None
        uncolored      = []

    # ------------------------------------------------------------------ #
    # 3. Stage 3 — Dynamic Programming Room Allocator                      #
    # ------------------------------------------------------------------ #
    print("\n[3] Stage 3: Dynamic Programming — Room Allocation")
    if coloring is not None:
        try:
            t0 = time.perf_counter()
            dp_schedule = allocate_rooms(problem, coloring)
            elapsed = time.perf_counter() - t0
            print(f"    Completed in {elapsed*1000:.2f} ms")
            print()
            greedy_waste = greedy_schedule.total_wasted() if greedy_schedule else 0
            print(dp_report(problem, dp_schedule, greedy_waste))
        except NotImplementedError:
            print("    [STUB] Stage 3 not yet implemented.")
            dp_schedule = None
    else:
        print("    [SKIP] Waiting for Stage 2 output.")
        dp_schedule = None

    # ------------------------------------------------------------------ #
    # 4. Stage 4 — Backtracking                                            #
    # ------------------------------------------------------------------ #
    print("\n[4] Stage 4: Backtracking — Best-Effort Gap Filling")
    if dp_schedule is not None and conflict_graph is not None:
        unresolved = dp_schedule.unscheduled_count()
        if unresolved == 0:
            print("    All classes scheduled — backtracker not needed.")
            final_schedule = dp_schedule
        else:
            try:
                t0 = time.perf_counter()
                final_schedule = backtrack_solve(problem, dp_schedule, conflict_graph)
                elapsed = time.perf_counter() - t0
                print(f"    Completed in {elapsed*1000:.2f} ms")
                print()
                dp_waste    = dp_schedule.total_wasted()
                greedy_waste = greedy_schedule.total_wasted() if greedy_schedule else 647
                print(bt_report(
                    problem, final_schedule,
                    dp_scheduled  = dp_schedule.scheduled_count(),
                    dp_wasted     = dp_waste,
                    greedy_wasted = greedy_waste,
                ))
            except NotImplementedError:
                print("    [STUB] Stage 4 not yet implemented.")
                final_schedule = dp_schedule
    else:
        print("    [SKIP] Waiting for Stage 3 output.")
        final_schedule = dp_schedule

    # ------------------------------------------------------------------ #
    # 5. Conflict Report                                                   #
    # ------------------------------------------------------------------ #
    print("\n")
    if final_schedule is not None:
        print(final_schedule.conflict_report())
    else:
        print("[!] No schedule produced yet — implement the stages above.")

    return final_schedule


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="M603 University Timetabling System"
    )
    parser.add_argument(
        "--data",
        type=str,
        default=None,
        help="Path to constraints.json (default: data/constraints.json)",
    )
    args = parser.parse_args()
    run(args.data)