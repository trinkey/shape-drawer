from PIL import Image
import math
import time

Color = tuple[int, int, int]

OUTPUT_FILENAME = "output.png"
SCR_WIDTH: int = 256
SCR_HEIGHT: int = 256
BACKGROUND_COLOR: Color = (17, 17, 17)

class Shader:
    def __init__(self, function: callable):
        self.pixel = function

class Circle:
    def __init__(self, radius: int, x: int, y: int, color: Color):
        self.Cx = x; self.Cy = y
        self.radius = radius
        self.color = color

    def inShape(self, x: int, y: int) -> tuple[bool, Color]:
        distance = math.sqrt((x - self.Cx) ** 2 + (y - self.Cy) ** 2)
        return (distance <= self.radius, self.color)

class Quadrilateral:
    def __init__(
        self,
        llx: int, lly: int,
        ulx: int, uly: int,
        lrx: int, lry: int,
        urx: int, ury: int,
        color: tuple[int, int, int]
    ):
        self.x1 = llx; self.y1 = lly
        self.x2 = ulx; self.y2 = uly
        self.x3 = lrx; self.y3 = lry
        self.x4 = urx; self.y4 = ury
        self.color = color

    def inShape(self, x: int, y: int) -> tuple[bool, Color]:
        x1 = self.x1; y1 = self.y1
        x2 = self.x2; y2 = self.y2
        x3 = self.x3; y3 = self.y3
        x4 = self.x4; y4 = self.y4

        def pointInQuad(p, quad):
            edges = [
                (quad[0], quad[1]),
                (quad[1], quad[2]),
                (quad[2], quad[3]),
                (quad[3], quad[0]),
            ]
            windingNumber = 0

            for edge in edges:
                if edge[0][1] <= p[1] < edge[1][1] or edge[1][1] <= p[1] < edge[0][1]:
                    if p[0] < edge[0][0] + (p[1] - edge[0][1]) * (edge[1][0] - edge[0][0]) / (edge[1][1] - edge[0][1]):
                        windingNumber += 1

            return windingNumber % 2 == 1

        quad = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
        return (pointInQuad((x, y), quad), self.color)

def calcPixelColor(x: int, y: int) -> Color:
    for i in shapes:
        c = i.inShape(x, y)
        if c[0]: return c[1]
    return BACKGROUND_COLOR

def gradientBackground(currentColor: Color, x: int, y: int) -> Color:
    if currentColor[0] == BACKGROUND_COLOR[0] \
   and currentColor[1] == BACKGROUND_COLOR[1] \
   and currentColor[2] == BACKGROUND_COLOR[2]:
        return (
            int(x / SCR_WIDTH * 255),
            int(y / SCR_WIDTH * 255),
            255 - int(x / SCR_WIDTH * 127.5) - int(y / SCR_WIDTH * 127.5)
        )
    return currentColor

img = Image.new("RGB", (SCR_WIDTH, SCR_HEIGHT), BACKGROUND_COLOR)
shapes = [
    Quadrilateral(120, 12, 160, 123, 59, 200, 9, 123, (200, 140, 230)),
    Circle(30, 200, 200, (250, 150, 100))
]
shaders = [
    Shader(gradientBackground)
]

start = time.time()

for xCoord in range(SCR_WIDTH):
    for yCoord in range(SCR_HEIGHT):
        img.putpixel((xCoord, yCoord), calcPixelColor(xCoord, yCoord))

for i in shaders:
    for xCoord in range(SCR_WIDTH):
        for yCoord in range(SCR_HEIGHT):
            img.putpixel((xCoord, yCoord), i.pixel(img.getpixel((xCoord, yCoord)), xCoord, yCoord))

img.save("output.png")

end = time.time()
print("Generated in " + str(end - start) + " seconds")
