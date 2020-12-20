# PySimpleNoGUI
**PySimpleNoGUI** is a mock-up module that overrides [PySimpleGUI](https://github.com/PySimpleGUI/PySimpleGUI) and [MySimpleGUI](https://github.com/salabim/MySimpleGUI).

**PySimpleNoGUI** transparently runs a GUI app built with **PySimpleGUI** as a CLI program, without creating any graphical elements on the screen. It allows you to run a GUI program in a text-only terminal and without consuming memory/cpu. 

Since **PySimpleNoGUI** overrides all required variables and functions, there is **no need to install any GUI library on the running platform** (no need to install **PySimpleGUI**, Tkinter, PyQt, etc.).

This is an ideal solution for programs that open a GUI screen for the user to set up a certain set of parameters and then execute something. With **PySimpleNoGUI**, the program can load a preconfigured setting of the GUI and immediately start the execution. All updates to Multiline elements will appears in stdout (via `print`).

The code will run the same but without creating any GUI. You are not required to change anything in the code and you can switch back and forth between **PySimpleGUI** and **PySimpleNoGUI** seamlessly. All the elements have the same values and are retrievable using `sg['element_name'].get()` or `sg.element_name.get()`, and similarly updated with the method `update()`, just like you do with **PySimpleGUI** and **MySimpleGUI**.

## Installation
You can install **PySimpleNoGUI** by downloading the file [PySimpleNoGUI.py](https://github.com/gilbh/PySimpleNoGUI/blob/main/PySimpleNoGUI.py) from this repository.

## Usage
### Integration in your code
Instead of:
```
import PySimpleGUI
```
use:
```
if terminal_mode:  # some boolean flag
    import PySimpleNoGUI as sg
else:
    import PySimpleGUI as sg
```
(**PySimpleNoGUI** works also with `import MySimpleGUI as sg`).

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

In this example, the code automatically sets `terminal_mode` to True if running in Raspberry Pi, and the code will run without **PySimpleGUI** and without generating costly GUI elements. (Obviously RPi can run GUI, but you can save a lot of ram/cpu resources by running apps as GUI-less. It will also run on a RPi Lite without any GUI libraries installed).

### Loading preconfigured settings
You would probably want to have some control over the values of the GUI.

The way to do this is with the save/load settings routines. Check out [example](https://pysimplegui.readthedocs.io/en/latest/cookbook/#recipe-save-and-load-program-settings) in the **PySimpleGUI Cookbook** or the [Demo.py](https://github.com/gilbh/PySimpleNoGUI/blob/main/Demo.py) file included here.


### Activating your code without GUI
In some cases, you would need to emulate clicking a button element in the window in order to activate the main routine in your program. For this, add the keyword parameter `metadata='auto_activate'` in the element creation, such as here:
<pre>
sg.Button('Run', key='button_key', <i>metadata='auto_activate'</i>)
</pre>

**PySimpleNoGUI** will remember all the elements with `metadata='auto_activate'` and will send them back as the return value of `event` on each call to `window.read()`.

This works for multiple elements in a sequence. This means that the first element created with `metadata='auto_activate'` will be returned in the first `event` call.

## To Do
Right now the constants used in Tkinter and PySimpleGUI are statically defined. In order to keep up with future changes, it is desirable to add a dynamic import of these definitions: on first run, these will be downloaded from GitHub and written locally.

Another improvement would be to first use a parser and tokenize the code in order to locate all the uses of `sg` in the text in order to extract the specific calls to **PySimpleGUI**. This would be the most efficient way for handling **all calls** to **PySimpleGUI**. I did not look into parsing the text, but might do this in the future.

## Issues and Features
The most common issue that might come up when running **PySimpleNoGUI** for the first time is having the code break because of unknown function calls and elements. The reason for this is that **PySimpleGUI** uses multiple names for common functions and elements, some of which are not yet included in **PySimpleNoGUI**.

It is very easy to fix such breaks because adding a function/element/constant is easy: just add the missing item to the respective tuples: either `empty_func_list`, `empty_consts_list `, or `elements_list`. Note that because different elements have specific behaviors, I creates `elements_aliases`, which is a dictionary that matches additional names to already existing elements (e.g., `Input` is just another alias for `InputText`).

Or you can write me about adding/fixing something.

That's it!
