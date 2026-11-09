
import streamlit as st
import pandas as pd

from scheduling import fcfs, sjf, priority_scheduling, round_robin
from metrics import calculate_metrics
from visualizer import plot_gantt


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="OS Playground",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
.stApp {
    background-color: #0f172a;
    color: #f8fafc;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #f8fafc;
}

.subtitle {
    color: #94a3b8;
    font-size: 17px;
}

.hero {
    background: linear-gradient(120deg, #1e3a8a, #312e81);
    padding: 35px;
    border-radius: 18px;
    margin-bottom: 25px;
}

.hero h1 {
    color: white;
    font-size: 36px;
}

.hero p {
    color: #dbeafe;
    font-size: 17px;
}

.feature-card {
    background-color: #1e293b;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #334155;
    min-height: 145px;
}

.feature-card h3 {
    color: #60a5fa;
}

.feature-card p {
    color: #cbd5e1;
}

.metric-card {
    background-color: #1e293b;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #334155;
    text-align: center;
}

.metric-value {
    font-size: 27px;
    font-weight: bold;
    color: #60a5fa;
}

.metric-label {
    color: #cbd5e1;
    font-size: 14px;
}

div.stButton > button {
    background-color: #2563eb;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 10px 22px;
    font-weight: 600;
}

div.stButton > button:hover {
    background-color: #1d4ed8;
    color: white;
}

h1, h2, h3 {
    color: #f8fafc;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

st.sidebar.title("💻 OS Playground")
st.sidebar.caption("Interactive Operating System Simulator")

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Home",
        "CPU Scheduling",
        "Algorithm Comparison",
        "Starvation & Aging",
        "Deadlock Simulator"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("Operating Systems Project | 2026")


# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

if page == "Home":

    st.markdown("""
    <div class="hero">
        <h1>Welcome to OS Playground 🚀</h1>
        <p>
        Explore Operating System concepts through interactive
        simulations, visualizations and real-time experiments.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Explore Operating Systems")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>⚙️ CPU Scheduling</h3>
            <p>
            Simulate FCFS, SJF, Priority and Round Robin
            scheduling algorithms with Gantt charts.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Algorithm Comparison</h3>
            <p>
            Compare scheduling algorithms using
            waiting time, turnaround time and response time.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>⏳ Starvation & Aging</h3>
            <p>
            Understand process starvation and how aging
            helps prevent indefinite waiting.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="feature-card">
            <h3>🔒 Deadlock Simulator</h3>
            <p>
            Explore deadlock conditions and understand
            how operating systems handle deadlocks.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    st.info("Select a module from the sidebar to get started.")


# --------------------------------------------------
# CPU SCHEDULING PAGE
# --------------------------------------------------

elif page == "CPU Scheduling":

    st.markdown('<p class="main-title">CPU Scheduling Simulator</p>',
                unsafe_allow_html=True)

    st.markdown(
        '<p class="subtitle">Add processes, select an algorithm and visualize CPU execution.</p>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.subheader("1. Enter Process Details")

    default_data = pd.DataFrame({
        "PID": ["P1", "P2", "P3", "P4"],
        "Arrival Time": [0, 2, 4, 5],
        "Burst Time": [7, 4, 1, 4],
        "Priority": [2, 1, 3, 2]
    })

    edited_data = st.data_editor(
        default_data,
        num_rows="dynamic",
        use_container_width=True,
        key="process_editor",
        column_config={
            "PID": st.column_config.TextColumn(
                "Process ID",
                required=True
            ),
            "Arrival Time": st.column_config.NumberColumn(
                "Arrival Time",
                min_value=0,
                step=1,
                required=True
            ),
            "Burst Time": st.column_config.NumberColumn(
                "Burst Time",
                min_value=1,
                step=1,
                required=True
            ),
            "Priority": st.column_config.NumberColumn(
                "Priority",
                min_value=1,
                step=1,
                required=True
            )
        }
    )

    st.markdown("---")

    st.subheader("2. Select Scheduling Algorithm")

    col1, col2 = st.columns(2)

    with col1:
        algorithm = st.selectbox(
            "Choose Algorithm",
            [
                "FCFS",
                "SJF (Non-Preemptive)",
                "Priority (Non-Preemptive)",
                "Round Robin"
            ]
        )

    with col2:
        quantum = st.number_input(
            "Time Quantum (Round Robin only)",
            min_value=1,
            value=2,
            step=1,
            disabled=(algorithm != "Round Robin")
        )

    st.markdown("---")

    # --------------------------------------------------
    # RUN SIMULATION
    # --------------------------------------------------

    if st.button("▶ Run Simulation", use_container_width=True):

        try:
            # Validate process table
            if edited_data.empty:
                st.error("Please enter at least one process.")

            elif edited_data.isnull().any().any():
                st.error("Please fill in all process details.")

            elif edited_data["PID"].astype(str).str.strip().eq("").any():
                st.error("Process IDs cannot be empty.")

            elif edited_data["PID"].astype(str).duplicated().any():
                st.error("Every process must have a unique Process ID.")

            elif (edited_data["Arrival Time"] < 0).any():
                st.error("Arrival time cannot be negative.")

            elif (edited_data["Burst Time"] <= 0).any():
                st.error("Burst time must be greater than zero.")

            elif (edited_data["Priority"] < 1).any():
                st.error("Priority must be at least 1.")

            else:
                # IMPORTANT:
                # Convert table column names into the format
                # expected by scheduling.py.
                processes = [
                    {
                        "pid": str(row["PID"]).strip(),
                        "arrival": int(row["Arrival Time"]),
                        "burst": int(row["Burst Time"]),
                        "priority": int(row["Priority"])
                    }
                    for _, row in edited_data.iterrows()
                ]

                # Run selected algorithm
                if algorithm == "FCFS":
                    intervals = fcfs(processes)

                elif algorithm == "SJF (Non-Preemptive)":
                    intervals = sjf(processes)

                elif algorithm == "Priority (Non-Preemptive)":
                    intervals = priority_scheduling(processes)

                else:
                    intervals = round_robin(processes, int(quantum))

                # Calculate performance metrics
                results, averages = calculate_metrics(
                    processes,
                    intervals
                )

                # Save simulation results
                st.session_state["simulation"] = {
                    "algorithm": algorithm,
                    "processes": processes,
                    "intervals": intervals,
                    "results": results,
                    "averages": averages
                }

                st.success("Simulation completed successfully!")

        except Exception as e:
            st.error(f"Something went wrong: {e}")

    # --------------------------------------------------
    # DISPLAY SIMULATION RESULTS
    # --------------------------------------------------

    if "simulation" in st.session_state:

        simulation = st.session_state["simulation"]

        st.markdown("---")
        st.subheader("3. Simulation Results")

        st.write(f"**Selected Algorithm:** {simulation['algorithm']}")

        st.markdown("### CPU Gantt Chart")

        fig = plot_gantt(simulation["intervals"])
        st.pyplot(fig)
        
        import matplotlib.pyplot as plt
        plt.close(fig)

        st.markdown("### Execution Sequence")

        sequence = "  →  ".join(
            f"{pid} ({start}-{end})"
            for pid, start, end in simulation["intervals"]
        )

        st.code(sequence)

        st.markdown("### Process Performance Table")

        results_df = pd.DataFrame(simulation["results"])
        st.dataframe(
            results_df,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("### Average Performance Metrics")

        averages = simulation["averages"]

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{averages['Average Turnaround Time']:.2f}</div>
                <div class="metric-label">Average Turnaround Time</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{averages['Average Waiting Time']:.2f}</div>
                <div class="metric-label">Average Waiting Time</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{averages['Average Response Time']:.2f}</div>
                <div class="metric-label">Average Response Time</div>
            </div>
            """, unsafe_allow_html=True)



# --------------------------------------------------
# ALGORITHM COMPARISON PAGE
# --------------------------------------------------

elif page == "Algorithm Comparison":

    st.markdown(
        '<p class="main-title">Algorithm Comparison</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">Compare all four CPU scheduling algorithms using the same processes.</p>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    if "simulation" not in st.session_state:

        st.warning(
            "Please run at least one simulation in CPU Scheduling first."
        )

    else:

        processes = st.session_state["simulation"]["processes"]

        st.subheader("1. Comparison Settings")

        quantum = st.number_input(
            "Round Robin Time Quantum",
            min_value=1,
            value=2,
            step=1,
            key="comparison_quantum"
        )

        st.write(f"Comparing **{len(processes)} processes**.")

        if st.button("Compare All Algorithms", use_container_width=True):

            algorithms = {
                "FCFS": fcfs,
                "SJF": sjf,
                "Priority": priority_scheduling
            }

            comparison_results = {}
            comparison_metrics = []

            # Run FCFS, SJF and Priority
            for name, algorithm_function in algorithms.items():

                intervals = algorithm_function(processes)

                results, averages = calculate_metrics(
                    processes,
                    intervals
                )

                comparison_results[name] = {
                    "intervals": intervals,
                    "results": results,
                    "averages": averages
                }

                comparison_metrics.append({
                    "Algorithm": name,
                    **averages
                })

            # Run Round Robin separately
            rr_intervals = round_robin(processes, int(quantum))

            rr_results, rr_averages = calculate_metrics(
                processes,
                rr_intervals
            )

            comparison_results["Round Robin"] = {
                "intervals": rr_intervals,
                "results": rr_results,
                "averages": rr_averages
            }

            comparison_metrics.append({
                "Algorithm": "Round Robin",
                **rr_averages
            })

            st.session_state["comparison_results"] = comparison_results
            st.session_state["comparison_metrics"] = pd.DataFrame(
                comparison_metrics
            )

            st.success("All four algorithms compared successfully!")

        # DISPLAY RESULTS
        if "comparison_results" in st.session_state:

            st.markdown("---")
            st.subheader("2. Performance Comparison")

            comparison_df = st.session_state["comparison_metrics"]

            st.dataframe(
                comparison_df.round(2),
                use_container_width=True,
                hide_index=True
            )

            st.markdown("### 3. Performance Graph")

            chart_df = comparison_df.set_index("Algorithm")

            st.bar_chart(
                chart_df[
                    [
                        "Average Waiting Time",
                        "Average Turnaround Time",
                        "Average Response Time"
                    ]
                ]
            )

            st.caption(
                "Lower values indicate better performance for all three metrics."
            )

            st.markdown("---")
            st.subheader("4. Best Performing Algorithms")

            col1, col2, col3 = st.columns(3)

            best_waiting = comparison_df.loc[
                comparison_df["Average Waiting Time"].idxmin()
            ]

            best_turnaround = comparison_df.loc[
                comparison_df["Average Turnaround Time"].idxmin()
            ]

            best_response = comparison_df.loc[
                comparison_df["Average Response Time"].idxmin()
            ]

            with col1:
                st.metric(
                    "Lowest Waiting Time",
                    best_waiting["Algorithm"],
                    f'{best_waiting["Average Waiting Time"]:.2f}'
                )

            with col2:
                st.metric(
                    "Lowest Turnaround Time",
                    best_turnaround["Algorithm"],
                    f'{best_turnaround["Average Turnaround Time"]:.2f}'
                )

            with col3:
                st.metric(
                    "Lowest Response Time",
                    best_response["Algorithm"],
                    f'{best_response["Average Response Time"]:.2f}'
                )

            st.markdown("---")
            st.subheader("5. Individual Gantt Charts")

            comparison_results = st.session_state["comparison_results"]

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("**FCFS**")
                fig = plot_gantt(comparison_results["FCFS"]["intervals"])
                st.pyplot(fig)
                import matplotlib.pyplot as plt
                plt.close(fig)

                st.markdown("**SJF**")
                fig = plot_gantt(comparison_results["SJF"]["intervals"])
                st.pyplot(fig)
                plt.close(fig)

            with col2:
                st.markdown("**Priority Scheduling**")
                fig = plot_gantt(comparison_results["Priority"]["intervals"])
                st.pyplot(fig)
                plt.close(fig)

                st.markdown("**Round Robin**")
                fig = plot_gantt(comparison_results["Round Robin"]["intervals"])
                st.pyplot(fig)
                plt.close(fig)




# --------------------------------------------------
# STARVATION AND AGING PAGE
# --------------------------------------------------

elif page == "Starvation & Aging":

    st.markdown(
        '<p class="main-title">Starvation & Aging</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">Understand process starvation and how aging prevents it.</p>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.subheader("1. Understanding Starvation")

    st.write(
        "Starvation occurs when a process waits for an indefinitely long "
        "time because other processes with higher priority continuously "
        "get CPU time."
    )

    st.subheader("2. Understanding Aging")

    st.write(
        "Aging is a technique used to prevent starvation. "
        "As a process waits in the ready queue, its priority gradually "
        "increases."
    )

    st.info(
        "In this simulator, a smaller priority number means higher priority. "
        "Aging gradually reduces the numerical priority of waiting processes."
    )

    st.markdown("---")

    st.subheader("3. Interactive Starvation Simulator")

    st.write(
        "We will simulate one low-priority process competing with "
        "multiple high-priority processes."
    )

    aging_interval = st.slider(
        "Aging interval (time units)",
        min_value=1,
        max_value=10,
        value=2,
        help="After this many waiting time units, a process gains one priority level."
    )

    st.caption(
        "The low-priority process starts with priority 8. "
        "Other processes start with priority 1."
    )

    def simulate_starvation(aging_enabled, interval):

        jobs = [
            {
                "pid": "P1",
                "arrival": 0,
                "burst": 4,
                "priority": 8
            }
        ]

        # Add high-priority processes arriving over time
        for i in range(2, 14):
            jobs.append({
                "pid": f"P{i}",
                "arrival": i - 2,
                "burst": 2,
                "priority": 1
            })

        remaining = {
            p["pid"]: p["burst"] for p in jobs
        }

        waiting = {
            p["pid"]: 0 for p in jobs
        }

        current_time = 0
        intervals = []
        first_start = {}
        completion = {}

        while any(value > 0 for value in remaining.values()):

            ready = [
                p for p in jobs
                if p["arrival"] <= current_time
                and remaining[p["pid"]] > 0
            ]

            if not ready:
                current_time += 1
                continue

            def effective_priority(p):

                priority = p["priority"]

                if aging_enabled:
                    improvement = waiting[p["pid"]] // interval
                    priority = max(1, priority - improvement)

                return priority

            selected = min(
                ready,
                key=lambda p: (
                    effective_priority(p),
                    p["arrival"],
                    p["pid"]
                )
            )

            pid = selected["pid"]

            if pid not in first_start:
                first_start[pid] = current_time

            # Execute the selected process for one time unit
            if intervals and intervals[-1][0] == pid:
                intervals[-1] = (
                    pid,
                    intervals[-1][1],
                    current_time + 1
                )
            else:
                intervals.append(
                    (pid, current_time, current_time + 1)
                )

            # All other ready processes wait
            for p in ready:
                if p["pid"] != pid:
                    waiting[p["pid"]] += 1

            remaining[pid] -= 1
            current_time += 1

            if remaining[pid] == 0:
                completion[pid] = current_time

        return intervals, first_start, completion, waiting

    if st.button(
        "▶ Run Starvation vs Aging Simulation",
        use_container_width=True
    ):

        without_aging = simulate_starvation(
            False,
            aging_interval
        )

        with_aging = simulate_starvation(
            True,
            aging_interval
        )

        st.session_state["starvation_results"] = {
            "without": without_aging,
            "with": with_aging
        }

        st.success("Starvation and Aging simulation completed!")

    # --------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------

    if "starvation_results" in st.session_state:

        data = st.session_state["starvation_results"]

        without = data["without"]
        with_aging = data["with"]

        without_start = without[1]["P1"]
        with_start = with_aging[1]["P1"]

        st.markdown("---")
        st.subheader("4. Simulation Results")

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### Without Aging")

            st.metric(
                "P1 starts executing at",
                f"{without_start} time units"
            )

            st.warning(
                "P1 has low priority and keeps waiting "
                "while higher-priority processes execute."
            )

            st.write("Execution sequence:")

            st.code(
                " → ".join(
                    f"{pid} ({start}-{end})"
                    for pid, start, end in without[0]
                )
            )

        with col2:

            st.markdown("### With Aging")

            st.metric(
                "P1 starts executing at",
                f"{with_start} time units",
                delta=f"{without_start - with_start} time units earlier",
                delta_color="normal"
            )

            st.success(
                "P1 gradually gains priority and gets CPU time earlier."
            )

            st.write("Execution sequence:")

            st.code(
                " → ".join(
                    f"{pid} ({start}-{end})"
                    for pid, start, end in with_aging[0]
                )
            )

        st.markdown("---")
        st.subheader("5. Process P1 Comparison")

        comparison = pd.DataFrame([
            {
                "Scenario": "Without Aging",
                "First CPU Start": without_start,
                "Completion Time": without[2]["P1"],
                "Total Waiting Time": without[3]["P1"]
            },
            {
                "Scenario": "With Aging",
                "First CPU Start": with_start,
                "Completion Time": with_aging[2]["P1"],
                "Total Waiting Time": with_aging[3]["P1"]
            }
        ])

        st.dataframe(
            comparison,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")

        st.subheader("6. What Did We Learn?")

        st.write(
            f"Without aging, P1 starts at time {without_start}. "
            f"With aging, it starts at time {with_start}."
        )

        st.success(
            "Conclusion: Aging helps prevent starvation by "
            "gradually increasing the priority of waiting processes."
        )




# --------------------------------------------------
# DEADLOCK SIMULATOR PAGE
# --------------------------------------------------

elif page == "Deadlock Simulator":

    st.markdown(
        '<p class="main-title">Deadlock Simulator</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">Explore resource allocation and detect unsafe system states using Bankers Algorithm.</p>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.subheader("1. Understanding Deadlock")

    st.write(
        "A deadlock occurs when processes wait indefinitely for resources "
        "held by one another, so none of them can proceed."
    )

    st.markdown("### Four Necessary Conditions")

    conditions = [
        ("Mutual Exclusion", "A resource can be used by only one process at a time."),
        ("Hold and Wait", "A process holds resources while waiting for additional resources."),
        ("No Preemption", "Resources cannot be forcibly taken from a process."),
        ("Circular Wait", "Processes form a circular chain, each waiting for a resource held by the next.")
    ]

    for title, description in conditions:
        st.markdown(f"**{title}:** {description}")

    st.markdown("---")

    st.subheader("2. Banker's Algorithm")

    st.write(
        "Banker's Algorithm checks whether granting resources can leave "
        "the system in a safe state."
    )

    st.info(
        "A safe state means there is at least one order in which all "
        "processes can finish without getting stuck."
    )

    st.markdown("### Sample Resource Allocation")

    st.write(
        "We will use 5 processes and 3 resource types: A, B and C. "
        "You can edit the values to experiment."
    )

    allocation_default = pd.DataFrame({
        "Process": ["P0", "P1", "P2", "P3", "P4"],
        "A": [0, 2, 3, 2, 0],
        "B": [1, 0, 0, 1, 0],
        "C": [0, 0, 2, 1, 2]
    })

    maximum_default = pd.DataFrame({
        "Process": ["P0", "P1", "P2", "P3", "P4"],
        "A": [7, 3, 9, 2, 4],
        "B": [5, 2, 0, 2, 3],
        "C": [3, 2, 2, 2, 3]
    })

    st.markdown("#### Allocation Matrix")

    allocation_df = st.data_editor(
        allocation_default,
        use_container_width=True,
        hide_index=True,
        key="deadlock_allocation",
        disabled=["Process"],
        column_config={
            "A": st.column_config.NumberColumn("A", min_value=0, step=1),
            "B": st.column_config.NumberColumn("B", min_value=0, step=1),
            "C": st.column_config.NumberColumn("C", min_value=0, step=1)
        }
    )

    st.caption(
        "Allocation = Number of resources currently held by each process."
    )

    st.markdown("#### Maximum Resource Requirement")

    maximum_df = st.data_editor(
        maximum_default,
        use_container_width=True,
        hide_index=True,
        key="deadlock_maximum",
        disabled=["Process"],
        column_config={
            "A": st.column_config.NumberColumn("A", min_value=0, step=1),
            "B": st.column_config.NumberColumn("B", min_value=0, step=1),
            "C": st.column_config.NumberColumn("C", min_value=0, step=1)
        }
    )

    st.caption(
        "Maximum = Maximum number of resources each process may need."
    )

    st.markdown("#### Available Resources")

    col1, col2, col3 = st.columns(3)

    with col1:
        available_a = st.number_input(
            "Available A",
            min_value=0,
            value=3,
            step=1,
            key="available_a"
        )

    with col2:
        available_b = st.number_input(
            "Available B",
            min_value=0,
            value=3,
            step=1,
            key="available_b"
        )

    with col3:
        available_c = st.number_input(
            "Available C",
            min_value=0,
            value=2,
            step=1,
            key="available_c"
        )

    st.caption(
        "Available = Resources currently free and ready to be allocated."
    )

    st.markdown("---")

    # --------------------------------------------------
    # BANKER'S ALGORITHM
    # --------------------------------------------------

    if st.button(
        "▶ Check System Safety",
        use_container_width=True
    ):

        try:
            resource_columns = ["A", "B", "C"]

            # Convert tables to numeric matrices
            allocation = allocation_df[resource_columns].to_numpy(dtype=int)
            maximum = maximum_df[resource_columns].to_numpy(dtype=int)

            available = [
                int(available_a),
                int(available_b),
                int(available_c)
            ]

            process_names = allocation_df["Process"].tolist()

            # Validate dimensions
            if len(allocation) != len(maximum):
                st.error("Allocation and Maximum matrices must have the same number of processes.")

            elif (allocation < 0).any() or (maximum < 0).any():
                st.error("Resource values cannot be negative.")

            elif (maximum < allocation).any():
                st.error("Maximum requirement cannot be smaller than current allocation.")

            else:

                # NEED = MAXIMUM - ALLOCATION
                need = maximum - allocation

                st.session_state["deadlock_need"] = pd.DataFrame(
                    need,
                    columns=resource_columns,
                    index=process_names
                )

                # Initialize Work and Finish
                work = available.copy()

                finish = [False] * len(process_names)

                safe_sequence = []

                # Find a safe execution sequence
                while len(safe_sequence) < len(process_names):

                    found = False

                    for i in range(len(process_names)):

                        if not finish[i]:

                            can_execute = all(
                                need[i][j] <= work[j]
                                for j in range(3)
                            )

                            if can_execute:

                                # Process finishes and releases its resources
                                for j in range(3):
                                    work[j] += allocation[i][j]

                                finish[i] = True
                                safe_sequence.append(process_names[i])
                                found = True
                                break

                    if not found:
                        break

                is_safe = all(finish)

                st.session_state["deadlock_result"] = {
                    "is_safe": is_safe,
                    "safe_sequence": safe_sequence,
                    "work": work,
                    "process_names": process_names
                }

        except Exception as e:
            st.error(f"Unable to run safety check: {e}")

    # --------------------------------------------------
    # DISPLAY RESULTS
    # --------------------------------------------------

    if "deadlock_result" in st.session_state:

        result = st.session_state["deadlock_result"]

        st.markdown("---")
        st.subheader("3. Resource Need Matrix")

        st.write(
            "Need = Maximum Requirement − Current Allocation"
        )

        st.dataframe(
            st.session_state["deadlock_need"],
            use_container_width=True
        )

        st.markdown("---")
        st.subheader("4. Safety Check Result")

        if result["is_safe"]:

            st.success("SAFE STATE: The system has a safe execution sequence.")

            st.markdown("### Safe Sequence")

            sequence = "  →  ".join(result["safe_sequence"])

            st.code(sequence)

            st.write(
                "Each process can complete in this order and release "
                "its allocated resources for the next process."
            )

        else:

            st.error(
                "UNSAFE STATE: No safe execution sequence was found."
            )

            st.warning(
                "The current resource allocation cannot guarantee that "
                "all processes will finish. An unsafe state does not "
                "necessarily mean that a deadlock has already occurred."
            )

            if result["safe_sequence"]:
                st.write(
                    "Processes that could finish before the system "
                    "became stuck:"
                )

                st.code(" → ".join(result["safe_sequence"]))

        st.markdown("---")
        st.subheader("5. Final Available Resources")

        final_resources = pd.DataFrame({
            "Resource": ["A", "B", "C"],
            "Available after execution": result["work"]
        })

        st.dataframe(
            final_resources,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")

        st.subheader("6. What Did We Learn?")

        st.write(
            "Banker's Algorithm checks the remaining resource needs "
            "of processes before determining whether a safe execution "
            "order exists."
        )

        st.info(
            "Operating systems can use resource-allocation strategies "
            "to avoid entering unsafe states."
        )

