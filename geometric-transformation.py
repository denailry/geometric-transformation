from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from array import array
import numpy as np
from shader import createProgram
from shader import createShader
import thread
import math

# VERTICES PROPERTY
vertexPositions = np.array([
    0.0, 0.0, 0.0, 1.0,
    0.0, 0.0, 0.0, 1.0,
    0.0, 0.0, 0.0, 1.0,
    ],
    dtype='float32'
)
vertexDim = 4
nVertices = 3

# VERTICES PROPERTY ARG
vArg = []

# SUPPORT VARIABLE
animateTime = 1000
scale = 100
exit = False

# VARIABLE TRANSLATE
translateX = 0.0;
translateY = 0.0;
velocityX = 0.0;
velocityY = 0.0;

# VARIABLE DILATE
vertexVelocity = np.array([
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0,
    0.0, 0.0, 0.0, 0.0,
    ],
    dtype='float32'
)
tDistance = 0.0
tPos = 0

# VARIABLE ROTATE
Rvelocity = 0.0
tRad = 0.0
absis = 0.0
ordinat = 0.0
sinx = 0.0
cosx = 0.0

# VARIABLE REFLECT
vertexVelocityR = vertexVelocity[:]
Rdistance = 0.0
Rpos = 0

# VARIABLE SHEAR
vertexVelocityS = vertexVelocity[:]
Sdistance = 0.0
Spos = 0

# COMMAND QUEUE
command = []

# BLOCKING STATE
state_one = True
state_two = True
state_three = True
state_four = True
state_five = True
state_six = True

# ANY CODE BELOW ARE FRAMEWORK TO DRAW USING SHADER

strVertexShader = """
#version 330

layout(location = 0) in vec4 position;
void main()
{
   gl_Position = position;
}
"""
strFragmentShader = """
#version 330

out vec4 outputColor;
void main()
{
   outputColor = vec4(1.0f, 0.0f, 0.0f, 1.0f);
}
"""

theProgram = None
positionBufferObject = None

def initializeProgram():
    shaderList = []
    
    shaderList.append(createShader(GL_VERTEX_SHADER, strVertexShader))
    shaderList.append(createShader(GL_FRAGMENT_SHADER, strFragmentShader))
    
    global theProgram 
    theProgram = createProgram(shaderList)
    
    for shader in shaderList:
        glDeleteShader(shader)

def initializeVertexBuffer():
    global positionBufferObject
    positionBufferObject = glGenBuffers(1)
    
    glBindBuffer(GL_ARRAY_BUFFER, positionBufferObject)
    glBufferData(
        GL_ARRAY_BUFFER,
        vertexPositions,
        GL_STREAM_DRAW
    )
    glBindBuffer(GL_ARRAY_BUFFER, 0)
# END OF SHADER HANDLING

