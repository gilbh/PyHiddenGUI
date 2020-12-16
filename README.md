# PyInvisibleGUI
PyInvisibleGUI is a mock-up module that overrides[PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI) and [MySimpleGUI](https://github.com/salabim/MySimpleGUI). It allows you to run a GUI program in a text-only terminal or without consuming memory/cpu. Put differently, PyInvisibleGUI transparently runs a GUI app as a CLI app.

This is an ideal solution for programs that open a GUI screen for the user to set up a certain set of parameters and then execute something. With PyInvisibleGUI, the program can load a preconfigured setting of the GUI and immediately starts to execute. All output sent to Multiline Elements will appears in stdout (via `print`).

The code will run the same but without creating any GUI. You are not required to change anything in the code and you can switch back and forth between PySimppleGUI and PyInvisibleGUI seamlessly. All the Elements will contain the same values and `update()` will store new values in them.

## Usage
### Integration in your code
Instead of:
```
import pysimplegui
```
use:
```
if terminal_mode:  # some boolean flag
    import myinvisiblegui as sg
else:
    import MySimpleGUI as sg
```

### System-dependent activation
The flag `terminal_mode` can be anything. You can set it manually or make is system-dependent, such as:

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

In this example, the code autoamtically sets `terminal_mode` to True if running in Raspberry Pi, and the code will run without loading PySimpleGUI and generating costly GUI elements. (Obsiously, RPi runs GUI but you can save a lot of ram/cpu resources running GUI-less).

### Loading preconfigured settings
You would probably want to have some control over the values of the GUI.

The way to do this is with the save/load settings routines. Check out [example](https://pysimplegui.readthedocs.io/en/latest/cookbook/#recipe-save-and-load-program-settings) in the PysimpleGUI Cookbook or the [Demo.py](https://github.com/gilbh/PyInvisibleGUI/blob/main/Demo.py) file included here.


### Activating the program without GUI
In some cases, you would need to emulate clicking a button in order to activate the main routine of your program. For this, add `metadata='auto_activate'` to the Element creation, such as here:
```
sg.Button('Run', key='button_key', metadata='auto_activate')
```

PyInvisibleGUI will remember all the elements with `metadata='auto_activate'` and will send them pack as `event` values on each call to `window.read()`.

This works sequencially for multiple Elements.

That's it. Would love to get your feedback on this.
