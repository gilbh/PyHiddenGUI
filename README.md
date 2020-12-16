# PyInvisibleGUI
PyInvisibleGUI is a mock-up module that overrides[PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI) and [MySimpleGUI](https://github.com/salabim/MySimpleGUI). It allows you to run a GUI program in a text-only terminal or without consuming memory/cpu. Put differently, it transparently runs a GUI app as a CLI app.

This is an ideal solution for programs that open a GUI screen for the user to set up a certain set of parameters and then execute something accordingly. With PyInvisibleGUI, the program can load a preconfigured setting of the GUI and immediately starts to execute. All output send to Multiline Elements is sent to stdout (via `print`).

## Integration
Instead of the line --
```
import pysimplegui
```
use
```
if terminal_mode:  # boolean flag
    import myinvisiblegui as sg
else:
    import MySimpleGUI as sg
```

`terminal_mode` can be anything. You can set it manually or make is system-dependent, such as:

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

That's it! The code will run the same but without creating any GUI. All the Elements still contain the same values and `update()` will store new values in them.
