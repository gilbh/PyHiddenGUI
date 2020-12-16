#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Project start date: Thurs 11/19/2020

@author: Gil Ben-Herut

This demo shows how to run a PySimpleGUI application in a text-only command line terminal.

Notes:

1) To switch between GUI and GUI-less, simply change the boolean flag: terminal_mode

2) For auto activation of a button (or mmore than one) when running GUI-less,
simpy add keyword parameters to Button Element:

metadata='auto_activate'
"""


# toggle terminal_mode to switch between GUI and GUI-less
terminal_mode = True
# terminal_mode = False
if terminal_mode:
    import PyInvisibleGUI as sg
else:
    import PySimpleGUI as sg

from json import (load as jsonload, dump as jsondump)
from os import path
from ipdb import set_trace  # noqa: F401

SETTINGS_FILE = path.join(path.dirname(__file__), r'settings_file.cfg')
DEFAULT_SETTINGS = {
    'max_users': '[enter no.]', 'user_data_folder': '[choose folder]', 'theme': sg.theme(), 'zipcode': '[enter zip]'

}
SETTINGS_KEYS_TO_ELEMENT_KEYS = {
    'max_users': '-MAX USERS-', 'user_data_folder': '-USER FOLDER-', 'theme': '-THEME-', 'zipcode': '-ZIPCODE-'
}


def load_settings(settings_file, default_settings):
    try:
        with open(settings_file, 'r') as f:
            settings = jsonload(f)
    except FileNotFoundError as e:
        sg.popup_quick_message(
            f'exception {e}', 'No settings file found... will create one for you',
            keep_on_top=True, background_color='red', text_color='white'
        )
        settings = default_settings
        save_settings(settings_file, settings, None)

    return settings


def save_settings(settings_file, settings, values):
    if values:
        for key in SETTINGS_KEYS_TO_ELEMENT_KEYS:
            try:
                settings[key] = values[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]]
            except Exception:
                print(f'Problem updating settings from window values. Key = {key}')

    with open(settings_file, 'w') as f:
        jsondump(settings, f)


def update_settings_window(window, settings):
    for key in SETTINGS_KEYS_TO_ELEMENT_KEYS:
        try:
            window[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]].update(value=settings[key])
        except Exception:
            print(f'Problem updating PySimpleGUI window from settings. Key = {key}')


def create_main_window(settings):

    def TextLabel(text):
        return sg.Text(text + ':', justification='r', size=(15, 1))

    sg.theme(settings['theme'])

    layout = [
        [sg.Text('1) Configuration parameters:', font='Any 15')],
        [TextLabel('Max Users'), sg.Input(key='-MAX USERS-')],
        [TextLabel('User Folder'), sg.Input(key='-USER FOLDER-'), sg.FolderBrowse(target='-USER FOLDER-')],
        [TextLabel('Zipcode'), sg.Input(key='-ZIPCODE-')],
        [TextLabel('Theme'), sg.Combo(sg.theme_list(), size=(20, 20), key='-THEME-')],
        [sg.Text('2) Click \'Run\' to execute demo program with parameters:', font='Any 15')],
        [sg.B('Run', metadata='auto_activate'), sg.B('Exit')],
    ]

    window = sg.Window('Main Application', layout)
    window.finalize()
    window.TKroot.focus_force()

    return window


def run_demo(window):
    print('\nRunning Demo with PyInvisibleGUI using loaded settings:')
    for key in SETTINGS_KEYS_TO_ELEMENT_KEYS:
        print(f"{key}: {window[SETTINGS_KEYS_TO_ELEMENT_KEYS[key]].get()}")
    print('\nFinished!')


def main():
    settings = load_settings(SETTINGS_FILE, DEFAULT_SETTINGS)
    window = create_main_window(settings)
    update_settings_window(window, settings)
    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        if event == 'Run':
            run_demo(window)
            break

    save_settings(SETTINGS_FILE, settings, values)
    window.close()

    return None


main()
