
import tkinter as tk
from tkinter import ttk
from .utils import Utils
from pymongo import MongoClient

from tkinter import messagebox
class AddModbus():
    def __init__(self):
        super().__init__()
        print('Add Modbus')

    def create_add_modbus_widget(self, modbusid_entry2, modbusname2):

        page_name_label = tk.Label(self, text="Add Modbus", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR, font=(
            "TkTextFont", 25), borderwidth=2, relief="solid", justify="center", padx=15, pady=5, highlightcolor="white", highlightbackground="red")
        # page_name_label.pack(fill="x",side="top",ipadx=5,ipady=15)
        page_name_label.grid(row=0, column=0, columnspan=5, pady=50)

        self.modbus_id_label = tk.Label(
            self, text="Modbus ID", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        self.modbus_id_entry = tk.Entry(self, width=25)

        self.modbus_name_label = tk.Label(
            self, text="Modbus Name", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        self.modbus_name = tk.Entry(self, width=25)
        self.modbus_id_entry.delete(0, tk.END)
        self.modbus_id_entry.insert(
            0, str(modbusid_entry2)+"-"+str(modbusname2))
        self.modbus_name.delete(0, tk.END)
        self.modbus_name.insert(0, modbusname2)
        self.baud_rate_label = tk.Label(
            self, text="Baud Rate", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        self.baud_rate_entry = tk.Entry(self, width=25)

        self.max_tries_label = tk.Label(
            self, text="Max Tries", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        self.max_tries_entry = tk.Entry(self, width=25)

        self.slave_id_range_label = tk.Label(
            self, text="Slave Id Range", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        self.slave_id_range_button = tk.Button(self, text="Add", bg=Utils.BTN_COLOR,
                                               command=lambda name="AddRange": self.show_frame(name))  # , command=self.add_range)

        self.parity_label = tk.Label(
            self, text="Parity", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        self.parity_entry = tk.Entry(self, width=25)

        self.average_label = tk.Label(
            self, text="Averaging values(in secs)", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        self.average_entry = tk.Entry(self, width=25)

        self.timer_label = tk.Label(
            self, text="Timer", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        self.timer_entry = tk.Entry(self, width=25)

        self.timeout_label = tk.Label(
            self, text="Timeout", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        self.timeout_entry = tk.Entry(self, width=25)

        self.stop_bits_label = tk.Label(
            self, text="Stop Bits", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        self.stop_bits_entry = tk.Entry(self, width=25)

        self.poll_frequency_label = tk.Label(
            self, text="Poll Frequency", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        self.poll_frequency_entry = tk.Entry(self, width=25)

        self.delete_button = tk.Button(
            self, text="Delete", bg=Utils.BTN_COLOR)
        self.save_button = tk.Button(
            self, text="Save", bg=Utils.BTN_COLOR, command=lambda: self.verify_all_entries())
        self.export_button = tk.Button(
            self, text="Export", bg=Utils.BTN_COLOR)

        self.modbus_id_label.grid(
            row=1, column=0, padx=10, pady=10, sticky="ne")
        self.modbus_id_entry.grid(
            row=1, column=1, padx=10, pady=10, sticky="ne")

        self.modbus_name_label.grid(
            row=2, column=0, padx=10, pady=10, sticky="ne")
        self.modbus_name.grid(row=2, column=1, padx=10, pady=10, sticky="ne")

        self.baud_rate_label.grid(
            row=3, column=0, padx=10, pady=10, sticky="ne")
        self.baud_rate_entry.grid(
            row=3, column=1, padx=10, pady=10, sticky="ne")

        self.max_tries_label.grid(
            row=4, column=0, padx=10, pady=10, sticky="ne")
        self.max_tries_entry.grid(
            row=4, column=1, padx=10, pady=10, sticky="ne")

        self.slave_id_range_label.grid(
            row=5, column=0, padx=10, pady=10, sticky="ne")
        self.slave_id_range_button.grid(
            row=5, column=1, padx=10, pady=10, sticky="W")

        self.parity_label.grid(row=1, column=2, padx=10, pady=10, sticky="ne")
        self.parity_entry.grid(row=1, column=3, padx=10, pady=10, sticky="ne")

        self.timeout_label.grid(row=2, column=2, padx=10, pady=10, sticky="ne")
        self.timeout_entry.grid(row=2, column=3, padx=10, pady=10, sticky="ne")

        self.stop_bits_label.grid(
            row=3, column=2, padx=10, pady=10, sticky="ne")
        self.stop_bits_entry.grid(
            row=3, column=3, padx=10, pady=10, sticky="ne")

        self.poll_frequency_label.grid(
            row=4, column=2, padx=10, pady=10, sticky="ne")
        self.poll_frequency_entry.grid(
            row=4, column=3, padx=10, pady=10, sticky="ne")

        self.average_label.grid(row=5, column=2, padx=10, pady=10, sticky="ne")
        self.average_entry.grid(row=5, column=3, padx=10, pady=10, sticky="ne")

        self.timer_label.grid(row=6, column=2, padx=10, pady=10, sticky="ne")
        self.timer_entry.grid(row=6, column=3, padx=10, pady=10, sticky="ne")

        self.delete_button.grid(row=7, column=1, padx=10, pady=10, sticky="ne")
        self.save_button.grid(row=7, column=2, padx=10, pady=10, sticky="ne")
        self.export_button.grid(row=7, column=4, padx=10, pady=10, sticky="ne")


    def show_add_modbus_widget(self):
        self.modbusid_entry2 = self.modbus_id_entry2.get()
        self.modbusname2 = self.modbus_name2.get()
        for widgets in self.winfo_children():
            widgets.destroy()
        self.pack(fill="y")

        self.create_add_modbus_widget(self.modbusid_entry2, self.modbusname2)

    def data_values(self):
        data_values_dict = {}
        data_values_dict["Modbus ID"] = self.modbus_id_entry.get()
        data_values_dict["Modbus Name"] = self.modbus_name.get()
        data_values_dict["Baud Rate"] = self.baud_rate_entry.get()
        data_values_dict["Max Tries"] = self.max_tries_entry.get()
        data_values_dict["Parity"] = self.parity_entry.get()
        data_values_dict["Averaging values(in secs)"] = self.average_entry.get(
        )
        data_values_dict["Timer"] = self.timer_entry.get()
        data_values_dict["Timeout"] = self.timeout_entry.get()
        data_values_dict["Stop Bits"] = self.stop_bits_entry.get()
        data_values_dict["Poll Frequency"] = self.poll_frequency_entry.get()

        return data_values_dict

    def verify_all_entries(self):
        data_list = []
        data_values_dict = self.data_values()  # Call the function to get the dictionary
        for key, value in data_values_dict.items():
            if value is None or value == '':
                data_list.append(key)
        if not data_list:  # Instead of 'data_list is []', use 'not data_list'
            return Utils.save_configuration(self, 1, data_values_dict) 
        else:
            messagebox.showerror('Fields Empty', f'Error: {data_list} fields Empty')