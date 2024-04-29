
import tkinter as tk
from tkinter import ttk
from .utils import Utils
from pymongo import MongoClient
import random
import string
from .add_sensor import AddSensor
from tkinter import messagebox
utils_obj = Utils()


class SensorSlaveId(tk.Frame, AddSensor):
    def __init__(self, parent):
        super().__init__(parent)
        print('Add Sensor')
        self.sensor_list = []
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['modbus']
        self.Rcollection = self.db['slave range']

    def create_sensor_slave_id_widget(self):
        page_name_label = tk.Label(self, text="Add Sensor", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR, font=(
            "TkTextFont", 25), borderwidth=2, relief="solid", justify="center", padx=15, pady=5, highlightcolor="white", highlightbackground="red")
        page_name_label.grid(row=0, column=0, columnspan=5, pady=50)

        modbus_id_label = tk.Label(
            self, text="Modbus ID:", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        modbus_id_label.grid(row=1, column=0, padx=10, pady=10, sticky="ne")

        client = MongoClient("mongodb://localhost:27017/")
        db = client["modbus"]
        collection = db["configurations"]
        available_ids = set(str(doc["modbus_id"])
                            for doc in collection.find({}, {"modbus_id": 1}))
        available_names = [str(doc["sensor"])
                           for doc in self.Rcollection.find({}, {"sensor": 1})]
        available_ids = list(available_ids)

        sensor_id_label = tk.Label(
            self, text="Sensor ID:", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        sensor_id_label.grid(row=4, column=0, padx=10, pady=10, sticky="ne")

        self.sensor_id_entry = tk.Entry(self, width=25)
        self.sensor_id_entry.grid(
            row=4, column=1, padx=10, pady=10, sticky="ne")

        self.generate_sensor_id_button = tk.Button(
            self, text="G", bg=Utils.BTN_COLOR, justify="center", command=lambda: self.generate_sensor_id())
        self.generate_sensor_id_button.grid(
            row=4, column=2, padx=10, pady=10, sticky="ne")

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

        self.slave_id_entry21 = tk.Entry(self, width=25)
        self.slave_id_entry21.grid(
            row=3, column=1, padx=10, pady=10, sticky="ne")

        slave_id_label = tk.Label(
            self, text="Slave ID", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        slave_id_label.grid(row=3, column=0, padx=10, pady=10, sticky="ne")

        self.generate_uniue_id_button = tk.Button(
            self, text="G", bg=Utils.BTN_COLOR, justify="center", command=lambda: Utils.gen_id(self, 2))
        self.generate_uniue_id_button.grid(
            row=3, column=2, padx=10, pady=10, sticky="ne")
        utils_obj = Utils()
        verify_uniqueness = tk.Button(
            self, text="Verify Uniqueness", bg=Utils.BTN_COLOR, command=lambda: self.verify_all_entries())
        verify_uniqueness.grid(row=4, column=1, padx=5, pady=50, sticky="S")

    def verify_all_entries(self):
        data_values_dict = {}
        data_values_dict["Modbus ID:"] = self.modbus_id_combobox.get()
        data_values_dict["Slave ID"] = self.slave_id_entry21.get()
        data_values_dict["Slave Name"] = self.slave_name.get()
        data_values_dict["Sensor ID"] = self.sensor_id_entry.get()
        data_list = []
        for key, value in data_values_dict.items():
            if value is None or value == '':
                data_list.append(key)
        if not data_list:  # Instead of 'data_list is []', use 'not data_list'
            return Utils.verify_entry(self, 2)
        else:
            messagebox.showerror(
                'Fields Empty', f'Error: {data_list} fields Empty')

    def show_sensor_slave_id_widget(self):

        for widgets in self.winfo_children():
            widgets.destroy()
        self.pack(fill="y")
        self.result_label = tk.Label(self, text="")
        self.result_label.grid(row=5, column=1, padx=10, pady=10, sticky="s")
        self.create_sensor_slave_id_widget()

    def generate_sensor_id(self):
        generated_id = ''.join(random.choices(
            string.ascii_uppercase + string.digits, k=4))
        print(generated_id)
        self.filled_generated_id = Utils.autofill_entry(self,
                                                        self.sensor_id_entry, generated_id)
        self.generate_id = self.filled_generated_id
        return generated_id

    def show_add_sensor_widget_new(self):

        for widgets in self.winfo_children():
            widgets.destroy()
        self.show_add_sensor_widget()
