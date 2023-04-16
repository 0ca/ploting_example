#!/bin/bash

# Check if the timeout argument is provided
if [ $# -lt 1 ]; then
  echo "Usage: $0 TIMEOUT"
  exit 1
fi

# Set the timeout duration from the command line argument
TIMEOUT=$1

# Run the ping command with a timeout and log the output
timeout ${TIMEOUT}s ping 8.8.8.8 | awk '/time=/ {
  system("date +\"[%Y-%m-%d %H:%M:%S]\" | tr -d \"\\n\""); # Print the current date and time
  printf(" "); # Add a space separator
  print $0 # Print the ping output
}' > ping_results.log

# Extract the ping data from the log file and save it to a data file
awk -F '[\\[\\]]|time=' '/time=/{print $2, $4}' ping_results.log > ping_data.dat

# Generate the plot using gnuplot and save it as a PNG image
gnuplot << EOF
set xdata time
set timefmt "%Y-%m-%d %H:%M:%S"
set term png
set output "ping_plot.png"
plot "ping_data.dat" using 1:3 with lines
quit
EOF

# Open the plot image using the default viewer on macOS
open ping_plot.png

