import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

#-------------------------Bezier-------------------------
# Define Control Point
x = np.array([[-0.5, -2, 0],
              [1, 1, 1],
              [2, 2 ,2]])

y = np.array([[2, 1, 0],
              [2, 1, 0],
              [2, 1 ,0]])

z = np.array([[1, -1, 2],
              [0, 3, 3],
              [0, 1, 2]])

# Number of Cells for Each Direction
uCELLS = 100
wCELLS = 100

# Total Number of Control Point in U and W
uPTS = np.size(x, 0)
wPTS = np.size(x, 1)

#Total Number of Subdivision
n = uPTS - 1
m = wPTS - 1

# Parametric Variable
u = np.linspace(0, 1, uCELLS)
w = np.linspace(0, 1, wCELLS)

# Instalizaed Empty Matrix for x, y, z
xBezier = np.zeros((uCELLS, wCELLS))
yBezier = np.zeros((uCELLS, wCELLS))
zBezier = np.zeros((uCELLS, wCELLS))

# Binomial Cofficients
def Ni(n, i):
    return np.math.factorial(n) / (np.math.factorial(i) * np.math.factorial(n - i))

def Mj(m, j):
    return np.math.factorial(m) / (np.math.factorial(j) * np.math.factorial(m - j))

# Bernstein Basic Polynomial
def J(n, i, u):
    return np.matrix(Ni(n, i) * (u ** i) * (1 - u) ** (n - i))

def K(m, j, w):
    return np.matrix(Mj(m, j) * (u ** j) * (1 - w) ** (m - j))

#   **************
#   *            *
#   *            *
#   *            *
#   *            *
#   **************

# Main Loop for calculate surface bezier point
for i in range(0, uPTS):
    for j in range(0, wPTS):
        # Transpose J array
        Jt = J(n, i, u).transpose()
        # Bezier Curve Calculation
        xBezier = Jt * K(m, j, w) * x[i, j] + xBezier
        yBezier = Jt * K(m, j, w) * y[i, j] + yBezier
        zBezier = Jt * K(m, j, w) * z[i, j] + zBezier

#--------------------------------------------------------------------
# Rotation angles
angle_x = 0.0
angle_y = 0.0
angle_z = 45.0

# position mouse
last_xpos = 0.0
last_ypos = 0.0

rotate = False
# Initial zoom level
zoom = 1.

# Function to initialize OpenGL settings
def initialize():
    glEnable(GL_DEPTH_TEST)

# Function to handle window resize
def resize(window, width, height):
    glViewport(0, 0, width, height)

# Mouse move callback function
def mouse_move_callback(window, xpos, ypos):
    global rotate, last_xpos, last_ypos, angle_x, angle_y

    if rotate:
        delta_x = xpos - last_xpos
        delta_y = ypos - last_ypos

        angle_x += delta_y * 0.3
        angle_y += delta_x * 0.3

    last_xpos, last_ypos = xpos, ypos

# Mouse button callback function
def mouse_button_callback(window, button, action, mods):
    global rotate
    if button == glfw.MOUSE_BUTTON_LEFT:
        rotate = (action == glfw.PRESS)

def scroll_callback(window, xoffset, yoffset):
    global zoom
    zoom += yoffset * 0.1  # Adjust the zoom factor based on the scroll offset

