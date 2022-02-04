Dependencies: open-cv2, tkinter, scipy, heapq

How to run:
    - ensure dependencies are installed
    - execute command 'python sandbox.py {height} {width} {pixel size} {show visited}'
        - ex; 'python sandbox.py 600 800 10 0'

How to use:
    - place starting node: 'Place start' button
    - place end node: 'Place end' button
    - draw walls: 'Place walls' button
    - run algorithm: 'Run algorithm' button

How to read image:
    - type image file name into text box (right of 'Scan an image')
    - click 'Scan an image' button
    Hint: Draw walls blocking the start node in the maze of the aStar algorithm might find a path going around maze
    Hint: reduce pixel size parameter to reduce size of maze walls if the path is too tight