def display():
    global translateX, translateY, velocityX, velocityY, tPos, tDistance
    global tRad, absis, ordinat, sinx, cosx, Rvelocity, vertexVelocityR, Rdistance, Rpos, vertexVelocityS, Spos, Sdistance
    global vertexVelocity, vertexPositions
    global state_one, state_two, state_three, state_four, state_five, state_six

    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT)
    gluOrtho2D(-50.0, 50.0, -50.0, 50.0)

    glUseProgram(theProgram)
    
    glBegin(GL_LINES)
    glVertex2f(-50.0,0.0)
    glVertex2f(50.0,0.0)
    glVertex2f(0.0,50.0)
    glVertex2f(0.0,-50.0)
    glEnd()

    # Translate Mechanism
    if state_one == False:
        if velocityX != 0 and translateX/velocityX > 0:
            for i in range (0, nVertices):
                vertexPositions[vertexDim*i] = vertexPositions[vertexDim*i] + velocityX
            translateX = translateX - velocityX
        else:
            velocityX = 0
            state_one = True

    if state_two == False:
        if velocityY != 0 and translateY/velocityY > 0:
            for i in range (0, nVertices):
                vertexPositions[vertexDim*i + 1] = vertexPositions[vertexDim*i + 1] + velocityY
            translateY = translateY - velocityY
        else:
            velocityY = 0
            state_two = True

    # Dilate Mechanism
    if state_three == False:
        if vertexVelocity[tPos] != 0 and tDistance/vertexVelocity[tPos] > 0:
            for i in range (0, nVertices):
                for j in range (0, 2):
                    vertexPositions[vertexDim * i + j] += vertexVelocity[vertexDim * i + j]
            tDistance = tDistance - vertexVelocity[tPos]
        else:
            for i in range (0, nVertices):
                for j in range(0, 2):
                    vertexVelocity[vertexDim*i + j] = 0
            state_three = True

    # Rotate Mechanism
    if state_four == False:
        if Rvelocity != 0 and tRad/Rvelocity > 0:
            for i in range (0, nVertices):
                vertexPositions[vertexDim*i+0] = (vertexPositions[vertexDim*i + 0]-absis)*cosx - (vertexPositions[vertexDim*i +1]-ordinat)*(sinx) + absis
                vertexPositions[vertexDim*i+1] = (vertexPositions[vertexDim*i + 0]-absis)*sinx + (vertexPositions[vertexDim*i +1]-ordinat)*(cosx) + ordinat
            tRad -= Rvelocity
        else:
            state_four = True
        
    # Reflect Mechanism
    if state_five == False:
        if vertexVelocityR[Rpos] != 0 and Rdistance/vertexVelocityR[Rpos] > 0:
            for i in range (0, nVertices):
                for j in range (0, 2):
                    vertexPositions[vertexDim * i + j] += vertexVelocityR[vertexDim * i + j]
            Rdistance -= vertexVelocityR[Rpos]
        else:
            state_five = True
        
    # Shear Mechanism
    if state_six == False:
        if vertexVelocityS[Spos] != 0 and Sdistance/vertexVelocityS[Spos] > 0:
            for i in range (0, nVertices):
                for j in range (0, 2):
                    vertexPositions[vertexDim * i + j] += vertexVelocityS[vertexDim * i + j]
            Sdistance -= vertexVelocityS[Spos]
        else:
            state_six = True

    glBindBuffer(GL_ARRAY_BUFFER, positionBufferObject)
    glBufferData(
        GL_ARRAY_BUFFER,
        vertexPositions,
        GL_DYNAMIC_DRAW
    )
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, vertexDim, GL_FLOAT, GL_FALSE, 0, None)
    
    glDrawArrays(GL_POLYGON, 0, nVertices)
    
    glDisableVertexAttribArray(0)
    glUseProgram(0)
    
    glutSwapBuffers()
    glutPostRedisplay()
    
def reshape(w, h):
    glViewport(-0, -0, w, h)

def translate(x, y):
    global translateX, translateY, velocityX, velocityY, animateTime
    global vertexPositions
    global state_one, state_two, state_three, state_four, state_five, state_six

    while  (state_one == False or 
            state_two == False or 
            state_three == False or
            state_four == False or
            state_five == False or
            state_six == False):
        nothing = 1

    fx = float(x) / scale
    fy = float(y) / scale

    translateX = fx
    translateY = fy
    velocityX = fx / animateTime
    velocityY = fy / animateTime

    state_one = False
    state_two = False

def dilate(k):
    global vertexVelocity, vertexPositions, tDistance, tPos
    global state_one, state_two, state_three, state_four, state_five, state_six

    while  (state_one == False or 
            state_two == False or 
            state_three == False or
            state_four == False or
            state_five == False or
            state_six == False):
        nothing = 1

    fk = float(k)

    tDistance = 0
    tPos = 0
    for i in range (0, nVertices):
        for j in range(0, 2):
            vertexVelocity[vertexDim*i + j] = (vertexPositions[vertexDim*i + j] * fk - vertexPositions[vertexDim*i + j]) / animateTime
            tempPos = vertexDim*i + j
            tempDistance = vertexPositions[tempPos] * fk - vertexPositions[tempPos]
            if abs(tempDistance) > abs(tDistance):
                tDistance = tempDistance
                tPos = tempPos

    state_three = False

