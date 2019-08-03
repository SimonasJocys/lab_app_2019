#import numpy as np
import glob

from kivy.app import App
from kivy.lang import Builder

from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.carousel import Carousel
from kivy.uix.popup import Popup
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.textinput import TextInput
from kivy.uix.scatter import Scatter
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen, RiseInTransition

from kivy.clock import Clock
from functools import partial
from kivy.graphics import Color
from kivy.core.audio import SoundLoader
from kivy.animation import Animation
from kivy.properties import ObjectProperty
from kivy.event import EventDispatcher

# Configuration of app sceen on computer
from kivy.config import Config
Config.set('graphics', 'fullscreen', '0')
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')

# KIVY LANGUAGE
Builder.load_string('''
#:import np numpy

# ----------------------------------- MENU -----------------------------------
<Menu>:
    BoxLayout:
        orientation: 'vertical'
# Label: welcome
        Image:
            font_size: 40
            source: 'img/Logo.png'
            allow_stretch: True
# Button for part 1
        Button:
            size_hint_y: 0.5
            text: 'Smt..'
            on_press: root.manager.current = 'part1'
            background_normal: 'img/menu.png'
            background_down: 'img/menu_press.png'
            border: 0,100,0,100
            font_size: 40
            bold: True
            italic: True
# Button for part 2
        Button:
            size_hint_y: 0.5
            text: 'Smt...'
            on_press: root.manager.current = 'part2'
            background_normal: 'img/menu.png'
            background_down: 'img/menu_press.png'
            border: 0,100,0,100
            font_size: 40
            bold: True
            italic: True
# Button for exit
        Button:
            size_hint_y: 0.5
            text: 'Exit'
            on_press: root.exit()
            background_normal: 'img/menu.png'
            background_down: 'img/menu_press.png'
            border: 0,100,0,100
            font_size: 40
            bold: True
            italic: True
# ----------------------------------------------------------------------------

# ---------------------------------- PART 1 ----------------------------------
<Container1>:
# background color
    canvas.before:
        Color:
            rgba: 1, 1, 1, 0.85
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            size_hint_y: 1
# Button: menu
            Button:
                # size_hint_x: 1
                size_hint: None, None
                width: 200
                id: btn_menu
                text: 'Menu'
                font_size: 30
                background_normal: 'img/btn_black.png'
                background_down: 'img/btn_press.png'
                background_disabled_normal: 'img/btn_dis.png'
                on_press: root.manager.current = 'menu'
                border: 0,0,0,0
                color: 1,1,1,1
# ----------------------------------------------------------------------------

# ---------------------------------- PART 2 ----------------------------------
<Container2>:
# background color
    canvas.before:
        Color:
            rgba: 1, 1, 1, 0.85
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            size_hint_y: 1
# Button: menu
            Button:
                # size_hint_x: 1
                size_hint: None, None
                width: 200
                id: btn_menu
                text: 'Menu'
                font_size: 30
                background_normal: 'img/btn_black.png'
                background_down: 'img/btn_press.png'
                background_disabled_normal: 'img/btn_dis.png'
                on_press: root.manager.current = 'menu'
                border: 0,0,0,0
                color: 1,1,1,1
# ----------------------------------------------------------------------------
''')

# # new widget: image with button behavior
# class Image_btn(ButtonBehavior, Image):
#     pass

# ----------------------------------- Menu -----------------------------------
class Menu(Screen):
# exit program
    def exit(self):
        App.get_running_app().stop()
# ----------------------------------------------------------------------------

# ---------------------------------- Part 1 ----------------------------------
class Container1(Screen):
    pass
# ----------------------------------------------------------------------------

# ---------------------------------- Part 2 ----------------------------------
class Container2(Screen):
    pass
# ----------------------------------------------------------------------------

# --------------------------------- Make App ---------------------------------
class MainApp(App):
# screen manager
    sm = ScreenManager()
# build app
    def build(self):
        self.title = 'App title'
        self.icon = 'img/Logo.png'
        MainApp.sm.add_widget(Menu(name='menu'))
        MainApp.sm.add_widget(Container1(name='part1'))
        MainApp.sm.add_widget(Container2(name='part2'))
        return MainApp.sm

# Run App
if __name__ == "__main__":
    MainApp().run()