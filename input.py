import tkinter as tk

class PointInputApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Point Input")

        # Canvas for drawing points
        self.canvas = tk.Canvas(self.master, width=500, height=500, bg="light grey")  # Change background color to light grey
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        # Label for instructions
        self.label = tk.Label(self.master, text="Left-click on the canvas to add points.", font=("Helvetica", 12))
        self.label.pack(pady=10)

        # Points list
        self.points = []

        # Bind left-click event to canvas
        self.canvas.bind("<Button-1>", self.add_point)

        # Button to clear points
        self.clear_button = tk.Button(self.master, text="Clear Points", command=self.clear_points)
        self.clear_button.pack(pady=5)

    def add_point(self, event):
        x, y = event.x, event.y
        self.points.append((x, y))
        self.canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill="red")  # Change dot color to red

    def clear_points(self):
        self.points = []
        self.canvas.delete("all")

if __name__ == "__main__":
    root = tk.Tk()
    app = PointInputApp(root)
    root.mainloop()