def stretch(type, k):
    global vertexVelocity, vertexPositions, tDistance, tPos
    global state_one, state_two, state_three, state_four, state_five, state_six

    while  (state_one == False or 
            state_two == False or 
            state_three == False or
            state_four == False or
            state_five == False or
            state_six == False):
        nothing = 1

    fk = float(k)

    if type == 'x':
        j = 1
    elif type == 'y':
        j = 0
    else:
        return

    tDistance = 0
    tPos = 0
    for i in range (0, nVertices):
        vertexVelocity[vertexDim*i + j] = (vertexPositions[vertexDim*i + j] * fk - vertexPositions[vertexDim*i + j]) / animateTime
        tempPos = vertexDim*i + j
        tempDistance = vertexPositions[tempPos] * fk - vertexPositions[tempPos]
        if abs(tempDistance) > abs(tDistance):
            tDistance = tempDistance
            tPos = tempPos

    state_three = False

def custom(a, b, c, d):
    global vertexVelocity, vertexPositions, tDistance, tPos
    global state_one, state_two, state_three, state_four, state_five, state_six

    while  (state_one == False or 
            state_two == False or 
            state_three == False or
            state_four == False or
            state_five == False or
            state_six == False):
        nothing = 1

    fa = float(a)
    fb = float(b)
    fc = float(c)
    fd = float(d)

    tDistance = 0.0
    tPos = 0
    for i in range (0, nVertices):
        t1 = custom_transform(
            vertexPositions[vertexDim * i],
            vertexPositions[vertexDim * i + 1],
            fa, fb)
        t2 = custom_transform(
            vertexPositions[vertexDim * i],
            vertexPositions[vertexDim * i + 1],
            fc, fd)
        vertexVelocity[vertexDim*i] = (t1 - vertexPositions[vertexDim * i]) / animateTime
        vertexVelocity[vertexDim*i + 1] = (t2 - vertexPositions[vertexDim * i + 1]) / animateTime
        if abs(vertexVelocity[vertexDim*i]) > abs(vertexVelocity[vertexDim*i + 1]):
            tempPos = vertexDim * i
            tempDistance = t1 - vertexPositions[vertexDim * i]
        else:
            tempPos = vertexDim * i + 1
            tempDistance = t2 - vertexPositions[vertexDim * i + 1]
        if abs(tempDistance) > abs(tDistance):
            tDistance = tempDistance
            tPos = tempPos

    state_three = False

def custom_transform(x, y, ta, tb):
    return (x * ta) + (y * tb)

def rotate (deg,a,b):
    global Rvelocity, vertexPositions, tRad, sinx, cosx, absis, ordinat
    global state_one, state_two, state_three, state_four, state_five, state_six

    while  (state_one == False or 
            state_two == False or 
            state_three == False or
            state_four == False or
            state_five == False or
            state_six == False):
        nothing = 1

    absis = float(a)/10
    ordinat = float(b)/10
    deg = float(deg)
    tRad = math.radians(deg)
    tCurve = 0
    
    if (deg != 0):
        Rvelocity = tRad / animateTime / (abs(deg)/90)
    else:
        Rvelocity = tRad / animateTime
    sinx = math.sin(Rvelocity)
    cosx = math.cos(Rvelocity)

    state_four = False
    
