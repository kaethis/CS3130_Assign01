import curses

import re


keyboard = { 'ENTER'  : 10,
             'ESC'    : 27,
             'BACKSP' : curses.KEY_BACKSPACE,
             'UP'     : curses.KEY_UP,
             'DOWN'   : curses.KEY_DOWN,
             'LEFT'   : curses.KEY_LEFT,
             'RIGHT'  : curses.KEY_RIGHT,
             'A'      : 0x61,
             'D'      : 0x64,
             'N'      : 0x6E,
             'S'      : 0x73,
             'Y'      : 0x79 }

regex = { 'ALNUM' : re.compile("^[A-Za-z0-9]+$"),
          'ALPHA' : re.compile("^[A-Za-z]+$"),
          'NUM'   : re.compile("^[0-9]+$") }

colors = { 'W/BK' : 1,
           'BK/W' : 2 }


stdscr = curses.initscr()

stdscr.keypad(True)


curses.noecho()

curses.cbreak()

curses.start_color()

curses.init_pair(colors['W/BK'], curses.COLOR_WHITE, curses.COLOR_BLACK)

curses.init_pair(colors['BK/W'], curses.COLOR_BLACK, curses.COLOR_WHITE)


stdscr.refresh()


def menuwin(y, x, height,focus, records, lengths, fields):

    curs_y, curs_x = y, x

    curs_height = height

    width = (len(lengths)+2)

    for l in lengths: width += (int(l)+1)


    color = curses.color_pair(colors['W/BK'])

    window(curs_y, curs_x, height, width, color, True)


    curs_y += 1;

    curs_x += 2;

    curs_height -= 2;


    return menu(curs_y, curs_x, curs_height, focus,\
                records, lengths, fields)


def menu(y, x, height, focus, records, lengths, fields):

    curs_y, curs_x = y, x

    width = 0

    for l in lengths: width += (int(l)+1)

    width += (len(lengths)-2)

    color = curses.color_pair(colors['W/BK'])

    window(curs_y, curs_x, height, width, color, False)


    pos, scroll = 0, 0

    for i in range(focus):

        if pos < (height-1): pos += 1

        else:                scroll += 1


    for i in range(len(fields)):

        stdscr.addstr((curs_y-1), curs_x, '|'+fields[i]+'|', color)

        stdscr.refresh()


        if i == 0: curs_x += 2

        curs_x += (int(lengths[i])+1)


    while True:

        curs_y, curs_x = y, x

        for i in range(height):

            if (i + scroll) == focus:

                color = curses.color_pair(colors['BK/W'])

            else:

                color = curses.color_pair(colors['W/BK'])


            curs_x = x

            for j in range(width):

                stdscr.addch(curs_y, curs_x, '_', color)

                curs_x += 1


            curs_x = x

            if not i > (len(records) - 1):

                for j in range(len(fields)):

                    field = records[(i+scroll)][j]

                    if not j == 0 or j == (len(fields)-1):

                        field = ("_|_"+field);


                    stdscr.addstr(curs_y, curs_x, field, color)

                    curs_x += (int(lengths[j])+1)


            curs_y += 1


        stdscr.refresh()


        cmd = { keyboard['ESC']   : [keyboard['ESC'], focus],
                keyboard['A']     : [keyboard['A'], focus],
                keyboard['D']     : [keyboard['D'], focus],
                keyboard['S']     : [keyboard['S'], focus] }

        while True:

            key = stdscr.getch();

            if key in cmd.keys():

                return cmd[key]

            else:

                if key == keyboard['DOWN']: 

                    if pos < (height-1): pos += 1

                    else:                scroll += 1


                    if focus < (len(records)-1):

                        focus += 1

                    else:

                        focus, pos, scroll = 0, 0, 0


                    break;

                elif key == keyboard['UP'] and not len(records) == 0:

                    if pos > 0: pos -= 1

                    else:       scroll -= 1


                    if focus == 0:

                        focus = (len(records)-1)


                        if len(records) > (height-1):

                            pos = (height-1)

                        else:

                            pos = (len(records)-1)


                        scroll = focus - pos

                    else:

                        focus -= 1


                    break;


def ask(y, x, typechs, lengths, fields):

    curs_y, curs_x = y, x 


    buffer = []

    for i in range(len(fields)):

        curs_y, curs_x = y, x

        field = ''

        field = textwin(curs_y, curs_x,\
                        typechs[i], int(lengths[i]), fields[i])


        if field == keyboard['ESC']: return keyboard['ESC']

        else:                        buffer.append(field)
        

    return buffer;


