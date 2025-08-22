import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class ResourceGraph(QWidget):
    """
    A QWidget that shows CPU/Memory/Disk usage as a live graph.
    """
    def __init__(self, fetch_callback, parent=None):
        super().__init__(parent)
        self.fetch_callback = fetch_callback  # function to fetch resource usage

        layout = QVBoxLayout(self)

        self.figure, self.ax = plt.subplots(3, 1, figsize=(5, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.cpu_data, self.mem_data, self.disk_data = [], [], []

        # Timer for updating graph
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(3000)  # update every 3 sec

    def update_graph(self):
        stats = self.fetch_callback()
        if not stats or not stats.get("cpu"):
            return

        try:
            # CPU
            cpu_val = float(stats["cpu"].replace("%us", "").strip())
            self.cpu_data.append(cpu_val)

            # Memory
            mem_val = float(stats["memory"])
            self.mem_data.append(mem_val)

            # Disk
            disk_val = float(stats["disk"].replace("%", ""))
            self.disk_data.append(disk_val)

            # Keep last 20 values
            self.cpu_data = self.cpu_data[-20:]
            self.mem_data = self.mem_data[-20:]
            self.disk_data = self.disk_data[-20:]

            # Clear and replot
            for a in self.ax:
                a.clear()

            self.ax[0].plot(self.cpu_data, label="CPU %")
            self.ax[1].plot(self.mem_data, label="Memory %", color="orange")
            self.ax[2].plot(self.disk_data, label="Disk %", color="green")

            for a in self.ax:
                a.legend(loc="upper right")
                a.set_ylim(0, 100)

            self.canvas.draw()
        except Exception:
            pass


# For testing this widget directly
if __name__ == "__main__":
    def fake_fetch():
        import random
        return {"cpu": f"{random.randint(1, 99)}%us",
                "memory": random.randint(1, 99),
                "disk": f"{random.randint(1, 99)}%"}

    app = QApplication(sys.argv)
    win = ResourceGraph(fetch_callback=fake_fetch)
    win.show()
    sys.exit(app.exec_())
