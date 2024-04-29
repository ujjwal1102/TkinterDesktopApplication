
import tkinter as tk
from tkinter import ttk
from .utils import Utils
from pymongo import MongoClient
from .add_modbus import AddModbus
from tkinter import messagebox


class ModbusID(tk.Frame, AddModbus):
    def __init__(self,parent):
        super().__init__(parent)
        print('Add Modbus Id')
        
    def create_modbus_id_widget(self):
        page_name_label = tk.Label(self, text="Add Modbus", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR, font=(
            "TkTextFont", 25), borderwidth=2, relief="solid", justify="center", padx=15, pady=5, highlightcolor="white", highlightbackground="red")
        
        page_name_label.grid(row=0, column=0, columnspan=5, pady=50)
        
        self.modbus_id_label = tk.Label(
            self, text="Modbus Id", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        self.modbus_id_entry2 = tk.Entry(self, width=25)

        self.modbus_name_label = tk.Label(
            self, text="Modbus Name", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        self.modbus_name2 = tk.Entry(self, width=25)

        self.verify_uniqueness_button = tk.Button(
            self, text="verify", bg=Utils.BTN_COLOR, command=lambda: self.data_values_modbus_id())

        self.generate_uniue_id_button = tk.Button(
            self, text="G", bg=Utils.BTN_COLOR, command=lambda: Utils.gen_id(self,1))

        self.modbus_id_label.grid(
            row=1, column=0, padx=10, pady=10, sticky="ne")
        self.modbus_id_entry2.grid(
            row=1, column=1, padx=10, pady=10, sticky="ne")
        self.modbus_name_label.grid(
            row=2, column=0, padx=10, pady=10, sticky="ne")
        self.modbus_name2.grid(row=2, column=1, padx=10, pady=10, sticky="ne")
        self.generate_uniue_id_button.grid(
            row=1, column=2, padx=10, pady=10, sticky="ne")
        self.verify_uniqueness_button.grid(
            row=3, column=1, padx=10, pady=10, sticky="W"+"E"+"N"+"S")
        # self.goback_button.grid_remove()

    def data_values_modbus_id(self):
          
        data_values_dict = {}
        data_values_dict["Modbus Id"]= self.modbus_id_entry2.get()
        data_values_dict["Modbus Name"]=self.modbus_name2.get()
                
        data_list = []
        for key, value in data_values_dict.items():
            if value is None or value == '':
                data_list.append(key)
        if not data_list:  # Instead of 'data_list is []', use 'not data_list'
            return Utils.verify_entry(self,1)
        else:
            messagebox.showerror(
                'Fields Empty', f'Error: {data_list} fields Empty')

    def show_modbus_id_widget(self):
        
        for widgets in self.winfo_children():
            widgets.destroy()
        self.pack(fill="y")
        self.create_modbus_id_widget()