#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project start date: Thurs 11/19/2020

@author: Gil Ben-Herut

A GUI-less mockup for PySimpleGUI/MySimpleGUI

Version: 0.13.1

Check out project:
https://github.com/gilbh/PySimpleNoGUI
"""

from sys import exit, argv
from time import sleep
from pathlib import Path
from traceback import format_stack

from cleverdict import CleverDict
from ipdb import set_trace  # noqa: F401
from PySimpleGUI_consts import *  # noqa: F403, F401


def popup_quick_message(*args, **kwargs):
    if args:
        ps(f"popup_quick_message: {args}")


def _get_func_name():
    main_file = argv[0]
    stack = '\n'.join([l2.strip().split(',', 1)[1] for l2 in format_stack() if main_file in l2][1:])
    stack = stack.split('.')[1].split('(')[0].strip()

    return stack


class ElementObject:

    def __init__(self, ele_key, ele_type, ele_val):
        self.ele_key = ele_key
        self.ele_type = ele_type
        self.ele_val = ele_val
        return None

    def get(self):
        if self.ele_type == 'TabGroup':
            # TablGroup might store a 2D list of values, but get() should return
            #   the value of the elected Tab. Here it sends the first value.
            res = self.ele_val[0][0]
        else:
            res = self.ele_val
        return res

    def __str__(self):
        return self.get()

    def __repr__(self):
        _vars = {k: v for k, v in vars(self).items()}
        return f"{self.__class__.__name__}({repr(_vars)})"

    def update(self, *args, **kwargs):
        if args:
            new_val = args[0]
        else:
            new_val = kwargs.get('value')

        if new_val:
            self.ele_val = new_val
            if self.ele_type == 'Multiline':
                ps(f"{self.ele_key}: {new_val}")

        return None

    def set_focus(self, *args):
        return None


class Window(CleverDict):

    size: None

    class TKRoot():

        def __init__(self):
            return None

        def focus_force(self):
            return None

        def title(self):
            return None

    def __init__(self, *args, **kwargs):
        super().__init__(ele)
        self.TKroot = self.TKRoot()
        if not silent:
            ps(
                f"Module {Path(__file__).stem} is activated and no GUI will be created.\n"
                f"Total GUI elements registered: {len(ele)}.\n"
                "Press ctrl+c in case you need to break event loop.\n\n"
            )
        return None

    def maximize(self):
        return None

    def finalize(self):
        return None

    def Finalize(self):
        return None

    def set_title(self, *args):
        return None

    def CurrentLocation(self):
        return None

    def read(self, timeout=0):
        # ugly path for avoiding non-breakable infinite loop
        try:
            sleep(0.001)
        except KeyboardInterrupt:
            ps('ctrl+c was pressed. breaking event loop.')
            exit()

        # for auto activation elements
        event = ''
        if auto_activate_ele:
            event = auto_activate_ele.pop()
        else:
            event = '__TIMEOUT__'

        values = {a: b.ele_val for a, b in self.items() if type(b) == ElementObject}

        return event, values

    def close(self):
        return None


def init_ele(args, kwargs, ele_from_alias=None):
    # find type
    if not (ele_type := ele_from_alias):
        ele_type = _get_func_name()

    # find key
    ele_key = kwargs.get('key')
    # Button can get a key from the first parameter
    if not ele_key and ele_type == 'Button' and args:
        ele_key = args[0]

    ele_val = ''
    # an element is created only if it has key
    if ele_key:
        # finding the element's value
        if args:
            # in most elements value is passed in first parameter, but not in all
            if ele_type == 'Combo' and len(args) > 1:
                ele_val = args[1]
            else:
                ele_val = args[0]
        # value could also be passed as keyword parameters, depending on element type
        elif ele_type == 'Button':
            ele_val = kwargs['button_text']
        elif ele_type == 'Checkbox':
            ele_val = kwargs['default']

        # storing element's essential data: name (as key), type, value
        ele[ele_key] = ElementObject(ele_key, ele_type, ele_val)

        # set up auto activation for running the program as CLI
        # store element in order to send as event on first call of window.read()
        if kwargs.get('metadata') == 'auto_activate':
            auto_activate_ele.append(ele_key)
    else:
        # there is no key so no elements is created,
        # but if there is a value parameter was provided, send it back
        if args:
            ele_val = args[0]

    return ele_val


# list of mock-up for any function called in sg module that does not do anything.
empty_func_list = (
    'theme',
    'theme_list',
    'SetOptions',
    'HorizontalSeparator',
)
for f in empty_func_list:
    exec(
        f"""
def {f}(*args, **kwargs):
    return None
        """
    )

# list of mock-up for any const (variable really) called in sg module that does not anything.
empty_consts_list = (
    'RELIEF_SUNKEN',
    'WIN_CLOSED',
)
for c in empty_consts_list:
    exec(
        f"""
{c} = 0
        """
    )

# list of mock-up GUI elements
elements_list = (
    'Text',
    'InputText',
    'Button',
    'Checkbox',
    'Frame',
    'Combo',
    'Column',
    'CalendarButton',
    'Multiline',
    'Image',
    'TabGroup',
    'Tab',
    'FolderBrowse',
)
# setup a function definition for any element creation call.
# Calls to init_ele which Will create an instance of ElementObject class.
for e in elements_list:
    exec(
        f"""
def {e}(*args, **kwargs):
    return init_ele(args, kwargs)
        """
    )

elements_aliases = {
    'In': 'InputText',
    'Input': 'InputText',
    'B': 'Button',
}
for e in elements_aliases:
    exec(
        f"""
def {e}(*args, **kwargs):
    init_ele(args, kwargs, ele_from_alias=elements_aliases['{e}'])
    return None
        """
    )

silent = True
ele = {}
auto_activate_ele = []
# "ps" stands for "print to stdout". You can assign any output function.
ps = print
