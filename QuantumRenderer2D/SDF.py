import numpy as np

class BaseSDF:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.sdf = np.full((height, width), np.inf)
        self._computeFunction = self.Circle  # Default function
        #self.generate()
    
    def Circle(self, x, y, center=None, radius=None):
        if center is None:
            center = (self.width // 2, self.height // 2)
        if radius is None:
            radius = min(self.width, self.height) // 4
        
        cx, cy = center
        # Return the computed distance for the circle
        return np.hypot(x - cx, y - cy) - radius
    
    def get_distance(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.sdf[y, x]
        return np.inf  # Out of bounds

    def visualize(self):
        import matplotlib.pyplot as plt
        plt.imshow(self.sdf, cmap='viridis', origin='lower')
        plt.colorbar(label='Distance')
        plt.title('Signed Distance Field')
        plt.show()

    def generate(self):
        # Iterate over every pixel and call the _computeFunction for each
        for y in range(self.height):
            for x in range(self.width):
                # Store the result of _computeFunction for each pixel
                self.sdf[y, x] = self._computeFunction(x, y)

class GridSDF(BaseSDF):
    def __init__(self, width, height):
        super().__init__(width, height)
    
    def generate_from_list(self, points):
        obstacle_points = [(x, y) for x, y, collision in points if collision]
        
        # Define the compute function for the grid
        self._computeFunction = lambda x, y: self._computeGrid(x, y, obstacle_points)

        # Recalculate the signed distance field
        self.generate()
    
    def _computeGrid(self, x, y, obstacle_points):
        if (x, y) in obstacle_points:
            return 0
        else:
            distances = [np.hypot(x - ox, y - oy) for ox, oy in obstacle_points]
            if distances:
                return min(distances)
            return np.inf

class CircleSDF(BaseSDF):
    def __init__(self, width, height, center, radius):
        super().__init__(width, height)
        self.center = center
        self.radius = radius
        # Set _computeFunction to use the Circle method for each pixel
        self._computeFunction = lambda x, y: self.Circle(x, y, self.center, self.radius)

class RectangleSDF(BaseSDF):
    def __init__(self, width, height, rect):
        super().__init__(width, height)
        self.rect = rect  # (x_min, y_min, x_max, y_max)
        # Set _computeFunction to use the Rectangle method for each pixel
        self._computeFunction = self._computeRectangle

    def _computeRectangle(self, x, y):
        x_min, y_min, x_max, y_max = self.rect
        dx = max(x_min - x, 0, x - x_max)
        dy = max(y_min - y, 0, y - y_max)
        return np.hypot(dx, dy)-1



if __name__ == '__main__':
    # Example Usage:
    sdf1 = GridSDF(20, 20)
    points = [(5, 5, True), (10, 10, True), (15, 15, True)]
    sdf1.generate_from_list(points)
    sdf1.visualize()

    sdf2 = CircleSDF(20, 20, (10, 10), 5)
    sdf2.generate()
    sdf2.visualize()

    sdf3 = RectangleSDF(20, 20, (5, 5, 15, 15))
    sdf3.generate()
    sdf3.visualize()
