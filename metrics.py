
def calculate_metrics(processes, intervals):

    results = []

    total_tat = 0
    total_wt = 0
    total_rt = 0

    for p in processes:

        pid = p["pid"]

        # Find all CPU execution intervals of this process
        runs = [
            interval
            for interval in intervals
            if interval[0] == pid
        ]

        if not runs:
            continue

        # First time the process gets CPU
        first_start = runs[0][1]

        # Last time the process finishes execution
        completion_time = runs[-1][2]

        # Calculate scheduling metrics
        turnaround_time = completion_time - p["arrival"]

        waiting_time = turnaround_time - p["burst"]

        response_time = first_start - p["arrival"]

        # Store results
        results.append({
            "PID": pid,
            "Arrival Time": p["arrival"],
            "Burst Time": p["burst"],
            "Completion Time": completion_time,
            "Turnaround Time": turnaround_time,
            "Waiting Time": waiting_time,
            "Response Time": response_time
        })

        # Calculate totals
        total_tat += turnaround_time
        total_wt += waiting_time
        total_rt += response_time

    # Calculate averages
    count = len(results)

    if count == 0:
        return results, {}

    averages = {
        "Average Turnaround Time": total_tat / count,
        "Average Waiting Time": total_wt / count,
        "Average Response Time": total_rt / count
    }

    return results, averages
