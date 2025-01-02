import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json

def SignalSource(images, positions, label):
    for img, pos in zip(images, positions):
        l = []
        for p in pos:
            yield (img, p)
            l.append(input("Label: "))
        label.append(l)


class OCRLabelizer(tk.Tk):
    def __init__(self,images, positions,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._label = []
        self._positions = positions
        self.signal = SignalSource(images, positions, self._label)

        # Create a plot that can be embedded in a tkinter window.
        self.figure = Figure(figsize=(6, 4))
        self.plt = self.figure.add_subplot(111)
        canvas = FigureCanvasTkAgg(self.figure, self)
        canvas.draw()
        canvas.get_tk_widget().pack()
        self.update_plot()

    def update_plot(self):
        """Get new signal data and update plot.  Called periodically"""
        try:
            img, pos = next(self.signal)
            # Refresh plot with new signal data.
            self.plt.clear()
            self.plt.margins(x=0)
            self.plt.imshow(img)
            self.plt.scatter(pos[0], pos[1], s=1000, c='red', marker='x', clip_on=False)
            self.figure.canvas.draw()
            self.after(100, self.update_plot)
        except StopIteration:
            print("All picture are labelled")
            self.quit()
            data = {l:p for label, position in zip(self._label, self._positions) for l, p in zip(label, position)}
            with open("dataset.json", "w") as f:
                json.dump(data, f)