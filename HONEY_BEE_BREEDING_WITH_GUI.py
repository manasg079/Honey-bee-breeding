import pygame
from tkinter import *
import math
from PIL import Image, ImageTk
from tkinter.messagebox import showinfo

class Honey_Bee_Breeding:
    base_case = {
        0: [-1, 0],
        1: [0, 1],
        2: [1, 1],
        3: [1, 0],
        4: [0, -1],
        5: [-1, -1]
    }

    def __init__(self, num1: int, num2: int):
        self.n1 = num1
        self.n2 = num2
        self.distance = self.calculate_distance(self.n1, self.n2)

    def max_in_ring(self, ring: int) -> int:
        return 3 * ring**2 + 3 * ring + 1

    def ring_number(self, num: int) -> int:
        return math.ceil((math.sqrt((4 * num - 1) / 12.0) - 0.5))

    def num_to_coordinate(self, num: int) -> list:
        if num == 1:
            return [0, 0]

        side_length = ring = self.ring_number(num)
        ring_distance = self.max_in_ring(ring) - num
        base_number = ring_distance // side_length
        base_ring_distance = ring_distance % side_length

        corner = self.base_case[base_number]
        next_corner = self.base_case[(base_number + 1) % 6]
        direction = [next_corner[0] - corner[0], next_corner[1] - corner[1]]
        coords = [corner[0] * ring + direction[0] * base_ring_distance, corner[1] * ring + direction[1] * base_ring_distance]

        return coords

    def coordinate_to_num(self, coord):
        if coord == [0, 0]:
            return 1

        ring = max([max(coord) - min(coord), max(map(abs, coord))])
        if coord[0] == ring:
            side = 2
        elif coord[0] == -ring:
            side = 5
        elif coord[1] == ring:
            side = 1
        elif coord[1] == -ring:
            side = 4
        elif coord[0] > coord[1]:
            side = 3
        else:
            side = 0

        max_num = self.max_in_ring(ring)
        corner = [x * ring for x in self.base_case[side]]
        ring_distance = side * ring + self.length_of_diff([coord[i] - corner[i] for i in range(2)])
        return max_num if ring_distance == ring * 6 else max_num - ring_distance

    def path_between(self):
        coord1, coord2 = self.num_to_coordinate(self.n1), self.num_to_coordinate(self.n2)
        diff = [coord1[i] - coord2[i] for i in range(2)]
        path = []

        while diff != [0, 0]:
            path.append([coord2[i] + diff[i] for i in range(2)])

            if diff[0] < 0 and diff[1] < 0:
                move = [1, 1]
            elif diff[0] > 0 and diff[1] > 0:
                move = [-1, -1]
            elif diff[0] != 0:
                move = [-1 if diff[0] > 0 else 1, 0]
            else:
                move = [0, -1 if diff[1] > 0 else 1]

            diff = [diff[i] + move[i] for i in range(2)]

        path.append(coord2)

        return path

    def length_of_diff(self, diff):
        for i in range(len(diff)):
            if diff[i] < 0:
                diff[i] *= -1

        if diff[0] > 0 and diff[1] > 0:
            return max(diff)
        else:
            return max(diff) - min(diff)

    def calculate_distance(self, num1, num2):
        diff = [self.num_to_coordinate(num1)[i] - self.num_to_coordinate(num2)[i] for i in range(2)]
        return self.length_of_diff(diff)


def generate_leftover_coordinates(x_diff, sign, num, ring):
    if ring == 1 and sign == 1:
        return [[-74, 0]]
    elif ring == 1 and sign != 1:
        return [[74, 0]]

    x = (num * 37) * (ring + 1) * x_diff
    y_start = 22 * (ring - 1)
    coordinates = []
    for i in range(ring):
        y = y_start - i * 44
        coordinates.append([x, y])

    for i in range(len(coordinates)):
        for j in range(2):
            coordinates[i][j] *= sign

    return coordinates

def generate_hexagon_coordinates(ring):
    coordinates = [[0, ring * 44]]

    for i in range(1, ring + 1):
        x = -i * 37
        y = ring * 44 - i * 22
        coordinates.append([x, y])

    if ring > 1:
        l = generate_leftover_coordinates(1, 1, -1, ring - 1)
        coordinates.extend(l)

    for i in range(ring, 0, -1):
        x = -i * 37
        y = -ring * 44 + i * 22
        coordinates.append([x, y])

    coordinates.append([0, -ring * 44])

    for i in range(1, ring + 1):
        x = i * 37
        y = -ring * 44 + i * 22
        coordinates.append([x, y])

    if ring > 1:
        l = generate_leftover_coordinates(-1, -1, 1, ring - 1)
        coordinates.extend(l)

    for i in range(ring, 0, -1):
        x = i * 37
        y = ring * 44 - i * 22
        coordinates.append([x, y])

    for i in range(ring - 1):
        x = coordinates.pop()
        coordinates.insert(0, x)

    return coordinates

def hexagon_vertices(x, y, size):
    vertices = []
    for i in range(6):
        angle = 60 * i
        vertex_x = x + size * math.cos(math.radians(angle))
        vertex_y = y + size * math.sin(math.radians(angle))
        vertices.extend([vertex_x, vertex_y])
    return vertices

def draw_hexagon(canvas, x, y, size, number, color):
    vertices = hexagon_vertices(x, y, size)
    hexagon = canvas.create_polygon(vertices, outline='black', fill=color, tags=("hexagon", f"hexagon_{number}"))
    canvas.create_text(x, y, text=str(number), font=("Verdana", 12, "bold"), fill='black')