def reflect1 (param):
    global vertexPositions, vertexVelocityR, Rdistance, Rpos, state_five
    global state_one, state_two, state_three, state_four, state_five, state_six

    while  (state_one == False or 
            state_two == False or 
            state_three == False or
            state_four == False or
            state_five == False or
            state_six == False):
        nothing = 1

    Rpos = 0
    Rdistance = 0.0
    
    if param == "x":
        for i in range (0, nVertices):
            vertexVelocityR[vertexDim*i + 0] = 0
            vertexVelocityR[vertexDim*i + 1] = (vertexPositions[vertexDim*i + 1]*(-1) - vertexPositions[vertexDim*i + 1]) / animateTime
            tempPos = [vertexDim*i + 1]
            tempDistance = vertexPositions[vertexDim*i + 1]*(-1) - vertexPositions[vertexDim*i + 1]
            if abs(tempDistance) > abs(Rdistance):
                Rpos = tempPos
                Rdistance = tempDistance
    elif param == "y":
        for i in range (0, nVertices):
            vertexVelocityR[vertexDim*i + 0] = (vertexPositions[vertexDim*i + 0]*(-1) - vertexPositions[vertexDim*i + 0]) / animateTime
            vertexVelocityR[vertexDim*i + 1] = 0
            tempPos = [vertexDim*i + 0]
            tempDistance = vertexPositions[vertexDim*i + 0]*(-1) - vertexPositions[vertexDim*i + 0]
            if abs(tempDistance) > abs(Rdistance):
                Rpos = tempPos
                Rdistance = tempDistance    
    elif param == "y=x":
        for i in range (0, nVertices):
            for j in range (0, 2):
                vertexVelocityR[vertexDim*i + j] = (vertexPositions[vertexDim*i + (1-j)] - vertexPositions[vertexDim*i + j]) / animateTime
                tempPos = [vertexDim*i + j]
                tempDistance = vertexPositions[vertexDim*i + (1-j)] - vertexPositions[vertexDim*i + j]
                if abs(tempDistance) > abs(Rdistance):
                    Rpos = tempPos
                    Rdistance = tempDistance
    elif param == "y=-x":
        for i in range (0, nVertices):
            for j in range (0, 2):
                vertexVelocityR[vertexDim*i + j] = (vertexPositions[vertexDim*i + (1-j)]*(-1) - vertexPositions[vertexDim*i + j]) / animateTime
                tempPos = [vertexDim*i + j]
                tempDistance = vertexPositions[vertexDim*i + (1-j)]*(-1) - vertexPositions[vertexDim*i + j]
                if abs(tempDistance) > abs(Rdistance):
                    Rpos = tempPos
                    Rdistance = tempDistance

    state_five = False
                                    
def reflect2 (a,b):
    global vertexPositions, vertexVelocityR, Rdistance, Rpos, state_five
    global state_one, state_two, state_three, state_four, state_five, state_six

    while  (state_one == False or 
            state_two == False or 
            state_three == False or
            state_four == False or
            state_five == False or
            state_six == False):
        nothing = 1

    Rpos = 0
    Rdistance = 0.0
    const = [float(a)/scale, float(b)/scale]
    for i in range (0, nVertices):
        for j in range (0, 2):
            vertexVelocityR[vertexDim*i + j] = ((2*const[j % 2] - vertexPositions[vertexDim*i + j]) - vertexPositions[vertexDim*i + j]) / animateTime
            tempPos = [vertexDim*i + j]
            tempDistance = (2*const[j % 2] - vertexPositions[vertexDim*i + j]) - vertexPositions[vertexDim*i + j]
            if abs(tempDistance) > abs(Rdistance):
                Rpos = tempPos
                Rdistance = tempDistance

    state_five = False

