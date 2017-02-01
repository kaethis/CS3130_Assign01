#!/usr/bin/env python3

import sys

import dbmgr

import ui


filename = ''

ret = [0, 0]

focus = ret[0]


def add():

    global ret

    global focus


    y, x = 18, 2 

    record = ui.ask(y, x,\
                    dbmgr.typechs, dbmgr.lengths, dbmgr.fields)


    if not record == ui.keyboard['ESC']:

        y, x = 19, 3

        if ui.confirm(y, x, 'ADD?') == 0:

            focus = dbmgr.add(record)

            if focus == -1: focus = dbmgr.search(record[0])

    else:

        focus = ret[1] 


def delete():

    global ret

    global focus


    if not len(dbmgr.records) == 0:

        y, x = 19, 3

        if ui.confirm(y, x, 'DELETE?') == 0:

            dbmgr.remove(dbmgr.records[ret[1]][0])

            if not focus == 0: focus -= 1

        else:

            focus = 0


def search():

    global ret

    global focus


    if not len(dbmgr.records) == 0:

        y, x = 18, 2

        typech = dbmgr.typechs[0]

        length = dbmgr.lengths[0]

        field = dbmgr.fields[0]

        search = ui.textwin(y, x, typech, int(length), field)


        if not search == ui.keyboard['ESC']: 

            index = dbmgr.search(search)

            if not index == -1: focus = index

            else:               focus = ret[1]

        else:

            focus = ret[1]


def exit():

    global filename


    y, x = 19, 3

    if ui.confirm(y, x, 'SAVE?') == 0: dbmgr.save(filename)


    ui.exitui();

    quit();


def main(argv):

    global filename

    global ret

    global focus


    if not len(argv) == 3:

        ui.exitui();


        print("[ERROR] INVALID SYNTAX!")

        print("[USAGE] "+argv[0]+" -db "+"filename.db\n")
        

        quit();


    filename = argv[2]

    if dbmgr.load(filename) == -1:

        ui.exitui();


        print("[ERROR] "+filename+" NOT FOUND!\n");

        quit();


    cmd = { ui.keyboard['A']   : add,
            ui.keyboard['D']   : delete,
            ui.keyboard['S']   : search,
            ui.keyboard['ESC'] : exit }

    while True:

        y, x = 1, 2

        height = 14

        ret = ui.menuwin(y, x, height, focus,\
                         dbmgr.records, dbmgr.lengths, dbmgr.fields,)


        if ret[0] in cmd.keys(): cmd[ret[0]]();

      
if __name__ == '__main__': main(sys.argv);
