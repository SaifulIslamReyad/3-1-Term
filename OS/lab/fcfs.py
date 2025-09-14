n = int(input("Enter number of processes: "))

processes = []
for i in range(n):
    pid = input(f"Enter Process ID for P{i+1}: ")
    at = int(input(f"Enter Arrival Time of {pid}: "))
    bt = int(input(f"Enter Burst Time of {pid}: "))
    processes.append([pid, at, bt])

processes.sort(key=lambda x: x[1])

ct, tat, wt = [], [], []

for i in range(n):
    if i == 0:
        ct.append(processes[i][1] + processes[i][2])  # AT + BT
    else:
        if processes[i][1] > ct[i - 1]:
            ct.append(processes[i][1] + processes[i][2])
        else:
            ct.append(ct[i - 1] + processes[i][2])

for i in range(n):
    tat.append(ct[i] - processes[i][1])  # TAT = CT - AT
    wt.append(tat[i] - processes[i][2])  # WT = TAT - BT

avg_tat = sum(tat) / n
avg_wt = sum(wt) / n
throughput = n / (ct[-1] - processes[0][1])

print("\nFCFS Scheduling Results:")
print("Process\tAT\tBT\tCT\tTAT\tWT")
for i in range(n):
    print(
        f"{processes[i][0]}\t{processes[i][1]}\t{processes[i][2]}\t{ct[i]}\t{tat[i]}\t{wt[i]}"
    )

print(f"\nAverage Turnaround Time = {avg_tat:.2f}")
print(f"Average Waiting Time = {avg_wt:.2f}")
print(f"Throughput = {throughput:.2f} processes/unit time")





import matplotlib.pyplot as plt


start_times = []
current_time = processes[0][1]
for i in range(n):
    if i == 0:
        start = processes[i][1]
    else:
        start = max(ct[i - 1], processes[i][1])
    start_times.append(start)


fig, gnt = plt.subplots()
gnt.set_title("FCFS Gantt Chart")
gnt.set_xlabel("Time")
gnt.set_yticks([5])
gnt.set_yticklabels(["Processes"])
gnt.set_ylim(0, 10)


for i in range(n):
    gnt.broken_barh(
        [(start_times[i], processes[i][2])],
        (0.5, 2),  # y=3, height=4
        facecolors=("tab:blue"),
        edgecolors=("black"),
        linewidth=2,
    )
    gnt.text(
        start_times[i] + processes[i][2] / 2,
        1.5,
        "p"+processes[i][0],
        ha="center",
        va="center",
        color="white",
        fontsize=9,
        fontweight="bold",
    )

plt.tight_layout()
plt.show()

