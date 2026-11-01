
import tkinter as tk
from tkinter import ttk, messagebox
from itertools import permutations
from time import perf_counter
from math import inf
import random


# ---------------- DISTANCE CALCULATION ----------------

def calculate_distance(route, matrix):
    return sum(
        matrix[route[i]][route[i + 1]]
        for i in range(len(route) - 1)
    )


# ---------------- BRUTE FORCE ALGORITHM ----------------

def brute_force(matrix):
    n = len(matrix)

    if n == 1:
        return [0, 0], 0

    best_route = None
    best_distance = inf

    for order in permutations(range(1, n)):
        route = [0] + list(order) + [0]
        distance = calculate_distance(route, matrix)

        if distance < best_distance:
            best_distance = distance
            best_route = route

    return best_route, best_distance


# ---------------- NEAREST NEIGHBOUR ALGORITHM ----------------

def nearest_neighbour(matrix):
    n = len(matrix)

    if n == 1:
        return [0, 0], 0

    route = [0]
    unvisited = set(range(1, n))
    current = 0

    while unvisited:
        next_city = min(
            unvisited,
            key=lambda city: matrix[current][city]
        )

        route.append(next_city)
        unvisited.remove(next_city)
        current = next_city

    route.append(0)

    return route, calculate_distance(route, matrix)


# ---------------- HELD KARP ALGORITHM ----------------

def held_karp(matrix):
    n = len(matrix)

    if n == 1:
        return [0, 0], 0

    if n == 2:
        return [0, 1, 0], matrix[0][1] + matrix[1][0]

    dp = {}
    parent = {}

    # Initialize starting paths
    for city in range(1, n):
        mask = 1 << (city - 1)
        dp[(mask, city)] = matrix[0][city]
        parent[(mask, city)] = 0

    # Calculate minimum distances
    for mask in range(1, 1 << (n - 1)):
        for last in range(1, n):

            if not (mask & (1 << (last - 1))):
                continue

            previous_mask = mask ^ (1 << (last - 1))

            if previous_mask == 0:
                continue

            best = inf
            best_previous = None

            for previous in range(1, n):

                if previous_mask & (1 << (previous - 1)):

                    candidate = (
                        dp[(previous_mask, previous)]
                        + matrix[previous][last]
                    )

                    if candidate < best:
                        best = candidate
                        best_previous = previous

            dp[(mask, last)] = best
            parent[(mask, last)] = best_previous

    # Find the minimum complete tour
    full_mask = (1 << (n - 1)) - 1

    last = min(
        range(1, n),
        key=lambda city: (
            dp[(full_mask, city)] + matrix[city][0]
        )
    )

    best_distance = dp[(full_mask, last)] + matrix[last][0]

    # Reconstruct route
    reverse_route = []
    mask = full_mask
    current = last

    while current != 0:
        reverse_route.append(current)

        previous = parent[(mask, current)]

        mask ^= (1 << (current - 1))
        current = previous

    route = [0] + reverse_route[::-1] + [0]

    return route, best_distance


# ---------------- TSP GUI APPLICATION ----------------

