#!/usr/bin/env python3

import sys
import subprocess
import time
import re
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Check if the timeout argument is provided
if len(sys.argv) < 2:
    print("Usage: {} TIMEOUT".format(sys.argv[0]))
    sys.exit(1)

# Set the timeout duration from the command line argument
timeout = int(sys.argv[1])

# Run the ping command with a timeout and capture the output
ping_process = subprocess.Popen(["ping", "8.8.8.8"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
ping_times = []

try:
    start_time = time.time()
    while time.time() - start_time < timeout:
        line = ping_process.stdout.readline().decode()
        match = re.search(r'time=(\d+\.?\d*)', line)
        if match:
            timestamp = datetime.now()
            ping_time = float(match.group(1))
            ping_times.append((timestamp, ping_time))
finally:
    ping_process.terminate()

# Save the ping data to a file
with open("ping_data.dat", "w") as f:
    for timestamp, ping_time in ping_times:
        f.write("{} {:.2f}\n".format(timestamp.strftime("%Y-%m-%d %H:%M:%S"), ping_time))

# Generate the plot using matplotlib and save it as a PNG image
timestamps, pings = zip(*ping_times)
fig, ax = plt.subplots()
ax.plot(timestamps, pings, linestyle='-', marker='o', markersize=3)

ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
plt.xticks(rotation=45)
plt.xlabel("Time")
plt.ylabel("Ping Time (ms)")
plt.grid()
plt.tight_layout()

plt.savefig("ping_plot.png")

# Open the plot image using the default viewer on macOS
subprocess.run(["open", "ping_plot.png"])