def shear(param,k):
    global vertexPositions, vertexVelocityS, Spos, Sdistance
    global state_one, state_two, state_three, state_four, state_five, state_six

    while  (state_one == False or 
            state_two == False or 
            state_three == False or
            state_four == False or
            state_five == False or
            state_six == False):
        nothing = 1

    Spos = 0
    Sdistance = 0.0
    const = float(k)
    
    if param == "x":
        for i in range (0, nVertices):
            vertexVelocityS[vertexDim*i + 0] = vertexPositions[vertexDim*i + 1]*const / animateTime
            vertexVelocityS[vertexDim*i + 1] = 0
            tempPos = [vertexDim*i + 0]
            tempDistance = vertexPositions[vertexDim*i + 1]*const
            if abs(tempDistance) > abs(Sdistance):
                Spos = tempPos
                Sdistance = tempDistance    
    elif param == "y":
        for i in range (0, nVertices):
            vertexVelocityS[vertexDim*i + 0] = 0
            vertexVelocityS[vertexDim*i + 1] = vertexPositions[vertexDim*i + 0]*const / animateTime
            tempPos = [vertexDim*i + 1]
            tempDistance = vertexPositions[vertexDim*i + 0]*const
            if abs(tempDistance) > abs(Sdistance):
                Spos = tempPos
                Sdistance = tempDistance    

    state_six = False

def from_user():
    global command

    start()

    while exit == False:
        arg = raw_input().split()
        if arg[0] == "multiple":
            for i in range (0, int(arg[1])):
                command.insert(i, raw_input())
            while len(command) > 0:
                exec_cmd(command.pop(0).split())
        else:
            exec_cmd(arg)

def exec_cmd(arg):
    global exit
    try:
        if arg[0] == "translate":
            translate(arg[1], arg[2])
        elif arg[0] == "dilate":
            dilate(arg[1])
        elif arg[0] == "stretch":
            stretch(arg[1], arg[2])
        elif arg[0] == "custom":
            custom(arg[1], arg[2], arg[3], arg[4])
        elif arg[0] == "reset":
            start(vArg)
        elif arg[0] == "rotate":
            rotate(arg[1], arg[2], arg[3])
        elif arg[0] == "reflect":
            if arg[1] == "x" or arg[1] == "y" or arg[1] == "y=x" or arg[1] == "y=-x":
                reflect1(arg[1])
            else:
                point = []
                list(arg[1])
                point += arg[1]
                point.remove('(')
                point.remove(')')
                temp1 = "".join(point)
                temp2 = temp1.split(',')
                list (temp2)
                reflect2(temp2[0],temp2[1])
        elif arg[0] == "shear":
            shear(arg[1], arg[2])   
        elif arg[0] == "exit":
            glutLeaveMainLoop()
            exit = True
    except:
        print "Some commands are wrong"

def start(sArg = None):
    global vertexPositions, nVertices, vertexVelocity, vArg
    global vertexVelocityR, vertexVelocityS
    if sArg == None:
        arg = raw_input()
        nVertices = int(arg)
    vertices = []
    velocity = []
    i = 0
    while i < nVertices:
        if sArg == None:
            vArg.insert(i, raw_input())
        arg = vArg[i].split(',')
        try:
            x = float(arg[0]) / scale
            y = float(arg[1]) / scale
            pos = vertexDim*i;
            vertices.insert(pos, x)
            vertices.insert(pos+1, y)
            vertices.insert(pos+2, 0.0)
            vertices.insert(pos+3, 1.0)

            velocity.insert(pos, 0.0)
            velocity.insert(pos+1, 0.0)
            velocity.insert(pos+2, 0.0)
            velocity.insert(pos+3, 0.0)       

            i = i + 1
        except:
            print "Wrong Format"

    vertexPositions = np.array(vertices, dtype='float32')
    vertexVelocity = np.array(velocity, dtype='float32')
    vertexVelocityR = np.array(velocity, dtype='float32')
    vertexVelocityS = np.array(velocity, dtype='float32')

def main():
    width = 500;
    height = 500
    displayMode = GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH | GLUT_STENCIL;
    
    glutInit()
    glutInitDisplayMode (displayMode);
    glutInitWindowSize (width, height)
    glutInitWindowPosition (10, 10)
    window = glutCreateWindow("Tubes Algeo")

    initializeProgram()
    initializeVertexBuffer()
    glBindVertexArray(glGenVertexArrays(1))

    glutDisplayFunc(display) 
    glutReshapeFunc(reshape)
    thread.start_new_thread(from_user, ())
    glutMainLoop()

if __name__ == '__main__':
    main()
