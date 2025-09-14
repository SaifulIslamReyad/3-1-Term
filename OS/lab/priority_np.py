import matplotlib.pyplot as plt

n = int(input("Enter number of processes: "))

processes = []
for i in range(n):
    pid = input(f"Enter Process ID for P{i+1}: ")
    at = int(input(f"Enter Arrival Time of {pid}: "))
    bt = int(input(f"Enter Burst Time of {pid}: "))
    pr = int(input(f"Enter Priority of {pid} (lower number = higher priority): "))
    processes.append([pid, at, bt, pr])

# Sort by arrival time first for tie-breaking
processes.sort(key=lambda x: (x[1], x[3]))

completed = [False] * n
ct, tat, wt = [0]*n, [0]*n, [0]*n
start_times = [0]*n
time = 0
completed_count = 0

gantt_order = []
while completed_count < n:
    # Find all arrived and not completed processes
    available = [(i, p) for i, p in enumerate(processes) if p[1] <= time and not completed[i]]
    if available:
        # Select process with highest priority (lowest pr), break ties by arrival time
        idx, proc = min(available, key=lambda x: (x[1][3], x[1][1]))
        start_times[idx] = time
        time += proc[2]
        ct[idx] = time
        completed[idx] = True
        completed_count += 1
        gantt_order.append((proc[0], start_times[idx], proc[2]))
    else:
        time += 1  # CPU idle

for i in range(n):
    tat[i] = ct[i] - processes[i][1]
    wt[i] = tat[i] - processes[i][2]

avg_tat = sum(tat) / n
avg_wt = sum(wt) / n
throughput = n / (max(ct) - min([p[1] for p in processes]))

print("\nPriority Scheduling (Non-Preemptive) Results:")
print("Process\tAT\tBT\tPR\tCT\tTAT\tWT")
for i in range(n):
    print(f"{processes[i][0]}\t{processes[i][1]}\t{processes[i][2]}\t{processes[i][3]}\t{ct[i]}\t{tat[i]}\t{wt[i]}")

print(f"\nAverage Turnaround Time = {avg_tat:.2f}")
print(f"Average Waiting Time = {avg_wt:.2f}")
print(f"Throughput = {throughput:.2f} processes/unit time")

# Gantt Chart
fig, gnt = plt.subplots()
gnt.set_title("Priority Scheduling (Non-Preemptive) Gantt Chart")
gnt.set_xlabel("Time")
gnt.set_yticks([1.5])
gnt.set_yticklabels(["Processes"])
gnt.set_ylim(0, 3)

for pid, start, dur in gantt_order:
    gnt.broken_barh(
        [(start, dur)],
        (1, 1),
        facecolors="tab:orange",
        edgecolors="black",
        linewidth=2,
    )
    gnt.text(
        start + dur / 2,
        1.5,
        "p" + pid,
        ha="center",
        va="center",
        color="white",
        fontsize=9,
        fontweight="bold",
    )

plt.tight_layout()
plt.show()