def draw_hexagon_with_timegap():
    global hexagon_count, hexagon_num
    max_ring = 7
    if hexagon_count < max_ring:
        hexagon_count += 1
        coordinates = generate_hexagon_coordinates(hexagon_count)

        i = 0
        for x, y in coordinates:
            color = colors[hexagon_num % len(colors)]
            root.after(i * 50, lambda x=x, y=y, num=hexagon_num, color=color: draw_hexagon(canvas, center_x + x, center_y + y, hexagon_size, num, color))
            hexagon_num += 1
            i += 1

        root.after(len(coordinates) * 50, draw_hexagon_with_timegap)

def draw_comb():
    global hexagon_count, hexagon_num
    draw_hexagon(canvas, center_x, center_y, hexagon_size, 1, colors[0])
    hexagon_count = 0
    hexagon_num = 2
    draw_hexagon_with_timegap()

def open_main_window():
    global root, main_window, canvas, center_x, center_y, hexagon_size, hexagon_count, hexagon_num, colors

    root.destroy()

    main_window = Tk()
    main_window.title("Honey Bee Breeding")
    main_window.attributes('-fullscreen', True)
    main_window.configure(bg="light yellow")

    canvas_frame = Frame(main_window, bg='white', highlightbackground='white', highlightthickness=1)
    canvas_frame.pack(side='right', anchor="nw", padx=80, pady=50)

    canvas = Canvas(canvas_frame, width=800, height=800, bg='white')
    canvas.pack(side="left", fill="both", expand=True)

    center_x = 400
    center_y = 380 - 37.8  # Move the honey bee grid 1 cm upwards
    hexagon_size = 25
    hexagon_count = 0
    hexagon_num = 2
    colors = ["yellow", "goldenrod", "dark orange"]

    draw_comb()

    input_frame = Frame(main_window, bg='white', highlightbackground='white', highlightthickness=1)
    input_frame.pack(side='left', anchor="nw", padx=50, pady=50)

    cell_a_label = Label(input_frame, text="Cell A:", font=("Verdana", 14), bg="white")
    cell_a_label.pack(pady=10)
    cell_a_entry = Entry(input_frame, font=("Verdana", 14))
    cell_a_entry.pack(pady=10)

    cell_b_label = Label(input_frame, text="Cell B:", font=("Verdana", 14), bg="white")
    cell_b_label.pack(pady=10)
    cell_b_entry = Entry(input_frame, font=("Verdana", 14))
    cell_b_entry.pack(pady=10)

    def trace_shortcut():
        cell_a = int(cell_a_entry.get())
        cell_b = int(cell_b_entry.get())
        bee = Honey_Bee_Breeding(cell_a, cell_b)
        distance = bee.calculate_distance(cell_a, cell_b)
        path = bee.path_between()
        path_str = " - ".join(str(bee.coordinate_to_num(coord)) for coord in path)

        canvas.delete("highlight")  # Clear previous highlights

        for coord in path:
            coord_num = bee.coordinate_to_num(coord)
            hexagon_id = f"hexagon_{coord_num}"
            canvas.itemconfig(hexagon_id, fill="blue", tags=("highlight", hexagon_id))

        shortest_distance_label.config(text=f"Shortest Distance: {distance}")
        showinfo("Shortest Distance", f"The distance between cell {cell_a} and cell {cell_b} is {distance}\nThe Path: {path_str}")

    def reset():
        global cell_a, cell_a
        cell1 = None
        cell2 = None

        canvas.delete('all')
        draw_comb()
        cell_a_entry.delete(0, END)
        cell_b_entry.delete(0, END)
        shortest_distance_label.config(text="Shortest Distance: ")

    def close_main_window():
        pygame.mixer.music.stop()
        main_window.destroy()

    trace_shortcut_button = Button(input_frame, text="Trace My Shortcut", font=("Verdana", 14), command=trace_shortcut)
    trace_shortcut_button.pack(pady=10)

    reset_button = Button(input_frame, text="Reset", font=("Verdana", 14), command=reset)
    reset_button.pack(pady=10)

    close_button = Button(input_frame, text="Close", font=("Verdana", 14), command=close_main_window)
    close_button.pack(pady=10)

    shortest_distance_label = Label(input_frame, text="Shortest Distance: ", font=("Verdana", 14), bg="white")
    shortest_distance_label.pack(pady=10)

    main_window.mainloop()

root = Tk()
root.title("Welcome")
root.geometry("600x400")
root.configure(bg="white")

# Load the image file
bee_image = PhotoImage(file="C:\\Users\\manas\\OneDrive\\Desktop\\honey_bee_picture.png")

# Create a frame for organizing the layout
frame = Frame(root, bg="white")
frame.pack(pady=20)

# Create the heading
heading_label = Label(frame, text="HONEY BEE BREEDING", font=("Verdana", 18, "bold"), bg="white")
heading_label.pack()

# Create the start button and place it at the top middle
start_button = Button(frame, text="Start", command=open_main_window, font=("Verdana", 14), bg="light blue")
start_button.pack(pady=10)

# Create a Label to display the image and place it below the start button
image_label = Label(frame, image=bee_image, bg="light yellow")
image_label.pack(pady=20)

# Initialize and play bee sound effect
pygame.mixer.init()
bee_sound = "C:\\Users\\manas\\Downloads\\bee_sound.wav"  # Path to your bee sound effect file
pygame.mixer.music.load(bee_sound)
pygame.mixer.music.play(-1)  # Play on a loop

root.mainloop()
