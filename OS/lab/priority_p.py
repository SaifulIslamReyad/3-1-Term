import matplotlib.pyplot as plt

n = int(input("Enter number of processes: "))
processes = []
for i in range(n):
    pid = input(f"Enter Process ID for P{i+1}: ")
    at = int(input(f"Enter Arrival Time of {pid}: "))
    bt = int(input(f"Enter Burst Time of {pid}: "))
    pr = int(input(f"Enter Priority of {pid} (lower number = higher priority): "))
    processes.append([pid, at, bt, pr])

processes.sort(key=lambda x: (x[1], x[3]))
remaining_bt = [p[2] for p in processes]
ct = [0] * n
tat = [0] * n
wt = [0] * n
start_times = []
gantt_order = []
time = 0
completed = 0
last_pid = None
start_exec = 0

while completed < n:
    available = [
        (i, p) for i, p in enumerate(processes) if p[1] <= time and remaining_bt[i] > 0
    ]
    if available:
        idx, proc = min(available, key=lambda x: (x[1][3], x[1][1]))
        if last_pid != proc[0]:
            if last_pid is not None:
                gantt_order.append((last_pid, start_exec, time - start_exec))
            start_exec = time
            last_pid = proc[0]
        remaining_bt[idx] -= 1
        time += 1
        if remaining_bt[idx] == 0:
            ct[idx] = time
            completed += 1
    else:
        if last_pid is not None:
            gantt_order.append((last_pid, start_exec, time - start_exec))
            last_pid = None
        time += 1
        start_exec = time

if last_pid is not None:
    gantt_order.append((last_pid, start_exec, time - start_exec))

for i in range(n):
    tat[i] = ct[i] - processes[i][1]
    wt[i] = tat[i] - processes[i][2]

avg_tat = sum(tat) / n
avg_wt = sum(wt) / n
throughput = n / (max(ct) - min([p[1] for p in processes]))

print("\nPriority Scheduling (Preemptive) Results:")
print("Process\tAT\tBT\tPR\tCT\tTAT\tWT")
for i in range(n):
    print(
        f"{processes[i][0]}\t{processes[i][1]}\t{processes[i][2]}\t{processes[i][3]}\t{ct[i]}\t{tat[i]}\t{wt[i]}"
    )

print(f"\nAverage Turnaround Time = {avg_tat:.2f}")
print(f"Average Waiting Time = {avg_wt:.2f}")
print(f"Throughput = {throughput:.2f} processes/unit time")

# Gantt Chart
fig, gnt = plt.subplots()
gnt.set_title("Priority Scheduling (Preemptive) Gantt Chart")
gnt.set_xlabel("Time")
gnt.set_yticks([1.5])
gnt.set_yticklabels(["Processes"])
gnt.set_ylim(0, 3)

for pid, start, dur in gantt_order:
    gnt.broken_barh(
        [(start, dur)],
        (1, 1),
        facecolors="tab:red",
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
