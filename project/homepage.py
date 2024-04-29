import uuid
import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk,Image
from pymongo import MongoClient
import random

from project.folderframes.add_sensor import AddSensor
from project.folderframes.addrange import AddRange
from project.folderframes.body import Body
from project.folderframes.modbus_id import ModbusID
from project.folderframes.sensor_slave_id import SensorSlaveId
from project.folderframes.actuator_slave_id import ActuatorSlaveId
from project.folderframes.modbus_setting import ModbusSetting
from tkinter import filedialog
import serial.tools.list_ports
import time
import string
from influxdb import InfluxDBClient
from datetime import datetime
import json
from project.folderframes.mapping import Mapping

BG_COLOR='#0F054C'
FONT_COLOR = '#F6F6F6'
BTN_COLOR = "#61CE70"



class HomePage(tk.Toplevel):
    def __init__(self,root):
        super().__init__(root)
        self.title("Homepage")
        self.geometry("1280x720")
        self.sensor_list = []
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['modbus']
        self.Rcollection = self.db['slave range']  

        self.count=1
        self.configure(bg = BG_COLOR)
        self.header_frame = tk.Frame(self,bg=BG_COLOR)
        self.footer_frame = tk.Frame(self,bg=BG_COLOR)
        self.show_header()
        self.slave_id_frame = SensorSlaveId(self)
        self.add_sensor_frame = AddSensor()
        self.actuator_slave_id_frame = ActuatorSlaveId(self)
        self.mapping_frame = Mapping(self)
        self.add_range_frame = AddRange(self)
        self.modbus_id_frame = ModbusID(self)
        self.modbus_setting = ModbusSetting(self)
        self.body_frame = Body(self)
        self.active_frame = self.body_frame
        print('active frame',self.active_frame)
        self.footer()
        

