"""
Package for the bintree-gui example

!NOTE! I am aware that:
    1. all files except 'bintree-gui.py' use German for variable & method names, etc.;
    2. the implementaion of the AVL-tree (avlbaum.py),
    as well as the tests (test.py & test_avlbaum.py) are incomplete and/or faulty;
    3. the gui is mostly done in pure pygame
    (the visualisation of the tree is done without the use of any widgets).

    Keeping this in mind, the intention of this example
    is the flawless incoorporation of PyGVisuals into a pygame-Application/Program.
    You can test out the gui by executing 'bintree-gui.py'.
    ## You can execute the following to start the program from outside (!) the package:
    __import__("pygvisuals.examples.bintree-gui.bintree-gui").main_loop() ##
    You can find the code for incorporating PyGVisuals' widgets in the sourcecode of 'bintree-gui.py'
    in the section 'Widgets' and in the mainloop (section: 'Functions', method: 'main_loop')
"""
