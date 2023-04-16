set xdata time
set timefmt "%Y-%m-%d %H:%M:%S"
set term png
set output "ping_plot.png"
plot "ping_data.dat" using 1:3 with lines
quit

