import tkinter as tk
from tkinter import messagebox, scrolledtext
import collections
import winsound

# Global variables
GRID_SIZE = 10  # 10x10 grid for simplicity
CELL_SIZE = 40  # Each cell will be 40x40 pixels
OBSTACLE = 1  # Represent obstacles
OPEN_SPACE = 0  # Represent open space
FIRE_POSITION = 2  # Fire position
FIRE_TRUCK = 3  # Fire truck position

# Create the initial grid
grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Create a basic Tkinter window
root = tk.Tk()
root.title("Fire Truck Pathfinding")
canvas = tk.Canvas(root, width=GRID_SIZE * CELL_SIZE, height=GRID_SIZE * CELL_SIZE)
canvas.pack()

# Label and Text Box to show the path
path_label = tk.Label(root, text="Shortest Path:")
path_label.pack()
scroll_text = scrolledtext.ScrolledText(root, width=30, height=10)
scroll_text.pack()

# Queue for BFS
queue = collections.deque()
visited = set()

# Directions for moving (up, down, left, right)
directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Variable to track current mode (fire or obstacle)
current_mode = None

def draw_grid():
    """Draw the grid on the canvas."""
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            text = ""
            color = "white"  # Default color for open space
            emoji_color = "black"  # Default emoji color
            if grid[i][j] == OBSTACLE:
                text = "🚧"  # Obstacle emoji
                emoji_color = "black"  # Set obstacle emoji color to black
            elif grid[i][j] == FIRE_POSITION:
                color = "white"  # Keep the background white
                text = "🔥"  # Fire emoji (orange)
                emoji_color = "orange"  # Set fire emoji color to orange
            elif grid[i][j] == FIRE_TRUCK:
                color = "white"  # Keep the background white
                text = "🚒"  # Fire truck emoji (red)
                emoji_color = "red"  # Set fire truck emoji color to red

            # Draw the cell with background color
            canvas.create_rectangle(
                j * CELL_SIZE, i * CELL_SIZE, 
                (j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE, 
                fill=color, outline="black"
            )

            # Place the emoji in the middle of the cell with the correct color
            if text:
                canvas.create_text(
                    j * CELL_SIZE + CELL_SIZE // 2, 
                    i * CELL_SIZE + CELL_SIZE // 2, 
                    text=text, font=("Arial", 16), fill=emoji_color
                )


def bfs(start, end):
    """Breadth-first search to find the shortest path."""
    queue.clear()
    visited.clear()
    queue.append((start, []))  # Store position and the path taken to reach it
    visited.add(start)

    while queue:
        (x, y), path = queue.popleft()

        # If we reach the fire position, return the path
        if (x, y) == end:
            return path + [(x, y)]

        # Check all 4 possible directions
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and grid[nx][ny] != OBSTACLE and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append(((nx, ny), path + [(x, y)]))

    return []  # No path found


def start_game():
    """Start the game and find the path."""
    start = (0, 0)  # Fire truck's start position (top-left corner)
    end = None

    # Find the fire position (2) in the grid
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == FIRE_POSITION:
                end = (i, j)
                break

    if end is None:
        messagebox.showerror("Error", "Fire position not set!")
        return

    # Find the shortest path using BFS
    path = bfs(start, end)
    
    if path:
        scroll_text.delete(1.0, tk.END)
        scroll_text.insert(tk.END, f"Shortest path: {path}\n")

        # Move fire truck along the path and play sound
        for step in path:
            x, y = step
            grid[x][y] = FIRE_TRUCK  # Move fire truck to the new position
            draw_grid()
            winsound.Beep(1000, 300)  # Play a siren sound when moving
            canvas.update()
            canvas.after(500)  # Delay to show the movement step by step
    else:
        messagebox.showerror("Error", "No path found!")


def set_fire_position(event):
    """Set the fire position based on the clicked cell."""
    if current_mode == "fire":
        fire_position_x = event.x // CELL_SIZE
        fire_position_y = event.y // CELL_SIZE
        if grid[fire_position_x][fire_position_y] != OBSTACLE:  # Ensure fire is not placed on an obstacle
            grid[fire_position_x][fire_position_y] = FIRE_POSITION
            draw_grid()


def set_obstacle(event):
    """Set an obstacle based on the clicked cell."""
    if current_mode == "obstacle":
        obstacle_x = event.x // CELL_SIZE
        obstacle_y = event.y // CELL_SIZE
        grid[obstacle_x][obstacle_y] = OBSTACLE
        draw_grid()


def set_fire_mode():
    """Activate fire position setting mode."""
    global current_mode
    current_mode = "fire"


def set_obstacle_mode():
    """Activate obstacle setting mode."""
    global current_mode
    current_mode = "obstacle"


# Bind mouse clicks to set fire position and obstacles
canvas.bind("<Button-1>", set_fire_position)  # Left-click to set fire
canvas.bind("<Button-3>", set_obstacle)  # Right-click to set obstacle

# Buttons and interactions
start_button = tk.Button(root, text="Start Game", command=start_game)
start_button.pack()

fire_button = tk.Button(root, text="Set Fire Position", command=set_fire_mode)
fire_button.pack()

obstacle_button = tk.Button(root, text="Set Obstacle Position", command=set_obstacle_mode)
obstacle_button.pack()

# Initial drawing of the grid
draw_grid()

# Run the Tkinter event loop
root.mainloop()
