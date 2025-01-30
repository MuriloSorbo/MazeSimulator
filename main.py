import cv2
import math
import numpy as np

rotation = 0
x_pos = 0
y_pos = 0
delay = 500

walls = [
    [
        [True, False, False, False], 
        [False, True, True, False], 
        [True, False, False, False], 
        [True, True, True, False], 
        [False, False, True, False]
    ],
    [
        [True, True, False, False], 
        [True, False, True, True], 
        [False, True, True, False], 
        [False, True, False, True], 
        [False, True, False, False]
    ],
    [
        [True, True, False, True], 
        [False, False, True, False], 
        [True, True, False, True], 
        [True, False, True, True], 
        [False, False, True, True]
    ],
    [
        [False, True, False, True], 
        [True, True, False, False], 
        [True, False, True, True], 
        [False, True, True, False], 
        [False, True, False, False]
    ],
    [
        [False, False, False, True], 
        [False, True, False, True], 
        [True, False, False, False], 
        [True, True, True, True], 
        [False, False, True, True]
    ],
    [
        [True, False, False, False], 
        [True, False, True, True], 
        [False, False, True, False], 
        [True, False, False, True], 
        [False, False, True, False]
    ]
]

def draw_nav(image, center, size, rotation_angle, color=(255, 255, 255), thickness=2):
    # Define triangle points relative to center
    half_size = size / 2
    height = math.sqrt(size**2 - half_size**2)

    # Initial triangle vertices for 0-degree rotation
    points = np.array([
        [center[0], center[1] - height / 2],  # Top vertex
        [center[0] - half_size, center[1] + height / 2],  # Bottom-left vertex
        [center[0] + half_size, center[1] + height / 2]   # Bottom-right vertex
    ], dtype=np.float32)

    # Calculate rotation matrix
    rotation_matrix = cv2.getRotationMatrix2D(center, rotation_angle, 1.0)

    # Rotate points
    rotated_points = cv2.transform(np.array([points]), rotation_matrix)[0]

    # Convert to integer for drawing
    rotated_points = rotated_points.astype(np.int32)

    # Draw triangle
    cv2.polylines(image, [rotated_points], isClosed=True, color=color, thickness=thickness)

    return image

def renderMap():
    global rotation
    global x_pos
    global y_pos
    global binary_maze
    global delay

    map_gray = cv2.imread('./maze.jpg', cv2.IMREAD_GRAYSCALE)
    _, binary_maze = cv2.threshold(map_gray, 128, 255, cv2.THRESH_BINARY_INV)

    draw_nav(binary_maze, ((x_pos) * 35 + 17, 237 - ((y_pos) * 50 + 20)), 20, rotation, (255, 0, 0))
    cv2.imshow('map', binary_maze)
    cv2.waitKey(delay)

def normalizeAngle(angle):
    return (angle % 360 + 360) % 360

def rotateClockWise():
    """Rotates the robot clockwise (90deg)"""

    global rotation
    rotation -= 90
    renderMap()

def rotateCounterClockWise():
    """Rotates the robot counter clocwise (90deg)"""
    global rotation
    rotation += 90
    renderMap()

def moveForward():
    """Move the robot one step front"""

    global x_pos
    global y_pos
    global rotation

    norm_angle = normalizeAngle(rotation)

    if (wallFront()):
        print('Shocked')
        exit()

    match norm_angle:
        case 0:
            y_pos += 1
        case 90:
            x_pos -= 1
        case 180:
            y_pos -= 1
        case 270:
            x_pos += 1

    renderMap()

def moveBackward():
    """Move the robot one step back"""

    global x_pos
    global y_pos
    global rotation

    norm_angle = normalizeAngle(rotation)

    if (wallBack()):
        print('Shocked')
        exit()

    match norm_angle:
        case 0:
            y_pos -= 1
        case 90:
            x_pos += 1
        case 180:
            y_pos += 1
        case 270:
            x_pos -= 1

    renderMap()

def wallFront():
    """Returns True if there is a wall in the front of the robot"""

    global x_pos, y_pos, rotation, walls
    norm_angle = normalizeAngle(rotation)

    if norm_angle == 0:     
        return not walls[x_pos][y_pos][0]
    elif norm_angle == 270:  
        return not walls[x_pos][y_pos][1]
    elif norm_angle == 180: # Esquerda
        return not walls[x_pos][y_pos][2]
    elif norm_angle == 90: # Baixo
        return not walls[x_pos][y_pos][3]

def wallBack():
    """Returns True if there is a wall in the back of the robot"""

    global x_pos, y_pos, rotation, walls
    norm_angle = normalizeAngle(rotation)

    if norm_angle == 0:     
        return not walls[x_pos][y_pos][2]
    elif norm_angle == 270:  
        return not walls[x_pos][y_pos][3]
    elif norm_angle == 180: # Esquerda
        return not walls[x_pos][y_pos][0]
    elif norm_angle == 90: # Baixo
        return not walls[x_pos][y_pos][1]

def wallLeft():
    """Returns True if there is a wall in the left side of the robot"""

    global x_pos, y_pos, rotation, walls
    norm_angle = normalizeAngle(rotation)

    if norm_angle == 0:     
        return not walls[x_pos][y_pos][3]
    elif norm_angle == 270:  
        return not walls[x_pos][y_pos][0]
    elif norm_angle == 180: # Esquerda
        return not walls[x_pos][y_pos][1]
    elif norm_angle == 90: # Baixo
        return not walls[x_pos][y_pos][2]

def wallRight():
    """Returns True if there is a wall in the right of the robot"""


    global x_pos, y_pos, rotation, walls
    norm_angle = normalizeAngle(rotation)

    if norm_angle == 0:     
        return not walls[x_pos][y_pos][1]
    elif norm_angle == 270:  
        return not walls[x_pos][y_pos][2]
    elif norm_angle == 180: # Esquerda
        return not walls[x_pos][y_pos][3]
    elif norm_angle == 90: # Baixo
        return not walls[x_pos][y_pos][0]

renderMap()
delay = 500 # set the delay of simulation

# Execucao: ----------------------------------

while True:
    moveForward()

# --------------------------------------------
renderMap()
cv2.waitKey()

    
