import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def SignalSource(images, positions):
    for img, pos in zip(images, positions):
        yield (img, pos)
        input("Next")


class OCRLabelizer(tk.Tk):
    def __init__(self,images, positions,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.signal = SignalSource(images, positions)

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
            self.figure.canvas.draw()
            self.after(100, self.update_plot)
        except StopIteration:
            print("All picture are labelled")