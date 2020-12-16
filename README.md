# PyInvisibleGUI
PyInvisibleGUI is a mock-up module that overrides[PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI) and [MySimpleGUI](https://github.com/salabim/MySimpleGUI). It allows you to run a GUI program in a text-only terminal or without consuming memory/cpu. Put differnetly, it transparently runs a GUI app as a CLI app.

This is an ideal solution for programs that open a GUI screen for the user to set up a certain set of parameters and then execute something accordingly. With PyInvisibleGUI, the program can load a preconfigured setting of the GUI and immediately starts to execute. All output send to Multiline Elements is sent to stdout (via `print`).
