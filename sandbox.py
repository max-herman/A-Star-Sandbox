import tkinter as tk
from astar_alg import aStarSearch
import sys
from scipy import ndimage
import cv2 as cv
import time


class Sandbox:

    def __init__(self, width, height, size, showSteps):
        self.size = size
        self.showSteps = showSteps
        self.problem = {"walls": set(), "start": {"pos": None, "color": "#FF5733"}, "end": {"pos": None, "color": "#3F33FF"}, "borders": (width, height)}
        self.elems = dict()
        self.output = []

    def coverSurrounding(self, x1, y1):
        """[fill space around coordinates to match user pixel size]

        Args:
            x1 ([int]): [x coord]
            y1 ([int]): [y coord]
        """
        for i in range(-1 * self.size, self.size):
            for j in range(-1 * self.size, self.size):
                self.problem["walls"].add((x1 + i, y1 + j))
    

    def removeWalls(self, x1, y1):
        """[delete walls from region]

        Args:
            x1 ([int]): [x coord]
            y1 ([int]): [y coord]
        """
        for i in range(-1 * self.size, self.size):
            for j in range(-1 * self.size, self.size):
                if (x1 + i, y1 + j) in self.problem["walls"]:
                    self.problem["walls"].remove((x1 + i, y1 + j))


    def paint(self, event):
        """[on a mouseclick, create a new canvas object at that event coordinate]

        Args:
            event ([event]): [tkinter mouse click event]
        """
        color = "#476042"
        x1, y1 = ( event.x - self.size ), ( event.y - self.size )
        x2, y2 = ( event.x + self.size ), ( event.y + self.size )

        self.coverSurrounding(event.x, event.y)

        self.elems[(event.x, event.y)] = window.create_oval( x1, y1, x2, y2, fill = color, outline = color )
    

    def toDelete(self, event):
        """[find all wall nodes within user defined range of selection walls, then delete collected walls]

        Args:
            event ([event]]): [tkinter mouse click event]
        """
        nodes = []

        for node in self.elems.keys():
            if event.x > node[0] - self.size and event.x < node[0] + self.size:
                if event.y > node[1] - self.size and event.y < node[1] + self.size:
                    nodes.append(node)

        for node in nodes:
            self.erase(node)


    def erase(self, node):
        """[erase node from canvas]

        Args:
            node ([object]): [tkinter canvas object]
        """
        self.removeWalls(node[0], node[1])
        window.delete(self.elems[(node[0], node[1])])
        self.elems.pop((node[0], node[1]))


    def placeStartMarker(self, event ):
        """[generate node for algorithm start]

        Args:
            node ([object]): [tkinter canvas object]
        """
        if self.problem['start']["pos"] != None:
            window.delete(self.elems[self.problem['start']["pos"]])

        x1, y1 = ( event.x - self.size ), ( event.y - self.size )
        x2, y2 = ( event.x + self.size ), ( event.y + self.size )

        self.elems[(event.x, event.y)] = window.create_oval( x1, y1, x2, y2, fill = self.problem["start"]["color"], outline = self.problem["start"]["color"] )
        self.problem['start']["pos"] = (event.x, event.y)


    def placeEndMarker(self, event ):
        """[generate node for algorithm goal]

        Args:
            node ([object]): [tkinter canvas object]
        """
        if self.problem['end']["pos"] != None:
            window.delete(self.elems[self.problem['end']["pos"]])

        x1, y1 = ( event.x - self.size ), ( event.y - self.size )
        x2, y2 = ( event.x + self.size ), ( event.y + self.size )

        self.elems[(event.x, event.y)] = window.create_oval( x1, y1, x2, y2, fill = self.problem["end"]["color"], outline = self.problem["end"]["color"] )
        self.problem['end']["pos"] = (event.x, event.y)


    def runAstarCallBack(self):
        """[compute shortest path to goal using aStar algorithm, then paint the path on canvas]
        """
        color = "#1ded0e"

        if self.problem["start"]["pos"] != None and self.problem["end"]["pos"] != None:
            t1 = time.time()
            path, visited = aStarSearch(self.problem, master, window, self.size, self.showSteps)
            print("Time: {t}, Nodes Expanded: {n}".format(t = time.time() - t1, n = len(visited)))

            self.output += visited

            if path != None:
                
                for p in path:
                    x1, y1 = ( p[0] - self.size ), ( p[1] - self.size )
                    x2, y2 = ( p[0] + self.size ), ( p[1] + self.size )

                    self.output.append(window.create_oval( x1, y1, x2, y2, fill = color, outline = color ))
        
        window.tag_raise(self.elems[self.problem['start']['pos']])
        window.tag_raise(self.elems[self.problem['end']['pos']])


    def resetCallBack(self):
        self.problem["walls"] = set()
        self.problem['start'] = {"pos": None, "color": "#FF5733"}
        self.problem['end'] = {"pos": None, "color": "#3F33FF"}
        window.delete("all")
    

    def getDimensions(self):
        """[return dimensions of canvas]

        Returns:
            [tuple]: [canvas dimensions]
        """
        return self.problem["borders"]


    def resetPathCallBack(self):
        for dot in self.output:
            window.delete(dot)
        self.output = []


    def edgeDetect(self, imgLoc):
        """[generate walls using an image file and some scipy/cv tools]

        Args:
            imgLoc ([type]): [description]
        """

        # read image file, rotate and flip to correct orientation
        img = cv.flip(ndimage.rotate(cv.imread(imgLoc, 0), 90), 0)

        # resize to match canvas dimensions
        resize = min(self.problem['borders']) / min(img.shape)

        # use uncanny edge detection to generate list of walls
        edges = cv.Canny(cv.resize(img, (0,0), fx=resize, fy=resize),100,200)
        adjust_x = int(self.problem['borders'][0] / 2) - int(edges.shape[0] / 2)
        adjust_y = int(self.problem['borders'][1] / 2) - int(edges.shape[1] / 2)

        # paint walls
        for i in range(edges.shape[0]):
            for j in range(edges.shape[1]):
                if edges[i,j] > 0:
                    color = "#476042"
                    x1, y1 = ( i - self.size ) + adjust_x, ( j - self.size ) + adjust_y
                    x2, y2 = ( i + self.size ) + adjust_x, ( j + self.size ) + adjust_y

                    self.coverSurrounding(i + adjust_x, j + adjust_y)

                    self.elems[(i + adjust_x, j + adjust_y)] = window.create_oval( x1, y1, x2, y2, fill = color, outline = color )


