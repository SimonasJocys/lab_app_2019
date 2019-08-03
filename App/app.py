import numpy as np
from glob import glob
import matplotlib.pyplot as plt
from skimage.morphology import remove_small_objects, label
import cv2
from array import array

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
from kivy.graphics.texture import Texture

from kivy.core.image import Image as II

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

# ----------------------------------- LOGO -----------------------------------
<Logo>:
# Label: welcome
    BoxLayout:
        orientation: 'vertical'
        Image_btn:
            source: 'img/logo.png'
            allow_stretch: True
            on_press: root.manager.current = 'menu'

# ----------------------------------- MENU -----------------------------------
<Menu>:
    GridLayout:
        cols2: 2
        rows: 3
# Button for cell count 1
        Button:
            size_hint_y: 0.5
            text: 'Cell counter confocal'
            on_press: root.manager.current = 'part1'
            background_normal: 'img/menu.png'
            background_down: 'img/menu_press.png'
            border: 0,100,0,100
            font_size: 40
            bold: True
            italic: True
# Button for cell count 2
        Button:
            size_hint_y: 0.5
            text: 'Cell counter light'
            on_press: root.manager.current = 'part2'
            background_normal: 'img/menu.png'
            background_down: 'img/menu_press.png'
            border: 0,100,0,100
            font_size: 40
            bold: True
            italic: True
# Button for ...
        Button:
            size_hint_y: 0.5
            text: '...'
            on_press: root.manager.current = 'part3'
            background_normal: 'img/menu.png'
            background_down: 'img/menu_press.png'
            border: 0,100,0,100
            font_size: 40
            bold: True
            italic: True
# Button for ...
        Button:
            size_hint_y: 0.5
            text: '...'
            on_press: root.manager.current = 'part3'
            background_normal: 'img/menu.png'
            background_down: 'img/menu_press.png'
            border: 0,100,0,100
            font_size: 40
            bold: True
            italic: True
# Button for ...
        Button:
            size_hint_y: 0.5
            text: '...'
            on_press: root.manager.current = 'part3'
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
        size_hint_x: 1
        padding: 30
        spacing: 20
# Selected Image
        Image:
            id: img_con
            source: root.select_img()
            allow_stretch: False
            pos_hint: {'center_x': .5}
# Button: menu
        Button:
            size_hint: .5, .3
            text: 'Count'
            font_size: 30
            background_normal: 'img/btn_black.png'
            background_down: 'img/btn_press.png'
            background_disabled_normal: 'img/btn_dis.png'
            on_press: 
                root.count_cells()
                root.manager.current = 'count'
                root.manager.get_screen('count').ids.img_confocal.source = root.img
                # root.manager.get_screen('count').ids.img_count.canvas\
                #     .get_group('c')[0].texture = root.texture
                root.manager.get_screen('count').ids.number.text = \
                    'Number of \\nCells: {}'.format(root.N)
            border: 0,0,0,0
            color: 1,1,1,1
            pos_hint: {'center_x': .5}
# Count cells
<Count_screen>:
# background color
    canvas.before:
        Color:
            rgba: 1, 0, 1, 0.85
        Rectangle:
            pos: self.pos
            size: self.size
    BoxLayout:
        orientation: 'horizontal'
        size_hint_y: 1
        padding: 10
        spacing: 10
        BoxLayout:
            orientation: 'vertical'
            spacing: 20
# Selected Image
            Image:
                id: img_confocal
                allow_stretch: False
# Counted Image
            FullImage: 
                id: img_count
                canvas:
                    Rectangle:
                        group: 'c'
                        pos: self.pos
                        texture: root.make_img()
                        size: root.size
# Buttons
        BoxLayout:
            orientation: 'vertical'
            size_hint_x: .3
            spacing: 20
            Label:
                id: number
                text: 'Number of \\nCells: 0'
                font_size: 30
                bold: True
                italic: True
                color: 0.15, 0.8, 0.3, 1
                canvas.before:
                    Color:
                        rgba: 0, 0, 0, 0.7
                    Rectangle:
                        pos: self.pos
                        size: self.size
            Button:
                size_hint_y: .3
                text: 'Next'
                font_size: 30
                background_normal: 'img/btn_black.png'
                background_down: 'img/btn_press.png'
                background_disabled_normal: 'img/btn_dis.png'
                on_press: root.manager.current = 'part1'
                border: 0,0,0,0
                color: 1,1,1,1
            Button:
                size_hint_y: .3
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