#---------------------------------------------------------------------
# Initialize GLFW
def render_bezier_surface(window):
    global angle_x, angle_y, zoom

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
 
    # Set up perspective projection
    # gluPerspective(45, 1, 1, 100)
    # glTranslatef(0, 0, -5)
    gluPerspective(45 * zoom, 1, 0.1, 10000)
    glTranslatef(0, 0, -5 / zoom)  # Adjust the translation based on the zoom factor
    
    glRotatef(angle_x, 1, 0, 0)
    glRotatef(angle_y, 0, 1, 0)
    glRotatef(angle_z, 0, 0, 1)

    # Draw axis coordinates
    glColor3f(1, 1, 1)
    glBegin(GL_LINES)

    # X-axis
    glColor(1, 0, 0)    # red
    glVertex3f(0, 0, 0)
    glVertex3f(10, 0, 0)
    # Y-axis
    glColor(0, 1, 0)    # Green
    glVertex3f(0, 0, 0)
    glVertex3f(0, 10, 0)
    # Z-axis
    glColor(0, 0, 1)    # Blue
    glVertex3f(0, 0, 0)
    glVertex3f(0, 0, 10)

    glEnd()

    # Draw the first Bezier Curve in wCTP first Row
    glColor3f(1, 0.5, 0)    #Organ
    glBegin(GL_POINTS)
    for j in range(0, wCELLS):
        # Get the Bezier surface points
        x_point = xBezier[0, j]
        y_point = yBezier[0, j]
        z_point = zBezier[0, j]
        glVertex3f(x_point, y_point, z_point)
    glEnd()

    # Draw the first Bezier Curve in uCTP in first Column
    glColor3f(1, 1, 0)
    glBegin(GL_POINTS)
    for i in range(0, uCELLS):
        # Get the Bezier surface points
        x_point = xBezier[i, 0]
        y_point = yBezier[i, 0]
        z_point = zBezier[i, 0]
        glVertex3f(x_point, y_point, z_point)
    glEnd()

    # Draw the first Bezier Curve in uCTP in first Column
    glColor3f(1, 1, 0)
    glBegin(GL_POINTS)
    for i in range(0, uCELLS):
        # Get the Bezier surface points
        x_point = xBezier[0, i]
        y_point = yBezier[0, i]
        z_point = zBezier[0, i]
        glVertex3f(x_point, y_point, z_point)
    glEnd()

    # Draw the Bezier surface
    glColor3f(1, 1, 1)
    glBegin(GL_LINES)
    for i in range(0, uCELLS):
        for j in range(0, wCELLS):
            # Get the Bezier surface points
            x_point = xBezier[i, j]
            y_point = yBezier[i, j]
            z_point = zBezier[i, j]
            glVertex3f(x_point, y_point, z_point)
            glVertex3f(x_point + 1, y_point + 1, z_point + 1)
    
    glColor3f(0.5, 0.5, 1)
    for j in range(0, wCELLS):
        for i in range(0, uCELLS):       
            # Get the Bezier surface points
            x_point = xBezier[i, j]
            y_point = yBezier[i, j]
            z_point = zBezier[i, j]
            
            glVertex3f(x_point, y_point, z_point)
    glEnd()

    # Draw control points
    glColor3f(0, 0, 1)
    glPointSize(10)
    glBegin(GL_POINTS)
    for i in range(0, uPTS):
        for j in range(0, wPTS):
            glVertex3f(x[i, j], y[i, j], z[i, j])
    # for i in range(0, uPTS):
    #     glVertex3f(x[i, 0], y[i, 0], z[i, 0])

    glEnd()
    glPointSize(5)

    # Draw red lines connecting control points
    glColor3f(1, 0, 1)
    glBegin(GL_LINES)
    for i in range(0, uPTS):
        for j in range(0, wPTS):
            # Connect to the next point in the row
            if j < wPTS - 1:
                glVertex3f(x[i, j], y[i, j], z[i, j])
                glVertex3f(x[i, j + 1], y[i, j + 1], z[i, j + 1])
            # Connect to the next point in the column
            # if i < uPTS - 1:
            #     glVertex3f(x[i, j], y[i, j], z[i, j])
            #     glVertex3f(x[i + 1, j], y[i + 1, j], z[i + 1, j])
    glEnd()

    glfw.swap_buffers(window)
    
#===============================================================
# Main function
def main():
    global rotate, last_xpos, last_ypos, angle_x, angle_y, zoom

    # Initialize GLFW
    if not glfw.init():
        return

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(800, 600, "Bezier Surface", None, None)

    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)

    # Set the callback functions
    glfw.set_window_size_callback(window, resize)
    glfw.set_cursor_pos_callback(window, mouse_move_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_scroll_callback(window, scroll_callback)

    # Initialize OpenGL settings
    initialize()

    # Main rendering loop
    while not glfw.window_should_close(window):
        # Render the Bezier surface
        render_bezier_surface(window)

        # Poll for and process events
        glfw.poll_events()

    # Terminate GLFW
    glfw.terminate()

if __name__ == "__main__":
    main()