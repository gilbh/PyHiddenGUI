# PyInvisibleGUI
PyInvisibleGUI is a mock-up module that overrides [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI) and [MySimpleGUI](https://github.com/salabim/MySimpleGUI).

It allows you to run a GUI program in a text-only terminal or without consuming memory/cpu. Put differently, PyInvisibleGUI transparently runs a GUI app as a CLI and GUI-less command.

This is an ideal solution for programs that open a GUI screen for the user to set up a certain set of parameters and then execute something. With PyInvisibleGUI, the program can load a preconfigured setting of the GUI and immediately start to execute. All updates to Multiline elements will appears in stdout (via `print`).

The code will run the same but without creating any GUI. You are not required to change anything in the code and you can switch back and forth between PySimppleGUI and PyInvisibleGUI seamlessly. All the elements have the same values and are retrievable using `sg['element_name'].get()` or `sg.element_name.get()`, and similarly updated with the method `update()`, just like PySimppleGUI.

## Installation
You can install PyInvisibleGUI by downloading the file [PyInvisibleGUI.py](https://github.com/gilbh/PyInvisibleGUI/blob/main/PyInvisibleGUI.py) in this repository.

## Usage
### Integration in your code
Instead of:
```
import PySimpleGUI
```
use:
```
if terminal_mode:  # some boolean flag
    import MyInvisibleGUI as sg
else:
    import MySimpleGUI as sg
```

### System-dependent activation
The flag `terminal_mode` can be set to anything. You can set it in the static code (as above) or make it system-dependent, such as here:

```
def is_raspbian():
    res = False
    if platform.lower() == 'linux':
        with open('/etc/os-release', 'r') as f:
            s = f.read()
        i = s.find('\nID=') + 4
        ii = s.find('\n', i)
        linux_sys = s[i:ii]
        res = linux_sys.lower() == 'raspbian'

    return res


terminal_mode = is_raspbian()
```

In this example, the code automatically sets `terminal_mode` to True if running in Raspberry Pi, and the code will run without *PySimpleGUI* and without generating costly GUI elements. (Obviously RPi can run GUI, but you can save a lot of ram/cpu resources running apps as GUI-less).

### Loading preconfigured settings
You would probably want to have some control over the values of the GUI.

The way to do this is with the save/load settings routines. Check out [example](https://pysimplegui.readthedocs.io/en/latest/cookbook/#recipe-save-and-load-program-settings) in the PysimpleGUI Cookbook or the [Demo.py](https://github.com/gilbh/PyInvisibleGUI/blob/main/Demo.py) file included here.


### Activating your code without GUI
In some cases, you would need to emulate clicking a button element in the window in order to activate the main routine in your program. For this, add the keyword parameter `metadata='auto_activate'` in the element creation, such as here:
```
sg.Button('Run', key='button_key', *metadata='auto_activate'*)
```

PyInvisibleGUI will remember all the elements with `metadata='auto_activate'` and will send them back as the return value of `event` on each call to `window.read()`.

This works for multiple elements in a sequence. This means that the first element created with `metadata='auto_activate'` will be returned in the first `event` call.

That's it! Would love to get any feedback you might have on this small project.
