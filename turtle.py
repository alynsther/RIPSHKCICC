import turtle
turtle.reset()
turtle.pensize(4)

print('Welcome to the Python sketchbook!')

##### While loop to repeat the main menu

# Initialize the option to empty in order to enter the while loop
option = ''

while option != 'q': # While the option is not 'q'
    print()
    print('Please choose one of the following options:')
    print()
    print('m - Move the turtle')
    print('t - Rotate the turtle')
    print('l - Draw a line')
    print('r - Draw a rectangle')
    print('c - Draw a circle')
    print('p - Change the pen colour of the turtle')
    print('f - Change the fill colour of the turtle')
    print('s - Change the speed pf the turtle')
    print('q - Quit the program')
    print()

    option = input('Please input your option: ')

    ##### Handle the move option
    if option == 'm':
        print()

        # Ask the user for the x and y location
        x = input('Please enter the x location: ')
        x = int(x)
        y = input('Please enter the y location: ')
        y = int(y)

        # Move the turtle without drawing anything
        turtle.up()
        turtle.goto(x, y)
        turtle.down()

    ##### Handle the rotate option
    if option == 't':
        print()

        #
        angle=int(input('Please enter the angle you want to turn: '))
        turtle.left(angle)
        #

    ##### Handle the line option
    if option == 'l':
        print()

        # Ask the user for the x and y location
        x = input('Please enter the x location: ')
        x = int(x)
        y = input('Please enter the y location: ')
        y = int(y)

        # Move the turtle and draw a line
        turtle.goto(x, y)

    ##### Handle the rectangle option
    if option == 'r':
        print()

        #
        w=int(input('Please enter the width: '))
        l=int(input('Please enter the lenth: '))
        turtle.begin_fill()
        turtle.forward(l)
        turtle.right(90)
        turtle.forward(w)
        turtle.right(90)
        turtle.forward(l)
        turtle.right(90)
        turtle.forward(w)
        turtle.right(90)
        turtle.end_fill()
        #

    ##### Handle the circle option
    if option == 'c':
        print()

        #
        turtle.begin_fill()
        r=int(input('Please enter the radius: '))
        d=int(input('Please enter the degree that you want to draw: '))
        turtle.circle(r,d)
        turtle.end_fill()
        #

    ##### Handle the pen colour option
    if option == 'p':
        print()

        #
        color_p=input('Please enter the pencolor that you want: ')
        turtle.pencolor(color_p)
        #

    ##### Handle the fill colour option
    if option == 'f':
        print()

        #
        color_f=input('Please enter the fillcolor that you want: ')
        turtle.fillcolor(color_f)
        #
    #### Handle the speed option
    if option == 's':

        speed=int(input('Please enter the speed that you want: '))
        turtle.speed(speed)
        
turtle.done()
