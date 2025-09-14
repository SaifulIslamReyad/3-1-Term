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
visited = [False] * n


while completed < n:
    idx = -1
    min_bt = float("inf")
    for i in range(n):
        if processes[i][1] <= time and not visited[i]:
            if processes[i][2] < min_bt:
                min_bt = processes[i][2]
                idx = i

    if idx == -1:
        time += 1
    else:
        time += processes[idx][2]
        ct[idx] = time
        tat[idx] = ct[idx] - processes[idx][1]
        wt[idx] = tat[idx] - processes[idx][2]
        visited[idx] = True
        completed += 1

avg_tat = sum(tat) / n
avg_wt = sum(wt) / n
throughput = n / (max(ct) - min(p[1] for p in processes))

print("\nSJF Non-Preemptive Results:")
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
visited = [False] * n
ct_gantt = [0] * n

while completed < n:
    idx = -1
    min_bt = float("inf")
    for i in range(n):
        if processes[i][1] <= time and not visited[i]:
            if processes[i][2] < min_bt:
                min_bt = processes[i][2]
                idx = i

    if idx == -1:
        time += 1
    else:
        start_time = time
        time += processes[idx][2]
        gantt_data.append((processes[idx][0], start_time, processes[idx][2]))
        ct_gantt[idx] = time
        visited[idx] = True
        completed += 1


# All processes on the same y-level with borders
fig, gnt = plt.subplots()
gnt.set_title("SJF Non-Preemptive Gantt Chart")
gnt.set_xlabel("Time")
gnt.set_yticks([5])
gnt.set_yticklabels(["Processes"])
gnt.set_ylim(0, 10)

for pid, start, dur in gantt_data:
    gnt.broken_barh(
        [(start, dur)],
        (3, 4),  # y=3, height=4
        facecolors=("tab:green"),
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
