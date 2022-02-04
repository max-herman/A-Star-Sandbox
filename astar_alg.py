import math
import heapq

def euclidien(problem, node):
    """Compute euclidien distance from current position to end goal

    Args:
        problem ([dict]): [contains relevant positional information]
        node ([tuple]): [current position]

    Returns:
        [float]: [distance from current position to end]
    """
    return math.sqrt((problem["end"]["pos"][0] - node[0])**2 + (problem["end"]["pos"][1] - node[1])**2)


def manhattan(problem, node):
    """Compute manhattan distance from current position to end goal 

    Args:
        problem ([dict]): [contains relevant positional information]
        node ([tuple]): [current position]

    Returns:
        [float]: [distance from current position to end]
    """
    return abs(problem["end"]["pos"][0] - node[0]) + abs(problem["end"]["pos"][1] - node[1])


def inBounds(border, p):
    """check if successor is within bounds

    Args:
        border ([tuple]): [width or height of screen]
        p ([int]): [x or y position]

    Returns:
        [bool]: [true if in bounds]
    """
    return p > 0 and p < border


def isGoal(node, end, size):
    """Check if current grouping of pixels contains the goal node

    Args:
        node ([tuple]): [current position]
        end ([tuple]): [goal node]
        size ([int]): [range of pixels]

    Returns:
        [bool]: [true if goal node is present]
    """
    if node[0] > end[0] - size and node[0] < end[0] + size:
        if node[1] > end[1] - size and node[1] < end[1] + size:
            return True
    
    return False


def getSuccessors(problem, node, size, dir4):
    """generate list of possible next steps from current position

    Args:
        problem ([dict]): [contains relevant board information]
        node ([tuple]): [current position]
        size ([int]): [size of 'pixel']
        dir4 ([bool]): [if 4, move north/east/south/west, if 8, move n/ne/e/...]

    Returns:
        [list]: [list of next nodes to check]
    """
    successors = []

    # 4-directional
    if dir4:
        for i in [-1 * size, size]:
            if (node[0] + i, node[1]) not in problem["walls"] and inBounds(problem["borders"][0], node[0] + i):
                successors.append((node[0] + i, node[1]))
            
            if (node[0], node[1] + i) not in problem["walls"] and inBounds(problem["borders"][1], node[1] + i):
                successors.append((node[0], node[1] + i))

    # 8-directional
    else:
        for i in [-1 * size, size]:
            for j in [-1 * size, size]:
                if (node[0] + i, node[1] + j) not in problem["walls"] and inBounds(problem["borders"][0], node[0] + i) and inBounds(problem["borders"][1], node[1] + j): 
                    successors.append((node[0] + i, node[1] + j))

    return successors


def generateRGB(rgb):
    """create hex value from rgb tuple

    Args:
        rgb ([tuple]): [rgb values]

    Returns:
        [f-string]: [rgb hex string]
    """
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'


def updateScan(node, count, master, w, size):
    """Change color of pixels based on how many times they were visited

    Args:
        node ([tuple]): [current position]
        count ([int]): [how many times visited]
        master ([TK]): [tkinter screen manager]
        w ([Canvas]): [tkinter canvas]
        size ([int]): ['pixel' size]

    Returns:
        [oval]: [tkinter object]
    """
    baseColor = generateRGB((170 , 255 - 20 * count, 241))
    x1, y1 = ( node[0] - size ), ( node[1] - size )
    x2, y2 = ( node[0] + size ), ( node[1] + size )
    dot = w.create_oval( x1, y1, x2, y2, fill = baseColor, outline = baseColor )

    # needed to refresh screen
    # read tkinter documentation to manage canvas changes properly
    master.update_idletasks()
    master.update()

    return dot
    

def aStarSearch(problem, master, w, size, show, dir4=True):
    """aStar algorithm: find shortest path from current node to goal node using a hueristic

    Args:
        problem ([dict]): [relevant board information]
        master ([Tkinter]): [tkinter manager]
        w ([canvas]): [tkinter canvas]
        size ([int]): ['pixel' size]
        show ([bool]): [change color of visited nodes]
        dir4 (bool, optional): [what directions can be moved to]. Defaults to True.

    Returns:
        [tuple]: [return list of visited nodes (path to goal)]
    """
    queue = []
    visited = []
    count = 0
    visitedDots = []
    vCount = dict()

    # set start for algorithm
    start = (problem["start"]["pos"], 0, [])
    heapq.heappush(queue, (0, count, start))
    vCount[problem["start"]["pos"]] = 0

    # check every node in queue
    while not len(queue) == 0:
        node, cost, path = heapq.heappop(queue)[2]

        if show:
            vCount[node] += 1
            visitedDots.append(updateScan(node, vCount[node], master, w, size))

        # end condition: goal found
        if isGoal(node, problem["end"]["pos"], size):
            return path, visitedDots

        elif node not in visited:
            fringe = getSuccessors(problem, node, size, dir4)
            
            # push each node to queue
            for fNode in fringe:

                if fNode not in visited:
                    newCost = cost + 1
                    data = (fNode, newCost, path + [fNode])
                    heapq.heappush(queue, (newCost + manhattan(problem, fNode), count, data))
                    vCount[fNode] = 0
            visited.append(node)
    
    return None, visitedDots
