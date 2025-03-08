import turtle

def subdivide_grid(grid, subdivide_factor):
    """Subdivide the grid cells into smaller sub-cells."""
    subdivided_grid = []
    
    # For each grid cell, create subdivide_factor * subdivide_factor smaller cells
    for row in grid:
        new_row = []
        for cell in row:
            new_row.extend([cell] * subdivide_factor)  # Add subdivide_factor elements
        subdivided_grid.extend([new_row]*subdivide_factor)
        #subdivided_grid.append(new_row * subdivide_factor)  # Duplicate for each sub-cell row
    return subdivided_grid

def draw_grid(grid, cell_size=30, shape_size=1):
    """Draw the grid with passable and blocked cells using stamps."""
    turtle.speed(0)
    turtle.penup()
    turtle.tracer(False)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            x, y = j * cell_size - len(grid[0]) * cell_size / 2, len(grid) * cell_size / 2 - i * cell_size
            turtle.goto(x, y)
            #turtle.shapesize(stretch_wid=shape_size, stretch_len=shape_size)  # Set shape size
            turtle.shapesize(cell_size/shape_size)
            if grid[i][j] == 1:
                turtle.shape("square")
                turtle.color("white")  # Passable area
            else:
                turtle.shape("square")
                turtle.color("black")  # Blocked area
            
            turtle.stamp()
        turtle.update()
    turtle.tracer(True)

def draw_path(path, cell_size=30, shape_size=1, color="green"):
    """Draw the path using turtle.stamp() with a specific color."""
    turtle.penup()
    turtle.pendown()
    turtle.shape("circle")
    turtle.color(color)
    turtle.tracer(5)
    #turtle.shapesize(stretch_wid=shape_size, stretch_len=shape_size)  # Set shape size
    turtle.shapesize(cell_size/shape_size)
    for (i, j) in path:
        x, y = j * 1 - len(path) * 1 / 2, len(path) * 1 / 2 - i * 1
        x, y = j * cell_size - len(grid[0]) * cell_size / 2, len(grid) * cell_size / 2 - i * cell_size
        turtle.goto(x, y)
        #turtle.update()
        #turtle.stamp()

def find_all_paths(grid, start, end):
    turtle.color(1,0,0)
    turtle.pendown()
    turtle.tracer(5)
    def dfs(x, y, path,done_grid = []):
        # Base case: if the current point is the end point, save the path

        if (x, y) == end:
            print("end")
            all_paths.append(path.copy())
            return done_grid
        if (x,y) in done_grid:
            return done_grid
        if grid[x][y] == 0:
            done_grid.append((x,y))
            return done_grid
        done_grid.append((x,y))

        # Directions for movement: right, left, down, up
        directions = [(1, 0), (-1, 0), (0, -1), (0, 1),(1,1),(-1,1),(1,-1),(-1,-1)]
        #directions = [(1,1),(-1,1),(1,-1),(-1,-1)]
        # Mark the current cell as visited
        #grid[x][y] = 0
        i,j= x,y
        cell_size =10
        x1, y1 = j * cell_size - len(grid[0]) * cell_size / 2, len(grid) * cell_size / 2 - i * cell_size
        turtle.goto(x1,y1)
        turtle.stamp()
        # Explore all 4 directions
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            #if 0 <= nx < len(grid) and 0 <= ny < len(grid[1]) :
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[1])and grid[nx][ny] == 1:
                #print(nx,ny)
                #turtle.penup()
                #turtle.goto(x1,y1)
                #turtle.pendown()
                dfs(nx, ny, path + [(nx, ny)],done_grid)
        return done_grid
        
        # Backtrack, unmark the current cell
        #grid[x][y] = 1

    all_paths = []
    start_x, start_y = start
    end_x, end_y = end
    
    # Ensure the start and end are valid positions
    if grid[start_x][start_y] == 1 and grid[end_x][end_y] == 1:
        dfs(start_x, start_y, [start])
        #dfs(start_x, start_y, [start])
    
    return all_paths

# Example grid and points
grid = [
    [1, 1, 0, 0, 0],
    [1, 1, 0, 1, 1],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 1],
    [0, 0, 0, 0, 1]
]
print((grid))
grid = subdivide_grid(grid,8)
print((grid))
start = (0, 0)  # Starting point (A)
end = (32, 32)    # Ending point (B)

# Define the pixel size (how large each grid cell is) and shape size (how large the stamps are)
pixel_size = 10  # Adjust to control the space between cells
shape_size = 20   # Adjust to control the size of the stamps

# Initialize the Turtle window
turtle.setup(600, 600)
turtle.bgcolor("lightblue")


draw_grid(grid, cell_size=pixel_size, shape_size=shape_size)

# Draw the grid and paths
all_paths = find_all_paths(grid, start, end)




draw_grid(grid, cell_size=pixel_size, shape_size=shape_size)
for path in all_paths:
    draw_path(path, cell_size=pixel_size, shape_size=shape_size)

turtle.done()
