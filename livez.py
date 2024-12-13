import matplotlib.pyplot as plt
import numpy as np

plt.ion()  # Turn on interactive mode

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))  # Create a figure with 2 subplots vertically stacked
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

line1, = ax1.plot(x, y1, label='Sin')  # Plot sin function on the first subplot
line2, = ax2.plot(x, y2, label='Cos')  # Plot cos function on the second subplot

ax1.set_title('Sin Function')
ax2.set_title('Cos Function')

for i in range(100):
    y = np.sin(x + i*0.1)
    y2 = np.cos(x + i*0.1)
    line1.set_ydata(y)
    line2.set_ydata(y2)
    ax1.relim()  # Update limits for the first subplot
    ax1.autoscale_view()  # Autoscale the view for the first subplot
    ax2.relim()  # Update limits for the second subplot
    ax2.autoscale_view()  # Autoscale the view for the second subplot
    plt.draw()
    plt.pause(0.1)

plt.ioff()  # Turn off interactive mode
plt.show()
