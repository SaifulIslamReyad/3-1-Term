n = int(input("Enter number of processes: "))

processes = []
for i in range(n):
    pid = input(f"Enter Process ID for P{i+1}: ")
    at = int(input(f"Enter Arrival Time of {pid}: "))
    bt = int(input(f"Enter Burst Time of {pid}: "))
    processes.append([pid, at, bt])

processes.sort(key=lambda x: x[1])

time = 0
completed = 0
ct, tat, wt = [0] * n, [0] * n, [0] * n
remaining_bt = [p[2] for p in processes]

while completed < n:
    idx = -1
    min_bt = float("inf")

    for i in range(n):
        if processes[i][1] <= time and remaining_bt[i] > 0:
            if remaining_bt[i] < min_bt:
                min_bt = remaining_bt[i]
                idx = i

    if idx == -1:
        time += 1
    else:
        remaining_bt[idx] -= 1
        time += 1

        if remaining_bt[idx] == 0:
            ct[idx] = time
            tat[idx] = ct[idx] - processes[idx][1]
            wt[idx] = tat[idx] - processes[idx][2]
            completed += 1

avg_tat = sum(tat) / n
avg_wt = sum(wt) / n
throughput = n / (max(ct) - min(p[1] for p in processes))

print("\nSJF Preemptive (SRTF) Results:")
print("Process\tAT\tBT\tCT\tTAT\tWT")
for i in range(n):
    print(
        f"{processes[i][0]}\t{processes[i][1]}\t{processes[i][2]}\t{ct[i]}\t{tat[i]}\t{wt[i]}"
    )

print(f"\nAverage Turnaround Time = {avg_tat:.2f}")
print(f"Average Waiting Time = {avg_wt:.2f}")
print(f"Throughput = {throughput:.2f} processes/unit time")

import matplotlib.pyplot as plt

gantt_data = []
time = 0
completed = 0
remaining_bt = [p[2] for p in processes]
last_pid = None
start_time = 0
timeline = []

while completed < n:
    idx = -1
    min_bt = float("inf")
    for i in range(n):
        if processes[i][1] <= time and remaining_bt[i] > 0:
            if remaining_bt[i] < min_bt:
                min_bt = remaining_bt[i]
                idx = i

    if idx == -1:
        time += 1
        timeline.append(("IDLE", time))
    else:
        if last_pid != processes[idx][0]:
            if last_pid is not None:
                gantt_data.append((last_pid, start_time, time - start_time))
            start_time = time
            last_pid = processes[idx][0]
        remaining_bt[idx] -= 1
        time += 1
        timeline.append((processes[idx][0], time))
        if remaining_bt[idx] == 0:
            gantt_data.append((processes[idx][0], start_time, time - start_time))
            last_pid = None
            start_time = time
            completed += 1

if last_pid is not None and time > start_time:
    gantt_data.append((last_pid, start_time, time - start_time))


# All processes on the same y-level with borders
fig, gnt = plt.subplots()
gnt.set_title("SJF Preemptive (SRTF) Gantt Chart")
gnt.set_xlabel("Time")
gnt.set_yticks([5])
gnt.set_yticklabels(["Processes"])
gnt.set_ylim(0, 10)

for pid, start, dur in gantt_data:
    color = "tab:orange" if pid != "IDLE" else "tab:gray"
    gnt.broken_barh(
        [(start, dur)],
        (3, 4),  # y=3, height=4
        facecolors=(color),
        edgecolors=("black"),
        linewidth=2,
    )
    gnt.text(
        start + dur / 2,
        5,
        pid,
        ha="center",
        va="center",
        color="white",
        fontsize=9,
        fontweight="bold",
    )

plt.tight_layout()
plt.show()
