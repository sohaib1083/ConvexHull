import tkinter as tk
from math import atan2
import time

class GeometryApp:

    def visualize(self, hull):
        for i in range(1, len(hull)):
            c0 = hull[i-1]
            c1 = hull[i]
            self.canvas.create_line(c0[0], c0[1], c1[0], c1[1], fill="blue", width=2, tags="hulline")
            self.master.update()
            self.canvas.after(1000)

        
        self.delete_lines()
        self.master.update()
        self.canvas.after(1000)

    def delete_lines(self):
        self.canvas.delete("hulline")    


    def __init__(self, master):
        self.master = master
        master.title("Geometry App")

        self.canvas = tk.Canvas(master, width=500, height=500, bg="white")
        self.canvas.pack()

        self.vertices = []
        self.lines = []

        self.canvas.bind("<Button-1>", self.add_vertex)
        self.canvas.bind("<Button-3>", self.add_line)

        self.result_label = tk.Label(master, text="")
        self.result_label.pack()

        self.convex_hull_button = tk.Button(master, text="Compute Convex Hull", command=self.compute_convex_hull)
        self.convex_hull_button.pack()

        self.are_lines_intersecting_button = tk.Button(master, text=" Check intersection", command=self.are_lines_intersecting)
        self.are_lines_intersecting_button.pack()

    def add_vertex(self, event):
        x, y = event.x, event.y
        self.vertices.append((x, y))
        self.canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="black")

    def add_line(self, event):
        x, y = event.x, event.y
        if self.vertices:
            self.lines.append((x, y))
            last_vertex = self.vertices[-1]
            self.canvas.create_line(last_vertex[0], last_vertex[1], x, y, fill="blue")

            # self.are_lines_intersecting()

    def are_lines_intersecting(self):
        self.Determinant_button = tk.Button(self.master, text="Determinant method", command=self.Determinant)
        self.Determinant_button.pack()

        self.CCW_button = tk.Button(self.master, text="Counter clockwise method", command=self.CCW)
        self.CCW_button.pack()

        self.bounding_box_button = tk.Button(self.master, text="Bounding box", command=self.bounding_box)
        self.bounding_box_button.pack()

    def Determinant(self):
        if len(self.vertices) < 4:
            self.result_label.config(text="Not enough vertices to form two lines.")
            return

        line1 = [self.vertices[-4], self.vertices[-3]]
        line2 = [self.vertices[-2], self.vertices[-1]]

        x1, y1 = line1[0]
        x2, y2 = line1[1]
        x3, y3 = line2[0]
        x4, y4 = line2[1]

        det = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if det == 0:
            result = "Lines are parallel and do not intersect"
        else:
            intersect_x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / det
            intersect_y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / det

            if (
                    min(x1, x2) <= intersect_x <= max(x1, x2)
                    and min(y1, y2) <= intersect_y <= max(y1, y2)
                    and min(x3, x4) <= intersect_x <= max(x3, x4)
                    and min(y3, y4) <= intersect_y <= max(y3, y4)
            ):
                result = "Lines intersect at ({:.2f}, {:.2f})".format(intersect_x, intersect_y)
            else:
                result = "Lines do not intersect"

        self.result_label.config(text=result)

    def CCW(self):
        if len(self.vertices) < 4:
            return None

        line1 = [self.vertices[-4], self.vertices[-3]]
        line2 = [self.vertices[-2], self.vertices[-1]]

        if self.is_ccw(line1[0], line1[1], line2[1]) != self.is_ccw(line1[0], line1[1], line2[0]) \
                and self.is_ccw(line2[0], line2[1], line1[1]) != self.is_ccw(line2[0], line2[1], line1[0]):
          
            x1, y1 = line1[0]
            x2, y2 = line1[1]
            x3, y3 = line2[0]
            x4, y4 = line2[1]

            det = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            intersect_x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / det
            intersect_y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / det

            result = "Lines intersect at ({:.2f}, {:.2f})".format(intersect_x, intersect_y)

            self.result_label.config(text=result)

        return None

    @staticmethod
    def is_ccw(p1, p2, p3):
    
        x1, y1 = p1
        x2, y2 = p2
        x3, y3 = p3
        return (y2 - y1) * (x3 - x2) > (y3 - y2) * (x2 - x1)

    def bounding_box(self):
        if len(self.vertices) < 4:
            return None

        line1 = [self.vertices[-4], self.vertices[-3]]
        line2 = [self.vertices[-2], self.vertices[-1]]

        if self.bounding_box_intersect(line1, line2):
            
            x1, y1 = line1[0]
            x2, y2 = line1[1]
            x3, y3 = line2[0]
            x4, y4 = line2[1]

            det = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            intersect_x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / det
            intersect_y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / det

            result = "Lines intersect at ({:.2f}, {:.2f})".format(intersect_x, intersect_y)

            self.result_label.config(text=result)

        return None

    @staticmethod
    def bounding_box_intersect(line1, line2):
        x1, y1 = line1[0]
        x2, y2 = line1[1]
        x3, y3 = line2[0]
        x4, y4 = line2[1]

        return (
                max(x1, x2) >= min(x3, x4) and
                max(x3, x4) >= min(x1, x2) and
                max(y1, y2) >= min(y3, y4) and
                max(y3, y4) >= min(y1, y2)
        )

    def compute_convex_hull(self):
        if len(self.vertices) < 3:
            self.result_label.config(text="Not enough vertices to compute convex hull.")
            return


        hull_vertices = tk.Button(self.master, text="Graham Scan", command=lambda: self.display_convex_hull(self.convex_hull_graham_scan(self.vertices)))
        hull_vertices.pack()


        hull_vertices = tk.Button(self.master, text="Quick Elimination", command=lambda: self.display_convex_hull(self.quick_hull(self.vertices)))
        hull_vertices.pack()


        hull_vertices = tk.Button(self.master, text="Jarvis March", command=lambda: self.display_convex_hull(self.convex_hull_gift_wrapping(self.vertices)))
        hull_vertices.pack()


        hull_vertices = tk.Button(self.master, text="Andrews Monotone Chain", command=lambda: self.display_convex_hull(self.andrews_monotone_chain(self.vertices)))
        hull_vertices.pack()

        hull_vertices = tk.Button(self.master, text="Brute Force", command=lambda: self.display_convex_hull(self.brute_force_convex_hull(self.vertices)))
        hull_vertices.pack()  


    def polar_angle(self, point):
        x, y = point[0] - self.start[0], point[1] - self.start[1]
        return atan2(y, x)

    def dist(self, point):
        x, y = point[0] - self.start[0], point[1] - self.start[1]
        return x**2 + y**2 

    def convex_hull_graham_scan(self, p):
        s = time.time()*1000
        n = len(p)

        if n < 3:
            return p  # Convex hull requires at least 3 p

        start = min(p, key=lambda p: (p[0], p[1]))
        self.start = start  # Save the starting point for later reference

        p.sort(key=lambda p: (self.polar_angle(p), self.dist(p)))

        hull = [start, p[0]]

        for pt in p[1:]:
            while len(hull) > 1 and self.orientation(hull[-2], hull[-1], pt) != 2:
                del hull[-1]
            hull.append(pt)
            # self.visualize(hull)

                
        
        e = time.time()*1000
        ms = (e - s)
        self.result_label.config(text="Convex Hull Computed in {:.7f} ms".format(ms))

        return hull


    def quick_hull(self, p):
        s = time.time()*1000
        if len(p) < 3:
            return p

        leftmost = min(p, key=lambda p: p[0])
        rightmost = max(p, key=lambda p: p[0])

        p_left = [point for point in p if self.orientation(leftmost, rightmost, point) == 1]
        p_right = [point for point in p if self.orientation(leftmost, rightmost, point) == 2]

        hull_left = self.quick_hull_recursive(leftmost, rightmost, p_left)
        hull_right = self.quick_hull_recursive(rightmost, leftmost, p_right)

        e = time.time()*1000
        ms = (e - s)

        self.result_label.config(text="Convex Hull Computed in {:.7f} ms".format(ms))

        return hull_left + hull_right

    def quick_hull_recursive(self, p1, p2, p):
        if not p:
            return []

        farthest = max(p, key=lambda p: self.distance(p1, p2, p))

        p_left = [point for point in p if self.orientation(p1, farthest, point) == 1]
        p_right = [point for point in p if self.orientation(farthest, p2, point) == 1]

        hull_left = self.quick_hull_recursive(p1, farthest, p_left)
        hull_right = self.quick_hull_recursive(farthest, p2, p_right)

        final = [p1] + hull_left + [farthest] + hull_right
        # self.visualize(final)
        return final

    def convex_hull_gift_wrapping(self, p):
        s = time.time()*1000
        n = len(p)
        if n < 3:
            return p  # Convex hull requires at least 3 p

        hull = []
        point_on_hull = min(p)

        while True:
            hull.append(point_on_hull)
            # self.visualize(hull)
            endpoint = p[0]
            for j in range(1, n):
                if endpoint == point_on_hull or self.orientation(point_on_hull, endpoint, p[j]) == 1:
                    endpoint = p[j]
            point_on_hull = endpoint
            if endpoint == hull[0]:
                break

        e = time.time()*1000
        ms = (e - s)

        self.result_label.config(text="Convex Hull Computed in {:.7f} ms".format(ms))

        return hull

    #        Input: a list P of points in the plane.

    # Precondition: There must be at least 3 points.

    # Sort the points of P by x-coordinate (in case of a tie, sort by y-coordinate).

    # Initialize U and L as empty lists.
    # The lists will hold the vertices of upper and lower hulls respectively.

    # for i = 1, 2, ..., n:
    #     while L contains at least two points and the sequence of last two points
    #             of L and the point P[i] does not make a counter-clockwise turn:
    #         remove the last point from L
    #     append P[i] to L

    # for i = n, n-1, ..., 1:
    #     while U contains at least two points and the sequence of last two points
    #             of U and the point P[i] does not make a counter-clockwise turn:
    #         remove the last point from U
    #     append P[i] to U

    # Remove the last point of each list (it's the same as the first point of the other list).
    # Concatenate L and U to obtain the convex hull of P.
    # Points in the result will be listed in counter-clockwise order.

    def andrews_monotone_chain(self, p):
        s = time.time()*1000
        sorted_p = sorted(set(p))

        lower_hull = []
        for p in sorted_p:
            while len(lower_hull) >= 2 and self.orientation(lower_hull[-2], lower_hull[-1], p) != 2:
                lower_hull.pop()
            lower_hull.append(p)
            # self.visualize(lower_hull)

        upper_hull = []
        for p in reversed(sorted_p):
            while len(upper_hull) >= 2 and self.orientation(upper_hull[-2], upper_hull[-1], p) != 2:
                upper_hull.pop()
            upper_hull.append(p)
            # self.visualize(upper_hull)

        e = time.time()*1000
        ms = (e - s)

        self.result_label.config(text="Convex Hull Computed in {:.7f} ms".format(ms))

        return lower_hull[:-1] + upper_hull[:-1]

    def brute_force_convex_hull(self, p):
        s = time.time()*1000
        n = len(p)

        if n < 3:
            return p  # Convex hull requires at least 3 vertices

        hull = []  # Convex hull vertices

        start_point = min(p, key=lambda p: p[0])

        current_point = start_point
        next_point = None

        while next_point != start_point:
            hull.append(current_point)
            # self.visualize(hull)

            next_point = p[0]
            for candidate_point in p:
                if candidate_point != current_point:
                    orientation = self.orientation(current_point, next_point, candidate_point)

                    if (next_point == current_point) or (orientation == 1) or \
                            (orientation == 0 and self.dis(current_point, candidate_point) > self.dis(
                                current_point, next_point)):
                        next_point = candidate_point

            current_point = next_point

        e = time.time()*1000
        elapsed_time_ms = (e - s)

        self.result_label.config(text="Convex Hull Computed in {:.7f} ms".format(elapsed_time_ms))

        return hull

    def orientation(self, p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        
        if val == 0:
            return 0  
        elif val > 0:
            return 1 # clockwise
        else:
            return 2  

    def distance(self, p1, p2, p3):
        return abs((p2[1] - p1[1]) * p3[0] - (p2[0] - p1[0]) * p3[1] + p2[0] * p1[1] - p2[1] * p1[0])

    def dis(self, p1, p2):
        return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2

    def display_convex_hull(self, hull_vertices):
        self.canvas.delete("convex_hull")

        if len(hull_vertices) < 3:
            return  

        for i in range(len(hull_vertices) - 1):
            x1, y1 = hull_vertices[i]
            x2, y2 = hull_vertices[i + 1]
            self.canvas.create_line(x1, y1, x2, y2, fill="red", tags="convex_hull")

        x1, y1 = hull_vertices[-1]
        x2, y2 = hull_vertices[0]
        self.canvas.create_line(x1, y1, x2, y2, fill="red", tags="convex_hull")


if __name__ == "__main__":
    root = tk.Tk()
    app = GeometryApp(root)
    root.mainloop()