# ---------------------------------- PART 3 ----------------------------------
<Container3>:
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

class FullImage(Image):
    pass

# new widget: image with button behavior
class Image_btn(ButtonBehavior, Image):
    pass

# ----------------------------------- Logo -----------------------------------
class Logo(Screen):
    pass
# ----------------------------------------------------------------------------

# ----------------------------------- Menu -----------------------------------
class Menu(Screen):
# exit program
    def exit(self):
        App.get_running_app().stop()
# ----------------------------------------------------------------------------

# ---------------------------------- Part 1 ----------------------------------
class Container1(Screen):
    """Confocal image cell count"""
    def select_img(self):
        """Choose random image"""
        self.img = np.random.choice(App.get_running_app().confocal)
        return self.img

    def clip(self, x): 
        '''Clip maximum to 4 sigma'''
        return np.clip(x, a_min=0, a_max=6*np.std(x))

    def norm(self, x): 
        x = self.clip(x)
        return (x) / ( np.max(x)) # clip at 6-sigma ?

    def binary_mask(self, x, treshold=None, sigmas = 2):
        if treshold is None:
            return self.norm(x) > sigmas*np.std(self.norm(x))
        else:
            return self.norm(x) > treshold

    def count_cells(self):
        cell = np.asarray(cv2.imread(self.img)[:,:,0], dtype=np.float32)
        binary_treshold = 0.46
        min_size = 16 # 16 px area is minimal
        # Binary tresholded image
        clean_cell_bw = remove_small_objects(
                    self.binary_mask(cell, binary_treshold), min_size = min_size)
        # count cells
        labeled = label(clean_cell_bw, background=0)
        self.N = np.max(labeled)
        # create image 
        # texture = Texture.create(size=labeled.shape)
        # labeled = cv2.imread(self.img)
        # buf = np.reshape(labeled, -1)
        # arr = array('B', buf)
        # self.texture = texture.blit_buffer(arr, colorfmt='rgb', bufferfmt='ubyte')

class Count_screen(Screen):
    def make_img(self):
        # create image 
        self.img = np.random.choice(App.get_running_app().confocal)
        labeled = cv2.imread(self.img)
        texture = Texture.create(size=labeled.shape[:2])
        # buf = np.reshape(labeled, -1)
        # arr = array('B', buf)
        # self.texture = texture.blit_buffer(arr, colorfmt='rgb', bufferfmt='ubyte')
        # self.size = labeled.shape[:2]
        data = labeled.ravel()
        self.texture = texture.blit_buffer(data, bufferfmt="ubyte", colorfmt="rgb")
        return self.texture
# ----------------------------------------------------------------------------

# ---------------------------------- Part 2 ----------------------------------
class Container2(Screen):
    pass
# ----------------------------------------------------------------------------

# ---------------------------------- Part 3 ----------------------------------
class Container3(Screen):
    pass
# ----------------------------------------------------------------------------

# --------------------------------- Make App ---------------------------------
class MainApp(App):
    confocal = glob('data/confocal/*')
    light = glob('data/light/*')
    print(confocal)
# screen manager
    sm = ScreenManager()
# build app
    def build(self):
        self.title = 'App title'
        self.icon = 'img/Logo.png'
        # MainApp.sm.add_widget(Container1(name='part1'))
        MainApp.sm.add_widget(Logo(name='logo'))
        MainApp.sm.add_widget(Menu(name='menu'))
        MainApp.sm.add_widget(Container1(name='part1'))
        MainApp.sm.add_widget(Count_screen(name='count'))
        MainApp.sm.add_widget(Container2(name='part2'))
        MainApp.sm.add_widget(Container3(name='part3'))
        return MainApp.sm

# Run App
if __name__ == "__main__":
    MainApp().run()
