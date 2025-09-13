import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Initial data
x = [0, 1, 2, 3, 4, 5]
y = [0, 1, 0, 1, 0, 1]

figure, axes = plt.subplots()
lines, = axes.plot(x, y, 'ro-')  # plot with red dots connected by lines

def update(frame):
    # Here you modify the data points, for example, shifting y values
    new_y = [(val + 0.01 * frame) % 2 for val in y]
    lines.set_data(x, new_y)
    return lines,

ani = FuncAnimation(fig=figure, func=update, frames=range(60), interval=1000/60, blit=True)
plt.show()