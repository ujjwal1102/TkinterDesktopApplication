
import tkinter as tk
from tkinter import ttk
from .utils import Utils
from pymongo import MongoClient
from tkinter import messagebox


class AddActuator():
    def __init__(self):
        super().__init__()
        print('Add Sensor')

    def create_add_actuator_widget(self, slaveid_entry, modbusid_combobox):
        page_name_label = tk.Label(self, text="Add Actuator", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR, font=(
            "TkTextFont", 25), borderwidth=2, relief="solid", justify="center", padx=15, pady=5, highlightcolor="white", highlightbackground="red")

        page_name_label.grid(row=0, column=0, columnspan=5, pady=50)

        self.slave_id_label = tk.Label(
            self, text="Slave ID", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        self.slave_id_label.grid(
            row=1, column=0, padx=10, pady=10, sticky="ne")

        self.slave_id_entry = tk.Entry(self, width=25)
        self.slave_id_entry.grid(
            row=1, column=1, padx=10, pady=10, sticky="ne")
        self.slave_id_entry.delete(0, tk.END)

        self.slave_id_entry.insert(0, str(slaveid_entry))

        description_label = tk.Label(
            self, text="Description", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        description_label.grid(row=1, column=2, padx=10, pady=10, sticky="ne")

        self.description_text = tk.Entry(self, width=25)
        self.description_text.grid(
            row=1, column=3, padx=10, pady=10, sticky="ne")

        relay_label = tk.Label(self,
                               text="Relay Name", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        relay_label.grid(row=4, column=2, padx=10, pady=10, sticky="ne")
        self.relay_entry = tk.Entry(self, width=25)
        self.relay_entry.grid(
            row=4, column=3, padx=10, pady=10, sticky="ne")

        mod_label = tk.Label(self,
                             text="Modbus ID", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        mod_label.grid(row=6, column=0, padx=10, pady=10, sticky="ne")
        self.mod_entry = tk.Entry(self, width=25)
        self.mod_entry.grid(row=6, column=1, padx=10, pady=10, sticky="ne")
        self.mod_entry.delete(0, tk.END)
        self.mod_entry.insert(0, str(modbusid_combobox))

        flash_button = tk.Button(self, text="Flash", bg=Utils.BTN_COLOR, command=lambda: self.connect_to_com_port(
            self.get_modbus_data(modbusid_combobox), 1))
        flash_button.grid(row=8, column=1, padx=10,
                          columnspan=5, pady=20, sticky="W")

        delete_button = tk.Button(
            self, text="Delete", bg=Utils.BTN_COLOR)
        delete_button.grid(row=8, column=2, padx=10,
                           columnspan=5, pady=20, sticky="W")

        save_button = tk.Button(self, text="Save",
                                bg=Utils.BTN_COLOR, command=lambda: self.verify_all_entries())
        save_button.grid(row=8, column=3, padx=10,
                         columnspan=5, pady=20, sticky="W")
        export_button = tk.Button(self, text="Export")
        export_button.grid(row=8, column=4, padx=10,
                           columnspan=5, pady=20, sticky="W")

    def show_add_actuator_widget(self):
        slaveid_entry = self.slave_id_entry2.get()
        modbusid_combobox = self.modbus_id_combobox.get()
        self.channelid = self.channelid_entry.get()
        self.slavename = self.slave_name.get()
        for widgets in self.winfo_children():
            widgets.destroy()
        self.pack(fill="y")
        self.create_add_actuator_widget(slaveid_entry, modbusid_combobox)

    def data_values(self):

        data_values_dict = {}
        data_values_dict["Slave Name"] = self.slavename
        data_values_dict["Channel ID"] = self.channelid
        data_values_dict["Slave ID"] = self.slave_id_entry.get()
        data_values_dict["Description"] = self.description_text.get()
        data_values_dict["Modbus ID"] = self.mod_entry.get()
        data_values_dict["Relay Name"] = self.relay_entry.get()
        return data_values_dict

    def verify_all_entries(self):
        data_list = []
        data_values_dict = self.data_values()
        for key, value in data_values_dict.items():
            if value is None or value == '':
                data_list.append(key)
        if not data_list:
            return Utils.save_configuration(self, 3, data_values_dict)
        else:
            messagebox.showerror(
                'Fields Empty', f'Error: {data_list} fields Empty')
