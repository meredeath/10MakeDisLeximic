import mdl
from display import *
from matrix import *
from draw import *
import math

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)

    if p:
        (commands, symbols) = p
    else:
        print("Parsing failed.")
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 100
    consts = ''
    coords = []
    coords1 = []
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'

    print(symbols)
    for command in commands:
        print(command)

        op = command["op"]
        args = command["args"]
        m = []
        
        #pop and push
        if op == "pop":
            stack.pop()
        if op == "push":
            stack.append([x[:] for x in stack[-1]])

        #transformations
        if op == "move":
            m = make_translate(args[0], args[1], args[2])
            matrix_mult(stack[-1], m)
            stack[-1] = [x[:] for x in m]
            m = []
        if op == "scale":
            m = make_scale(args[0], args[1], args[2])
            matrix_mult(stack[-1], m)
            stack[-1] = [x[:] for x in m]
            m = []
        if op == "rotate":
            angle = args[1]*(math.pi/180)
            if args[0] == "x":
                m = make_rotX(angle)
            if args[0] == "y":
                m = make_rotY(angle)
            if args[0] == "z":
                m = make_rotZ(angle)
            matrix_mult(stack[-1],m)
            stack[-1] = [x[:] for x in m]
            m = []

        #line
        if op == 'line':
            add_edge(m, args[0], args[1], args[2], args[3], args[4], args[5])
            matrix_mult(stack[-1], m)
            draw_lines(m, screen, zbuffer, [155,155,155])
            m = []
            
        #3d shapes
        if op == "box":
            add_box(m, args[0], args[1], args[2], args[3], args[4], args[5])
            matrix_mult(stack[-1], m)
            if(command['constants']):
                reflect = command['constants']
            draw_polygons(m, screen, zbuffer, view, ambient, light, symbols, reflect)
        if op == 'sphere':
            add_sphere(m,args[0], args[1], args[2], args[3], step_3d)
            matrix_mult(stack[-1], m)
            if (command['constants']):
                reflect = command['constants']
            draw_polygons(m, screen, zbuffer, view, ambient, light, symbols, reflect)
        if op == 'torus':
            add_torus(m,args[0], args[1], args[2], args[3], args[4], step_3d)
            matrix_mult(stack[-1], m)
            if (command['constants']):
                reflect = command['constants']
            draw_polygons(m, screen, zbuffer, view, ambient, light, symbols, reflect)

        #save and display
        if op == 'save':
            newname = args[0] + ".png"
            save_extension(screen, newname)
            screen = new_screen()
            zbuffer = new_zbuffer()
        if op == 'display':
            display(screen)
