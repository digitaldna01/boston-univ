import matplotlib.pyplot as plt

# Data provided
utilization = [
    0.06684500783321592, 0.1336707527946651, 0.20048570923193568, 0.26729663684631666,
    0.3340799155264227, 0.4008578340504423, 0.46762053401045667, 0.5343719665055295,
    0.6011192561018542, 0.6678480524684188, 0.7345739929192759, 0.8012662868434848,
    0.860577767614917, 0.9166490772557693, 0.9703461137798655
]

avg_response_time = [
    0.07078575599985197, 0.0764845350026153, 0.08276943399012089, 0.09090426200721413,
    0.10010125800454989, 0.1126457069911994, 0.127716535998974, 0.1456022840021178,
    0.16748851699940862, 0.20181648099934682, 0.2714627019953914, 0.36817776600364593,
    0.49327193999662994, 0.659623870998621, 0.9743090979997069
]

avg_queue_length = [
    0.004138866104563857, 0.01786893369054184, 0.04401226123589471, 0.08856029569955444,
    0.158459348033703, 0.2577821254462251, 0.399413221992935, 0.5982416591392073,
    0.8801787157456495, 1.3215881667020168, 2.246100681046178, 3.583297451496042,
    5.4848436182135565, 8.127723952749369, 13.236610455510519
]

# Create a figure and axis object
fig, ax1 = plt.subplots(figsize=(10, 6))

# Plot average queue length on the left y-axis
ax1.set_xlabel('Server Utilization (%)')
ax1.set_ylabel('Average Queue Length', color='red')
ax1.plot(utilization, avg_queue_length, label='Average Queue Length', color='red', marker='x')
ax1.tick_params(axis='y', labelcolor='red')

# Create a second y-axis
ax2 = ax1.twinx()
ax2.set_ylabel('Average Response Time (sec)', color='blue')
ax2.plot(utilization, avg_response_time, label='Average Response Time (sec)', color='blue', marker='o')
ax2.tick_params(axis='y', labelcolor='blue')

# Adding title and grid
plt.title('Trend of Average Response Time and Average Queue Length vs Server Utilization')
plt.grid(True)

# Display the plot
plt.show()

