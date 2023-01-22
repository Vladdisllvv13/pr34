from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
##макеты
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout

import json

class calculator(App):
    def build(self):
        self.ins = Animation(font_size = 80, duration = 0.1)
        self.outs = Animation(font_size = 50, duration = 0.1)
        
        
        
        fs = "20sp"
        self.state = False
        self.history = [0]
        #settings data#
        default = {"theme":"light"}
        try:
            with open("theme.txt") as data:
                l = json.load(data)
                theme = l["theme"]
        except:
            with open("theme.txt", "w") as data:
                json.dump(default, data)
            with open("theme.txt") as data:
                l = json.load(data)
                theme = l["theme"]
                
        if theme == "light":
            tcol = (0,0,0,1)
            bg = (.8,.8,.8,1)
            
            Window.clearcolor = (.9,.9,.9,1)
            
        elif theme == "dark":
            tcol = (1,1,1,1)
            bg = (.2,.2,.2,1)
            Window.clearcolor = (.1,.1,.1,1)
                    
        self.calc_text = ""
        buttons_list = ["9","8","7","+",
                         "6","5","4","-",
                         "3","2","1","*",
                         ".","0","=","/"]
        buttons_panel = GridLayout(rows = 4)
        bl = BoxLayout(orientation = "vertical")
        bl_tool = BoxLayout(size_hint = (1,.15))
        clear = Button(text = "clear",background_normal = "norm.png", background_down = "down.png", color = tcol, font_size = fs)
        remove = Button(text = "remove", background_normal = "norm.png", background_down = "down.png", color = tcol, font_size = fs)
        clear.bind(on_release = self.clear)
        remove.bind(on_release = self.remove)
        bl_tool.add_widget(clear)
        bl_tool.add_widget(remove)
        ##settings##
        self.settings_view = ModalView(size_hint = (.6,.5), background = "bg.png", background_color = bg)
        blset = BoxLayout(orientation = "vertical")
        #settings = Button(text = "Настройки", background_normal = "norm.png", background_down = "down.png", color = tcol, font_size = fs)
        self.info = Label(font_size = fs, color = tcol)
        bl_top = BoxLayout(size_hint = (1,.2))
        #bl_top.add_widget(settings)
        bl_top.add_widget(self.info)
        light = Button(text = "Light",background_normal = "norm.png", background_down = "down.png", color = tcol, font_size = fs)
        dark = Button(text = "Dark",background_normal = "norm.png", background_down = "down.png", color = tcol, font_size = fs)
        blset.add_widget(light)
        blset.add_widget(dark)
        self.settings_view.add_widget(blset)
        #settings.bind(on_release = self.open_settings)
        light.bind(on_release = self.themeedit)
        dark.bind(on_release = self.themeedit)
        for btl in buttons_list:
            btn = Button(text = btl, background_normal = "norm.png", background_down = "down.png", color = tcol, font_size = fs)
            buttons_panel.add_widget(btn)
            btn.bind(on_release = self.add)
        self.result_label = Label(color = tcol, text_size = (Window.width - Window.width/4, Window.height/5), size_hint = (1,.5), font_size = 50)
        self.result_label2 = Label(color = tcol, text_size = (Window.width - Window.width/4, Window.height/5), size_hint = (1,.5), font_size = 50)
        bl.add_widget(bl_top)
        bl.add_widget(self.result_label)
        bl.add_widget(self.result_label2)
        bl.add_widget(bl_tool)
        bl.add_widget(buttons_panel)
        Clock.schedule_interval(self.null, 0.1)
        Clock.schedule_interval(self.calculate, 0.1)
        return bl
    def add(self, instance):
        
        special_symbol = ["*","+","-","/","."]
        for sp in special_symbol:
            if self.history[len(self.history)-1] == sp and (instance.text == "*" or instance.text == "-" or instance.text == "+" or instance.text == "/" or instance.text == "."):
                self.calc_text = self.calc_text.rstrip(self.history[len(self.history)-1])
            
        
        try:
            if instance.text == "=":
                self.result_label2.text = str(eval(self.calc_text))
                self.ins.start(self.result_label2)
                self.outs.start(self.result_label)
                 
            
            if not len(self.result_label.text) == 60 and not instance.text == "=":
                self.calc_text += instance.text
                self.outs.start(self.result_label2)
                self.ins.start(self.result_label)
                
                    
                    
            if len(self.result_label.text) == 60:
                self.info.text = "max length"
            else:
                self.info.text = ""
        except:
            pass
        self.history.append(instance.text)
        self.result_label.text = self.calc_text
        
    def clear(self, instance):
        self.calc_text = ""
        self.result_label.text = self.calc_text
        self.info.text = ""
    def remove(self, instance):
        self.calc_text = self.calc_text[:-1]
        self.result_label.text = self.calc_text   
        self.info.text = ""
    def null(self, dt):
        if self.result_label.text == "" and self.state:
            self.result_label.text = "0"
    def calculate(self, dt):
        try:
            self.result_label2.text = str(eval(self.calc_text))
        except:
            pass
    def open_settings(self, instance):
        self.settings_view.open() 
        self.state = True
    def themeedit(self, instance):
        if instance.text == "Light":
            a = {"theme":"light"}
            with open("theme.txt", "w") as data:
                json.dump(a, data)
        elif instance.text == "Dark":
            b = {"theme":"dark"}
            with open("theme.txt", "w") as data:
                json.dump(b, data)
        self.state = False
        self.result_label.text = ""
        self.result_label2.text = ""
        self.calc_text = ""
        self.settings_view.dismiss()
        
        re()
                
def re():
        calculator().run()
        
calculator().run()