class TSPApplication:

    def __init__(self, root):

        self.root = root
        self.root.title("Travelling Salesman Problem Visualizer")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f4f6f7")

        self.matrix = []
        self.points = {}

        self.create_widgets()

    # ---------------- GUI DESIGN ----------------

    def create_widgets(self):

        title = tk.Label(
            self.root,
            text="Travelling Salesman Problem Visualizer",
            font=("Arial", 20, "bold"),
            bg="#154360",
            fg="white",
            pady=15
        )
        title.pack(fill=tk.X)

        control_frame = tk.Frame(
            self.root,
            bg="#f4f6f7",
            pady=15
        )
        control_frame.pack()

        tk.Label(
            control_frame,
            text="Number of Cities:",
            font=("Arial", 11),
            bg="#f4f6f7"
        ).grid(row=0, column=0, padx=5)

        self.city_entry = tk.Entry(
            control_frame,
            width=8,
            font=("Arial", 11)
        )
        self.city_entry.insert(0, "5")
        self.city_entry.grid(row=0, column=1, padx=5)

        ttk.Button(
            control_frame,
            text="Generate Cities",
            command=self.generate_cities
        ).grid(row=0, column=2, padx=8)

        ttk.Button(
            control_frame,
            text="Brute Force",
            command=lambda: self.run_algorithm("Brute Force")
        ).grid(row=0, column=3, padx=5)

        ttk.Button(
            control_frame,
            text="Nearest Neighbour",
            command=lambda: self.run_algorithm("Nearest Neighbour")
        ).grid(row=0, column=4, padx=5)

        ttk.Button(
            control_frame,
            text="Held-Karp",
            command=lambda: self.run_algorithm("Held-Karp")
        ).grid(row=0, column=5, padx=5)

        ttk.Button(
            control_frame,
            text="Clear",
            command=self.clear
        ).grid(row=0, column=6, padx=5)

        # Canvas for city visualization
        self.canvas = tk.Canvas(
            self.root,
            width=900,
            height=400,
            bg="white",
            highlightthickness=1,
            highlightbackground="#abb2b9"
        )
        self.canvas.pack(pady=10)

        # Output section
        output_label = tk.Label(
            self.root,
            text="Algorithm Results",
            font=("Arial", 14, "bold"),
            bg="#f4f6f7"
        )
        output_label.pack()

        self.output = tk.Text(
            self.root,
            height=9,
            width=110,
            font=("Consolas", 10),
            wrap=tk.WORD
        )
        self.output.pack(pady=10)

        self.generate_cities()

    # ---------------- GENERATE RANDOM CITIES ----------------

    def generate_cities(self):

        try:
            n = int(self.city_entry.get())

            if n < 2 or n > 15:
                messagebox.showerror(
                    "Invalid Input",
                    "Enter number of cities between 2 and 15."
                )
                return

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter a valid integer."
            )
            return

        self.canvas.delete("all")
        self.output.delete("1.0", tk.END)

        self.matrix = [
            [0 for _ in range(n)]
            for _ in range(n)
        ]

        self.points = {}

        # Generate random city coordinates
        for i in range(n):

            x = random.randint(60, 840)
            y = random.randint(50, 350)

            self.points[i] = (x, y)

        # Calculate Euclidean distance matrix
        for i in range(n):
            for j in range(n):

                x1, y1 = self.points[i]
                x2, y2 = self.points[j]

                distance = (
                    (x1 - x2) ** 2 +
                    (y1 - y2) ** 2
                ) ** 0.5

                self.matrix[i][j] = round(distance, 2)

        self.draw_cities()

    # ---------------- DRAW CITIES ----------------

    def draw_cities(self):

        self.canvas.delete("all")

        for city, (x, y) in self.points.items():

            self.canvas.create_oval(
                x - 17,
                y - 17,
                x + 17,
                y + 17,
                fill="#d6eaf8",
                outline="#174a7e",
                width=2
            )

            label = chr(65 + city) if city < 26 else str(city + 1)

            self.canvas.create_text(
                x,
                y,
                text=label,
                font=("Arial", 10, "bold")
            )

    # ---------------- DRAW ROUTE ----------------

    def draw_route(self, route):

        self.draw_cities()

        for i in range(len(route) - 1):

            city1 = route[i]
            city2 = route[i + 1]

            x1, y1 = self.points[city1]
            x2, y2 = self.points[city2]

            self.canvas.create_line(
                x1, y1, x2, y2,
                fill="#e74c3c",
                width=3,
                arrow=tk.LAST
            )

    # ---------------- RUN ALGORITHMS ----------------

    def run_algorithm(self, algorithm):

        if not self.matrix:
            messagebox.showwarning(
                "Warning",
                "Generate cities first."
            )
            return

        n = len(self.matrix)

        if algorithm == "Brute Force" and n > 10:
            messagebox.showwarning(
                "Warning",
                "Brute Force is slow for more than 10 cities."
            )
            return

        if algorithm == "Nearest Neighbour":
            function = nearest_neighbour

        elif algorithm == "Brute Force":
            function = brute_force

        else:
            function = held_karp

        start_time = perf_counter()

        route, distance = function(self.matrix)

        end_time = perf_counter()

        execution_time = (end_time - start_time) * 1000

        self.draw_route(route)

        city_names = [
            chr(65 + city) if city < 26 else str(city + 1)
            for city in route
        ]

        self.output.delete("1.0", tk.END)

        self.output.insert(
            tk.END,
            f"Algorithm: {algorithm}\n"
        )

        self.output.insert(
            tk.END,
            f"Optimal/Calculated Route: {' -> '.join(city_names)}\n"
        )

        self.output.insert(
            tk.END,
            f"Total Distance: {distance:.2f}\n"
        )

        self.output.insert(
            tk.END,
            f"Execution Time: {execution_time:.4f} ms\n"
        )

        self.output.insert(
            tk.END,
            f"Number of Cities: {n}\n"
        )

    # ---------------- CLEAR ----------------

    def clear(self):

        self.output.delete("1.0", tk.END)
        self.canvas.delete("all")


# ---------------- MAIN PROGRAM ----------------

if __name__ == "__main__":

    root = tk.Tk()

    app = TSPApplication(root)

    root.mainloop()