def placeWallsCallBack():
    window.bind( "<B1-Motion>", sandbox.paint )


def eraseWallsCallBack():
    window.bind( "<B1-Motion>", sandbox.toDelete )


def placeStartCallBack():
    window.bind( "<B1-Motion>", sandbox.placeStartMarker )


def placeEndCallBack():
    window.bind( "<B1-Motion>", sandbox.placeEndMarker )


def buildWindow():
    """[helper function for creating tkinter window elements]
    """
    placeWalls = tk.Button(master, text = "Place Walls", command = placeWallsCallBack)
    eraseWalls = tk.Button(master, text = "Erase Walls", command = eraseWallsCallBack)
    placeStart = tk.Button(master, text = "Place Start", command = placeStartCallBack)
    placeEnd = tk.Button(master, text = "Place End", command = placeEndCallBack)
    runAstar = tk.Button(master, text = "Run Algorithm", command = sandbox.runAstarCallBack)
    reset = tk.Button(master, text = "Reset Window", command = sandbox.resetCallBack)
    resetPath = tk.Button(master, text = "Reset Path and Coloring", command = sandbox.resetPathCallBack)
    imgLocInput = tk.Text(master, width=20, height=1)
    imgLocInput.insert(tk.END, "Insert Image File")
    scanImg = tk.Button(master, text = "Scan an image", command = lambda: sandbox.edgeDetect("images/" + str(imgLocInput.get(1.0, 'end').strip())))

    placeWalls.grid(row=1,column=0)
    eraseWalls.grid(row=1,column=1)
    placeStart.grid(row=1,column=2)
    placeEnd.grid(row=1,column=3)
    runAstar.grid(row=2,column=0)
    reset.grid(row=2,column=1)
    resetPath.grid(row=2,column=2)
    imgLocInput.grid(row=3,column=1)
    scanImg.grid(row=3,column=0)
        

if __name__ == "__main__":
    master = tk.Tk()
    master.title( "A* & Drawing" )

    sandbox = Sandbox(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    dim = sandbox.getDimensions()

    window = tk.Canvas(master, 
            width=dim[0], 
            height=dim[1])
    window.grid(row=0, column=0, columnspan=9)
    window.bind( "<B1-Motion>", sandbox.paint )
    master.resizable(False, False) 

    buildWindow()
    tk.mainloop()
