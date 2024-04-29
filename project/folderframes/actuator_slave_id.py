
import tkinter as tk
from tkinter import ttk
from .utils import Utils
from pymongo import MongoClient
import random
import string
from .add_actuator import AddActuator
from tkinter import messagebox

class ActuatorSlaveId(tk.Frame,AddActuator):
    def __init__(self, parent):
        super().__init__(parent)
        print('Add Actuator Slave id')
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['modbus']
        self.Rcollection = self.db['slave range']

    def create_actuator_slave_id_widget(self):

        page_name_label = tk.Label(self, text="Add Actuator", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR, font=(
            "TkTextFont", 25), borderwidth=2, relief="solid", justify="center", padx=15, pady=5, highlightcolor="white", highlightbackground="red")
        page_name_label.grid(row=0, column=0, columnspan=5, pady=50)

        modbus_id_label = tk.Label(
            self, text="Modbus ID:", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        modbus_id_label.grid(row=1, column=0, padx=10, pady=10, sticky="ne")
        client = MongoClient("mongodb://localhost:27017/")
        db = client["modbus"]
        collection = db["configurations"]
       # available_ids = [str(doc["modbus_id"]) for doc in collection.find({}, {"modbus_id": 1})]
        available_ids = set(str(doc["modbus_id"])
                            for doc in collection.find({}, {"modbus_id": 1}))
        available_names = [str(doc["sensor"])
                           for doc in self.Rcollection.find({}, {"sensor": 1})]
        available_ids = list(available_ids)

        self.modbus_id_combobox = ttk.Combobox(
            self, width=20, values=available_ids)
        self.modbus_id_combobox.grid(
            row=1, column=1, padx=10, pady=10, sticky="ne")

        slave_name_label = tk.Label(
            self, text="Slave Name", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        slave_name_label.grid(row=2, column=0, padx=10, pady=10, sticky="ne")
        self.slave_name = ttk.Combobox(
            self, width=20, values=available_names)
        self.slave_name.grid(row=2, column=1, padx=10, pady=10, sticky="ne")

        self.slave_id_entry2 = tk.Entry(self, width=25)
        self.slave_id_entry2.grid(
            row=3, column=1, padx=10, pady=10, sticky="ne")

        slave_id_label = tk.Label(
            self, text="Slave ID", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        slave_id_label.grid(row=3, column=0, padx=10, pady=10, sticky="ne")

        self.generate_uniue_id_button = tk.Button(
            self, text="G", bg=Utils.BTN_COLOR, justify="center", command=lambda: Utils.gen_id(self, 3))
        self.generate_uniue_id_button.grid(
            row=3, column=2, padx=10, pady=10, sticky="ne")

        channelid_label = tk.Label(
            self, text="Channel ID", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        channelid_label.grid(row=4, column=0, padx=10, pady=10, sticky="ne")

        self.channelid_entry = tk.Entry(self, width=25)
        self.channelid_entry.grid(
            row=4, column=1, padx=10, pady=10, sticky="ne")

        verify_uniqueness = tk.Button(
            self, text="Verify Uniqueness", bg=Utils.BTN_COLOR, command=lambda:self.verify_all_the_entries())
        verify_uniqueness.grid(row=5, column=1, padx=5, pady=50, sticky="S")

    def show_actuator_slave_id_widget(self):
        for widgets in self.winfo_children():
            widgets.destroy()
            
        self.pack(fill="y")
        print("Slave id")
        self.create_actuator_slave_id_widget()

    def verify_all_the_entries(self):
        data_values_dict = {}
        data_values_dict["Slave Name"] = self.slave_name.get()
        data_values_dict["Channel ID"] = self.channelid_entry.get()
        data_values_dict["Slave ID"] = self.slave_id_entry2.get()
        
        data_values_dict["Modbus ID"] = self.modbus_id_combobox.get()
        data_list = []
        for key, value in data_values_dict.items():
            if value is None or value == '':
                data_list.append(key)
        if not data_list:  # Instead of 'data_list is []', use 'not data_list'
            return  Utils.verify_entry(self, 3)
        else:
            messagebox.showerror(
                'Fields Empty', f'Error: {data_list} fields Empty')
        
    