#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project start date: Thurs 11/19/2020

@author: Gil Ben-Herut

A GUI-less mockup for PySimpleGUI/MySimpleGUI

Notes:
    There is no treatment for layout. Elements are recorded in their intiialization only.
"""

from sys import exit, argv
from time import sleep
from pathlib import Path
from traceback import format_stack

from cleverdict import CleverDict
from ipdb import set_trace  # noqa: F401


def get_func_name():
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
        return self.ele_val

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

        # print(f"{self.ele_key}: {new_val}")
        if new_val:
            self.ele_val = new_val
            if self.ele_type == 'Multiline':
                print(f"{self.ele_key}: {new_val}")

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
        print(
            f"Module {Path(__file__).stem} is activated, no GUI will show (press Ctrl+c to break event loop).\n"
            f"Total GUI elements registered: {len(ele)}."
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
        try:
            sleep(0.001)
        except KeyboardInterrupt:
            exit()
        return '__TIMEOUT__', {a: b.ele_val for a, b in self.items() if type(b) == ElementObject}

    def close(self):
        return None


def init_ele(args, kwargs, ele_from_alias=None):
    if not (ele_type := ele_from_alias):
        ele_type = get_func_name()
    # an element is created only if it has a 'key' value
    if kwargs.get('key'):
        ele_val = ''
        # finding the element's value
        if args:
            # in most elements value is passed in first parameter, but not in all
            if ele_type == 'Combo':
                ele_val = args[1]
            else:
                ele_val = args[0]
        # value could also be passed as keyword parameters, depending on element type
        elif ele_type == 'Button':
            ele_val = kwargs['button_text']
        elif ele_type == 'Checkbox':
            ele_val = kwargs['default']

        # storing element's essential data: name (as key), type, value
        ele[kwargs['key']] = ElementObject(kwargs['key'], ele_type, ele_val)
    return None


# Mockup for any function called in sg module that does not do anything.
empty_func_list = (
    'theme',
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

# Mockup for any const (variable really) called in sg module that does not anything.
empty_consts_lst = (
    'RELIEF_SUNKEN',
    'WIN_CLOSED',
)
for c in empty_consts_lst:
    exec(
        f"""
{c} = None
        """
    )

# list of mockup GUI elements
ele_list = (
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
)
# setup a function definition for any element creation call.
# Calls to init_ele which Will create an instance of ElementObject class.
for e in ele_list:
    exec(
        f"""
def {e}(*args, **kwargs):
    init_ele(args, kwargs)
    return None
        """
    )

ele_aliases = {
    'In': 'InputText',
}
for e in ele_aliases:
    exec(
        f"""
def {e}(*args, **kwargs):
    init_ele(args, kwargs, ele_from_alias=ele_aliases['{e}'])
    return None
        """
    )

ele = {}
