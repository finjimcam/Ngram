from PIL import Image
import numpy as np

class nonogram:
    def __init__(self, location, scale, mode="GS"):
        self.img = Image.open(location)
        self.mode = mode  # 'GS' for grayscale, 'RGB' for color
        self.width, self.height = self.img.size
        self.resize((int(self.width / scale), int(self.height / scale)))
        self.x,self.y = self.to_nonogram()

    def resize(self, newSize):
        self.img = self.img.resize(newSize)
        self.width, self.height = self.img.size

    def show(self):
        self.img.show()

    def to_nonogram(self, threshold=128):
        if self.mode == 'GS':
            self.img = self.img.convert('L')
            return self.toGrey(threshold)
        elif self.mode == 'RGB':
            return self.toColour()
        else:
            raise ValueError("Unsupported image mode: {}".format(self.mode))

    def toGrey(self, threshold):
        # Convert image to binary based on the threshold
        binary_image = self.img.point(lambda p: 255 if p > threshold else 0)
        
        # Create numpy array of the binary image
        binary_array = np.array(binary_image)
        #print(binary_array)
        
        # Generate row clues
        col_clues = [self._generate_clues(row) for row in binary_array]
        
        # Generate column clues
        row_clues = [self._generate_clues(col) for col in binary_array.T]
        #print(row_clues, col_clues)
        return row_clues, col_clues

    def toColour(self):
        raise NotImplementedError("Colour nonograms are not implemented yet")

    def _generate_clues(self, line):
        clues = []
        count = 0
        for pixel in line:
            if pixel == 0:  # Filled cell
                count += 1
            elif count > 0:
                clues.append(count)
                count = 0
        if count > 0:
            clues.append(count)
        return clues
    
    def printGrid(self):
        print(["X"],self.x)
        for i in self.y:
            print(i)

# Example usage:
#converter = nonogram('desktop/bird.jpg', 25, "GS")
#converter.printGrid()