# Construct the path to the image file relative to the root directory
            
        self.frames = {"Home":self.body_frame,"AddSensor": AddSensor(),"SensorSlaveID":self.slave_id_frame, "ActuatorSlaveID": self.actuator_slave_id_frame,"Mapping": self.mapping_frame,"AddRange": self.add_range_frame,"ModbusID":self.modbus_id_frame,"ModbusSetting":self.modbus_setting}
        self.offcanvas_frame = tk.Frame(self, width=400, height=600, bg='#4422ee')
        self.show_offcanvas_widget()
        self.show_frame("Home")
        
    def show_frame(self, frame_name):
        if self.active_frame:
            print('Pack Forget', type(self.active_frame))
            self.active_frame.pack_forget()
            print('self.active_frame',self.active_frame)
        self.active_frame = self.frames[frame_name]
        print(self.active_frame,frame_name)
        if frame_name == "ModbusID":
            ModbusID.show_modbus_id_widget(self.modbus_id_frame)
        elif frame_name == "AddModbus":
            self.show_add_modbus_widget()
        elif frame_name == "AddRange":
            AddRange.show_add_range_widget(self.add_range_frame)    
        elif frame_name == "Home":
            Body.show_body_table_widget(self.body_frame)
        elif frame_name == "AddSensor":
            # self.show_add_sensor_widget()
            AddSensor.show_add_sensor_widget()
        elif frame_name == "SensorSlaveID":
            SensorSlaveId.show_sensor_slave_id_widget(self.slave_id_frame)
            
        elif frame_name == "ActuatorSlaveID":
            ActuatorSlaveId.show_actuator_slave_id_widget(self.actuator_slave_id_frame)
        
        elif frame_name == "AddActuator":
            self.show_add_actuator_widget()
        elif frame_name == "Mapping":
            Mapping.show_mapping_widget(self.mapping_frame)
        elif frame_name == "ModbusSetting":
            ModbusSetting.show_modbussetting_widget(self.modbus_setting)
            
            
    
    def create_header_widgets(self):
        root_directory = os.getcwd()
        print('root_dir',root_directory)
        top_image = os.path.join(root_directory,"project", "folderframes","imgs","top.png")
        hamb_image = os.path.join(root_directory,"project", "folderframes","imgs","hamburger.png")
        self.top_image_path = top_image.replace("\\", "/")
        self.hamb_image_path = hamb_image.replace("\\", "/")  
        
        print(self.top_image_path)
        image = tk.PhotoImage(file=str(self.top_image_path))
        pil_img = Image.open(str(self.hamb_image_path))
        hamburger = tk.PhotoImage(file=str(self.hamb_image_path))
        hamburger_image = Image.open(str(self.hamb_image_path))

        print(' height=pil_img.height, width=pil_img.width ',pil_img.width, pil_img.height)
        canvas = tk.Canvas(self.header_frame, background="#4422ee",
                           height=40, width=224, highlightthickness=0)
        canvas.create_image(0,22, anchor="w", image=image)
        canvas.image = image
        print(canvas.image.width)
        canvas.grid(row=0, column=8, sticky="W", pady=10)
        self.header_frame.grid()
        resized_hamburger_image = hamburger_image.resize((20, 20))

        tk_hamburger_image = ImageTk.PhotoImage(resized_hamburger_image)

        canvas1 = tk.Canvas(self.header_frame,
                            background="#4422ee", height=30, width=30)
        canvas1.create_image(15, 15, anchor="center", image=tk_hamburger_image)
        canvas1.image = tk_hamburger_image

        self.offcanvas_button = tk.Button(self.header_frame, image=canvas1.image,
                                          bg=BTN_COLOR, compound=tk.RIGHT, command=self.toggle_frame_visibility)
        
        self.home_button = tk.Button(self.header_frame,text="Home",bg=BTN_COLOR,command=lambda name="Home": self.show_frame(name))
        self.add_modbus_button = tk.Button(self.header_frame,text="Add Modbus",bg=BTN_COLOR,command=lambda name="ModbusID": self.show_frame(name))
        self.add_sensor_button = tk.Button(self.header_frame,text="Add Sensor",bg=BTN_COLOR,command=lambda name="SensorSlaveID": self.show_frame(name))
        self.add_acctuator_button = tk.Button(self.header_frame,text="Add Acctuator",bg=BTN_COLOR,command=lambda name="ActuatorSlaveID": self.show_frame(name))
        self.add_errorlog_button = tk.Button(self.header_frame,text="Errorlog",bg=BTN_COLOR)
        self.mapping_button = tk.Button(self.header_frame,text="Mapping",bg=BTN_COLOR,command=lambda name="Mapping": self.show_frame(name))
        self.slave_id_range_button = tk.Button(self.header_frame,text="Add Range",bg=BTN_COLOR,command=lambda name="AddRange": self.show_frame(name))
        self.modbussetting_button = tk.Button(self.header_frame,text="Modbus Settings",bg=BTN_COLOR,command=lambda name="ModbusSetting": self.show_frame(name))
        label = tk.Label(self.header_frame,bg="#4422ee",fg=BG_COLOR)
        
        self.logout_button = tk.Button(self.header_frame, bg=BTN_COLOR,
                          fg=FONT_COLOR, text="Logout", )
        

        self.offcanvas_button.grid(row=0, column=0,  padx=10, pady=10,)
        self.home_button.grid(row=0, column=1,  padx=10, pady=10,)
        self.add_sensor_button.grid(row=0, column=2,  padx=10, pady=10)
        self.add_acctuator_button.grid(row=0, column=3,  padx=10, pady=10)
        self.add_modbus_button.grid(row=0, column=4,  padx=10, pady=10)
        self.mapping_button.grid(row=0, column=5,  padx=10, pady=10)
        self.slave_id_range_button.grid(row=0, column=6,  padx=10, pady=10)
        label.grid(row=0, column=7,  padx=200, pady=10)
       # self.modbussetting_button.grid(row=0, column=7,  padx=10, pady=10)
        self.logout_button.grid(row=0, column=7,  padx=10, pady=10)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_columnconfigure(4, weight=1)
        
    def show_header(self):
        self.create_header_widgets() 
        self.header_frame.config(bg="#4422ee")
        self.header_frame.pack(fill="both")
        
    def footer(self):
        self.footer_label_left = tk.Label(self.footer_frame,bg=BG_COLOR,fg=FONT_COLOR, text="Proprietry Technologies",anchor="w")
        self.footer_label_right = tk.Label(self.footer_frame,bg=BG_COLOR,fg=FONT_COLOR, text="Powered by Envirya Projects Pvt. Ltd.",anchor="e")
        self.footer_label_left.pack(side="left",expand=True)
        self.footer_label_right.pack(side="left",expand=True)
        self.footer_frame.pack(side="bottom", fill="x", pady=20) 
        
    def toggle_frame_visibility(self):
        if self.offcanvas_frame.winfo_viewable():
            self.offcanvas_frame.place_forget()  # Hide the frame
        else:
            self.offcanvas_frame.place(x=0,y=53)   
        
     
    def show_offcanvas_widget(self):
        
      #  if self.offcanvas_frame.winfo_x() <=0:
           # print(self.offcanvas_frame.winfo_x())
            # Slide in the offcanvas
            self.offcanvas_frame.place(x=0,y=53)
            self.offcanvas_frame.place_forget() 
            self.create_offcanvas_widget()   
        
    def create_offcanvas_widget(self):
        empty=tk.Label(self.offcanvas_frame,text="",bg='#4422ee')
        empty.grid(row=0,column=2,pady=50,sticky="E") 
        self.upload_button = tk.Button(self.offcanvas_frame,text="       Upload       ",bg=BTN_COLOR)
        self.upload_button.grid(row=1,column=0,sticky="E")
        empty=tk.Label(self.offcanvas_frame,text="",bg='#4422ee')
        empty.grid(row=2,column=1,sticky="E")
        empty=tk.Label(self.offcanvas_frame,text="",bg='#4422ee')
        empty.grid(row=3,column=2,sticky="E")
        self.about_us_button  = tk.Button(self.offcanvas_frame,text="     About Us      ",bg=BTN_COLOR)
        self.about_us_button.grid(row=4,column=0,sticky="E")
        empty=tk.Label(self.offcanvas_frame,text="",bg='#4422ee')
        empty.grid(row=5,column=1,sticky="E")
        empty=tk.Label(self.offcanvas_frame,text="",bg='#4422ee')
        empty.grid(row=6,column=2,sticky="E") 
        self.help_button  = tk.Button(self.offcanvas_frame,text="         Help         ",bg=BTN_COLOR)
        self.help_button.grid(row=7,column=0,sticky="E")
        empty=tk.Label(self.offcanvas_frame,text="",bg='#4422ee')
        empty.grid(row=8,column=1,sticky="E")
        empty=tk.Label(self.offcanvas_frame,text="",bg='#4422ee')
        empty.grid(row=9,column=2,sticky="E")        
        self.factory_reset_button  = tk.Button(self.offcanvas_frame,text="  Factory Reset   ",bg=BTN_COLOR)
        self.factory_reset_button.grid(row=10,column=0,sticky="E")
        empty=tk.Label(self.offcanvas_frame,text="",bg='#4422ee')
        empty.grid(row=11,column=1,sticky="E")
        empty=tk.Label(self.offcanvas_frame,text="",bg='#4422ee')
        empty.grid(row=12,column=2,sticky="E")        
        self.modbus_setting_button  = tk.Button(self.offcanvas_frame,text="Modbus Setting",bg=BTN_COLOR,command=lambda name="ModbusSetting": self.show_frame(name))
        self.modbus_setting_button.grid(row=13,column=0,sticky="E")
        empty=tk.Label(self.offcanvas_frame,text="",bg='#4422ee')
        empty.grid(row=14,column=2,padx=20,pady=150,sticky="E")
        
    def toggle_frame_visibility(self):
        if self.offcanvas_frame.winfo_viewable():
            self.offcanvas_frame.place_forget()  # Hide the frame
        else:
            self.offcanvas_frame.place(x=0,y=53)
                 

if __name__ == "__main__":
    app = HomePage()
    app.mainloop()

