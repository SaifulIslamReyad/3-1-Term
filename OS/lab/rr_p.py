import matplotlib.pyplot as plt

n = int(input("Enter number of processes: "))
q = int(input("Enter Time Quantum: "))
processes = []
for i in range(n):
    pid = input(f"Enter Process ID for P{i+1}: ")
    at = int(input(f"Enter Arrival Time of {pid}: "))
    bt = int(input(f"Enter Burst Time of {pid}: "))
    processes.append([pid, at, bt])

processes.sort(key=lambda x: x[1])
remaining_bt = [p[2] for p in processes]
ct = [0] * n
tat = [0] * n
wt = [0] * n
start_times = [0] * n
time = 0
completed = 0
queue = []
gantt_order = []
visited = [False] * n

while completed < n:
    for i in range(n):
        if processes[i][1] <= time and not visited[i]:
            queue.append(i)
            visited[i] = True
    if not queue:
        time += 1
        continue
    idx = queue.pop(0)
    exec_time = min(q, remaining_bt[idx])
    gantt_order.append((processes[idx][0], time, exec_time))
    time += exec_time
    remaining_bt[idx] -= exec_time
    for i in range(n):
        if (
            processes[i][1] > time - exec_time
            and processes[i][1] <= time
            and not visited[i]
        ):
            queue.append(i)
            visited[i] = True
    if remaining_bt[idx] > 0:
        queue.append(idx)
    else:
        ct[idx] = time
        completed += 1

for i in range(n):
    tat[i] = ct[i] - processes[i][1]
    wt[i] = tat[i] - processes[i][2]

avg_tat = sum(tat) / n
avg_wt = sum(wt) / n
throughput = n / (max(ct) - min([p[1] for p in processes]))

print("\nRound Robin (Preemptive) Results:")
print("Process\tAT\tBT\tCT\tTAT\tWT")
for i in range(n):
    print(
        f"{processes[i][0]}\t{processes[i][1]}\t{processes[i][2]}\t{ct[i]}\t{tat[i]}\t{wt[i]}"
    )

print(f"\nAverage Turnaround Time = {avg_tat:.2f}")
print(f"Average Waiting Time = {avg_wt:.2f}")
print(f"Throughput = {throughput:.2f} processes/unit time")

# Gantt Chart
fig, gnt = plt.subplots()
gnt.set_title("Round Robin (Preemptive) Gantt Chart")
gnt.set_xlabel("Time")
gnt.set_yticks([1.5])
gnt.set_yticklabels(["Processes"])
gnt.set_ylim(0, 3)

for pid, start, dur in gantt_order:
    gnt.broken_barh(
        [(start, dur)],
        (1, 1),
        facecolors="tab:green",
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
