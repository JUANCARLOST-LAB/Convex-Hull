import matplotlib.pyplot as plt
import numpy as np

class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y
    
    def cross(self, point) -> float:
        return point.x * self.y - point.y * self.x
    
    def __lt__(self, point):
        if self.x == point.x:
            return self.y < point.y
        return self.x < point.x
    
    def __sub__(self, point):
        return Point(self.x - point.x, self.y - point.y)
    
class Edge:
    def __init__(self, point_1: Point, point_2: Point) -> None:
        self.point_1 = point_1
        self.point_2 = point_2

class EdgeList:
    def __init__(self, coordinates : list) -> None:
        self.edges = []
        for i in range(len(coordinates)):
            self.edges.append(Edge(coordinates[i], coordinates[(i+1)%len(coordinates)]))
    
    def graph(self, ax):
        for edge in self.edges:
            ax.plot([edge.point_1.x, edge.point_2.x], [edge.point_1.y, edge.point_2.y])

class ConvexHull:

    def __init__(self, coordinates: list) -> None:
        self.coordinates = []

        for coordinate in coordinates:
            self.coordinates.append(Point(*coordinate))

        self.upper_convex = []
        self.lower_convex = []

        self.sortCoordinates()

        self.buildLowerConvex()
        self.buildUpperConvex()

        self.edges = self.combineUpperAndLower()

        self.generateEdges()

    def sortCoordinates(self) -> None:
        self.coordinates.sort()
    
    def left(self, coord_1: Point, coord_2: Point, coord_3: Point) -> bool:
        vector_1 = coord_2 - coord_1
        vector_2 = coord_3 - coord_1

        return vector_2.cross(vector_1) <= 0
    
    def buildLowerConvex(self) -> None:
        self.lower_convex.append(self.coordinates[0])
        self.lower_convex.append(self.coordinates[1])

        for i in range(2, len(self.coordinates)):
            while len(self.lower_convex) >= 2 and self.left(self.lower_convex[-2], self.lower_convex[-1], self.coordinates[i]):
                self.lower_convex.pop()
            self.lower_convex.append(self.coordinates[i])

    def buildUpperConvex(self) -> None:
        self.upper_convex.append(self.coordinates[-1])
        self.upper_convex.append(self.coordinates[-2])

        for i in range(len(self.coordinates) - 2, -1, -1):
            while len(self.upper_convex) >= 2 and self.left(self.upper_convex[-2], self.upper_convex[-1], self.coordinates[i]):
                self.upper_convex.pop()
            self.upper_convex.append(self.coordinates[i])

    def combineUpperAndLower(self):
        self.upper_convex.pop()
        self.upper_convex.pop(0)

        self.lower_convex.extend(self.upper_convex)

        return self.lower_convex

    def generateEdges(self):
        self.edgeList = EdgeList(self.edges)
    
    def printEdges(self):
        for edge in self.edges:
            print(edge.x, edge.y)

    def graph(self):
        fig, ax = plt.subplots(figsize = (10, 5))
        for coordinate in self.coordinates:
            ax.scatter(coordinate.x, coordinate.y)
        self.edgeList.graph(ax)

        ax.set_title('Convex Hull')
        plt.show()


coordinates = [(np.random.randint(-100, 100),np.random.randint(-100, 100)) for i in range(30)]
Convex = ConvexHull(coordinates)
#Convex.printEdges()
Convex.graph()

