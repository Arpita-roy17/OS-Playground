
from collections import deque


# 1. FIRST COME FIRST SERVE (FCFS)

def fcfs(processes):

    process_list = sorted(
        processes,
        key=lambda p: (p["arrival"], p["pid"])
    )

    current_time = 0
    intervals = []

    for p in process_list:

        if current_time < p["arrival"]:
            intervals.append(
                ("IDLE", current_time, p["arrival"])
            )
            current_time = p["arrival"]

        start = current_time
        end = start + p["burst"]

        intervals.append((p["pid"], start, end))

        current_time = end

    return intervals


# 2. SHORTEST JOB FIRST (NON-PREEMPTIVE)

def sjf(processes):

    remaining = processes.copy()
    current_time = 0
    intervals = []

    while remaining:

        ready = [
            p for p in remaining
            if p["arrival"] <= current_time
        ]

        if not ready:

            next_time = min(
                p["arrival"] for p in remaining
            )

            intervals.append(
                ("IDLE", current_time, next_time)
            )

            current_time = next_time
            continue

        p = min(
            ready,
            key=lambda x: (
                x["burst"],
                x["arrival"],
                x["pid"]
            )
        )

        start = current_time
        end = start + p["burst"]

        intervals.append((p["pid"], start, end))

        current_time = end
        remaining.remove(p)

    return intervals


# 3. PRIORITY SCHEDULING (NON-PREEMPTIVE)

def priority_scheduling(processes):

    remaining = processes.copy()
    current_time = 0
    intervals = []

    while remaining:

        ready = [
            p for p in remaining
            if p["arrival"] <= current_time
        ]

        if not ready:

            next_time = min(
                p["arrival"] for p in remaining
            )

            intervals.append(
                ("IDLE", current_time, next_time)
            )

            current_time = next_time
            continue

        p = min(
            ready,
            key=lambda x: (
                x["priority"],
                x["arrival"],
                x["pid"]
            )
        )

        start = current_time
        end = start + p["burst"]

        intervals.append((p["pid"], start, end))

        current_time = end
        remaining.remove(p)

    return intervals


# 4. ROUND ROBIN

def round_robin(processes, quantum):

    if quantum <= 0:
        raise ValueError("Time quantum must be greater than zero.")

    process_list = sorted(
        processes,
        key=lambda p: (p["arrival"], p["pid"])
    )

    remaining = {
        p["pid"]: p["burst"]
        for p in process_list
    }

    ready_queue = deque()

    intervals = []
    current_time = 0
    i = 0

    while i < len(process_list) or ready_queue:

        if not ready_queue:

            if current_time < process_list[i]["arrival"]:

                intervals.append(
                    ("IDLE", current_time,
                     process_list[i]["arrival"])
                )

                current_time = process_list[i]["arrival"]

            while (
                i < len(process_list)
                and process_list[i]["arrival"] <= current_time
            ):
                ready_queue.append(process_list[i])
                i += 1

        p = ready_queue.popleft()

        run_time = min(
            quantum,
            remaining[p["pid"]]
        )

        start = current_time
        current_time += run_time

        intervals.append(
            (p["pid"], start, current_time)
        )

        remaining[p["pid"]] -= run_time

        while (
            i < len(process_list)
            and process_list[i]["arrival"] <= current_time
        ):
            ready_queue.append(process_list[i])
            i += 1

        if remaining[p["pid"]] > 0:
            ready_queue.append(p)

    return intervals