def confirm(y, x, msg):

    msg += '  '

    choices = ['YES', 'NO']


    curs_y, curs_x = y, x

    height, width = 1, (len(msg)+1)

    for choice in choices: width += len(choice)


    color = curses.color_pair(colors['BK/W'])

    stdscr.addstr(curs_y, curs_x, msg, color)

    window(curs_y, curs_x, height, width, color, False)


    toggle = lambda x: x^1


    focus = 0

    while True:

        curs_x = (x+width-1)

        for choice in choices: curs_x -= len(choice)


        for i in range(len(choices)):
 
            if focus == i: color = curses.color_pair(colors['W/BK'])

            else:          color = curses.color_pair(colors['BK/W'])


            stdscr.addstr(curs_y, curs_x, choices[i], color)

            if not i == (len(choices)-1):

                curs_x += len(choices[i])

                color = curses.color_pair(colors['BK/W'])

                stdscr.addch(curs_y, curs_x, '/', color)

                curs_x += 1


        stdscr.refresh()


        cmd = { keyboard['ESC']   :    -1,
                keyboard['N']     :     1,
                keyboard['Y']     :     0,
                keyboard['ENTER'] : focus }

        ctrl = { keyboard['LEFT']  : toggle,
                 keyboard['RIGHT'] : toggle }

        while True:

            key = stdscr.getch();

            if key in cmd.keys():

                clear(y, x, height, width)

                return cmd[key]

            elif key in ctrl.keys():

                focus = ctrl[key](focus)

                break


def textwin(y, x, typech, length, field):

    curs_y, curs_x = y, x

    height, width = 3, ((length+1)+4)

    color = curses.color_pair(colors['W/BK'])

    window(curs_y, curs_x, height, width, color, True)


    height, width = 1, (length+1)

    curs_y, curs_x = (y+1), (x+2)


    buffer = textbox(curs_y, curs_x, height, width,\
                     typech, length, field)


    height, width = 3, ((length+1)+4)

    clear(y, x, height, width)


    return buffer


def textbox(y, x, height, width, typech, length, field):

    curs_y, curs_x = y, x

    stdscr.addstr((curs_y-1), curs_x, '|'+field+'|')

    color = curses.color_pair(colors['W/BK'])

    window(curs_y, curs_x, height, width, color, False)


    stdscr.move(curs_y, curs_x)

    stdscr.refresh();


    return input(curs_y, curs_x, typech, length)


def window(y, x, height, width, color, is_drop):

    if is_drop:

        drop = curses.color_pair(colors['BK/W'])

        shadow(y, x, height, width, drop)


    win = curses.newwin((height+2), (width+2), (y-1), (x-1))

    win.bkgd(color)

    win.box(0, 0)

    win.refresh()


    stdscr.refresh()


def shadow(y, x, height, width, color):

    curs_y, curs_x = y, (x+width+1)
 
    for i in range(height+1):

        stdscr.addch(curs_y, curs_x, ' ', color)

        curs_y += 1


    curs_y, curs_x = (y+height+1), x

    for i in range(width+2):

        stdscr.addch(curs_y, curs_x, ' ', color)

        curs_x += 1


def clear(y, x, height, width):

    clr = curses.newwin((height+3), (width+3), (y-1), (x-1))

    color = curses.color_pair(colors['W/BK'])

    clr.bkgd(color)

    clr.refresh()


    stdscr.refresh()


def input(y, x, typech, length):

    curs_y, curs_x = y, x


    buffer = ''

    while True:

        key = stdscr.getch();

        if key == keyboard['ESC']:

            return key

        elif key == keyboard['ENTER'] and not len(buffer) == 0:

            return buffer 

        elif key == keyboard['BACKSP'] and len(buffer) > 0:

            ret = backsp(curs_y, curs_x, buffer)

            if not ret == -1:

                buffer = ret
   
                curs_x -= 1

        elif regex['ALNUM'].match(chr(key)) and len(buffer) < length:

            ret = addchr(curs_y, curs_x, typech, chr(key), buffer)

            if not ret == -1:

                buffer = ret

                curs_x += 1


def backsp(y, x, buffer):

    if len(buffer) == 0:

        return -1

    else:

        x -= 1

        stdscr.move(y, x)
 
        stdscr.addch(' ')

        stdscr.move(y, x)

        stdscr.refresh()


        return buffer[:-1]


def addchr(y, x, typech, ch, buffer):

    if not regex[typech].match(ch):

        return -1

    else:

        stdscr.addch(ch.upper())

        x += 1

        stdscr.move(y, x)

        stdscr.refresh();

        
        return (buffer + ch.upper())


def exitui():

    stdscr.keypad(True)


    curses.echo()

    curses.endwin()
