-----------------------------------------------------------------
          _          _                         _    __  _ 
         /_\   _____(_)__ _ _ _  _ __  ___ _ _| |_ /  \/ |
        / _ \ (_-<_-< / _` | ' \| '  \/ -_) ' \  _| () | |
       /_/ \_\/__/__/_\__, |_||_|_|_|_\___|_||_\__|\__/|_|
                      |___/                               
-----------------------------------------------------------------

[AUTHOR]  Matt W. Martin, 4374851
          kaethis@tasmantis.net

[VERSION] 1.0

[PROJECT] CS3130, Assign01
          DATABASE MANAGEMENT SYSTEM

          A Python program for administering a simple database.

          The program allows the user to [D]ELETE, [S]EARCH for,
          and [A]DD a record to the database.  At any time, the
          user may CANCEL an operation or EXIT the program with
          the [ESC] key.  Use the [ARROW KEYS] to navigate the
          menu or between options (when applicable, [Y] and [N]
          also serve to confirm an operation).

[DATE]    31-Jan-2017

[ISSUED]  15-Jan-2017

[USAGE]   python3 driver.py -db filename.db

[FILES]   ./README.txt
          ./driver.py
          ./dbmgr.py
          ./ui.py
          ./employees.db
          ./courses.db

[ISSUES]  - "VERBOSENESS vs. SUBTLETY"
            As of right now, the program does not provide any
            explicit feedback when an operation is unsuccessful.
            That is, if a user searches for an ID and said ID
            does not exist in the database, the menu will stay
            selected on the current record.  Likewise, if a new
            record contains an ID that already exists, the menu
            will select the corresponding record with said ID.
            This is by all design, but it's debatable whether
            this suffices to give enough information to the user
            about the actual outcome of the operation.

          - "POST-DELETE SELECTION"
            When cancelling or performing the [D]ELETE operation,
            the menu will always select the very first record
            afterwards.  This was not by design.  Cancelling the
            [A]DD and [S]EARCH operations seem to yield the
            desired effect (namely, remaining selected on the
            record before invoking the operation), but the same
            cannot be said for [D]ELETE.  This annoying quirk
            is not detrimental, but should later be investigated.
            
[REPO]    https://github.com/kaethis/CS3130_Assign01

