

import tkinter as tk
from tkinter import ttk
from .utils import Utils
from pymongo import MongoClient
from tkinter import messagebox


class ModbusSetting(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        print('Modbus_setting')
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['modbus']
        self.Rcollection = self.db['slave range']

    def create_modbussetting_widget(self):

        client = MongoClient("mongodb://localhost:27017/")
        db = client["modbus"]
        collection = db["configurations"]
        available_ids = set(str(doc["modbus_id"])
                            for doc in collection.find({}, {"modbus_id": 1}))
        available_ids = list(available_ids)
        page_name_label = tk.Label(self, text="Modus Setting", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR, font=(
            "TkTextFont", 25), borderwidth=2, relief="solid", justify="center", padx=15, pady=5, highlightcolor="white", highlightbackground="red")

        modbus_id_label = tk.Label(
            self, text="Select Modbus ID:", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        self.modbus_id_combobox = ttk.Combobox(
            self, width=20, values=available_ids)
        self.modbus_id_combobox.grid(
            row=1, column=1, padx=(10, 5), pady=10, sticky="ne")
        modbus_id_label.grid(row=1, column=0, padx=10, pady=10, sticky="ne")
        # page_name_label.pack(fill="x",side="top",ipadx=5,ipady=15)
        page_name_label.grid(row=0, column=0, columnspan=5, pady=50)
        self.Amodbutton = tk.Button(self, text="Search", bg=Utils.BTN_COLOR,
                                    command=lambda: self.fill_form(self.modbus_id_combobox.get()))
        self.Amodbutton.grid(row=1, column=2, padx=(
            5, 10), pady=10, sticky="ne")

        self.modbus_id_label = tk.Label(
            self, text="Modbus ID", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        self.modbus_id_entry = tk.Entry(self, width=25)

        self.modbus_name_label = tk.Label(
            self, text="Modbus Name", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        self.modbus_name = tk.Entry(self, width=25)
        self.empty = tk.Label(self, text=" ",
                              bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        self.empty.grid(row=2, column=2, padx=20, pady=10, sticky="ne")

        self.baud_rate_label = tk.Label(
            self, text="Baud Rate", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        self.baud_rate_entry = tk.Entry(self, width=25)

        self.max_tries_label = tk.Label(
            self, text="Max Tries", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        self.max_tries_entry = tk.Entry(self, width=25)

        self.slave_id_range_label = tk.Label(
            self, text="Slave Id Range", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        # self.slave_id_range_button = tk.Button(self, text="Add", bg=Utils.BTN_COLOR,
        #                                        command=lambda name="AddRange": self.show_frame(name))  # , command=self.add_range)

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
            self, text="Update", bg=Utils.BTN_COLOR, command=lambda: self.update_modbus(1))
        self.export_button = tk.Button(
            self, text="Export", bg=Utils.BTN_COLOR)

        self.modbus_id_label.grid(
            row=3, column=0, padx=10, pady=10, sticky="ne")
        self.modbus_id_entry.grid(
            row=3, column=1, padx=10, pady=10, sticky="ne")

        self.baud_rate_label.grid(
            row=4, column=0, padx=10, pady=10, sticky="ne")
        self.baud_rate_entry.grid(
            row=4, column=1, padx=10, pady=10, sticky="ne")

        self.max_tries_label.grid(
            row=5, column=0, padx=10, pady=10, sticky="ne")
        self.max_tries_entry.grid(
            row=5, column=1, padx=10, pady=10, sticky="ne")

        self.slave_id_range_label.grid(
            row=7, column=0, padx=10, pady=10, sticky="ne")
     #   self.slave_id_range_button.grid(
      #      row=7, column=1, padx=10, pady=10, sticky="W")

        self.parity_label.grid(row=7, column=2, padx=10, pady=10, sticky="ne")
        self.parity_entry.grid(row=7, column=3, padx=10, pady=10, sticky="ne")

        self.timeout_label.grid(row=6, column=0, padx=10, pady=10, sticky="ne")
        self.timeout_entry.grid(row=6, column=1, padx=10, pady=10, sticky="ne")

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

        self.delete_button.grid(row=8, column=1, padx=10, pady=10, sticky="ne")
        self.save_button.grid(row=8, column=2, padx=10, pady=10, sticky="ne")
        self.export_button.grid(row=8, column=3, padx=10, pady=10, sticky="ne")

    def update_modbus(self, dev):
        client = MongoClient("mongodb://localhost:27017/")
        db = client["modbus"]
        collection = db["configurations"]
        modbus_id = self.modbus_id_entry.get()
        baud_rate = self.baud_rate_entry.get()
        max_tries = self.max_tries_entry.get()
        parity = self.parity_entry.get()
        timeout = self.timeout_entry.get()
        stop_bits = self.stop_bits_entry.get()
        poll_frequency = self.poll_frequency_entry.get()
        average = self.average_entry.get()
        timer = self.timer_entry.get()

        query = {"modbus_id": modbus_id}
        update_data = {
            "$set": {
                "baud_rate": baud_rate,
                "max_tries": max_tries,
                "parity": parity,
                "timeout": timeout,
                "stop_bits": stop_bits,
                "poll_frequency": poll_frequency
            }}
        collection.update_one(query, update_data)
        messagebox.showinfo("Updated", "Configuration updated successfully!")

    
    def fill_form(self, type):
        client = MongoClient("mongodb://localhost:27017/")
        db = client["modbus"]
        collection = db["configurations"]

        document = collection.find_one({"modbus_id": type})
        if document:
            modbus_id = document["modbus_id"]
            baud_rate = document.get("baud_rate", 0)
            parity = document.get("parity", 0)
            stop_bits = document.get("stop_bits", 0)
            timeout = document.get("timeout", 0)
            max_tries = document.get("max_tries", 0)
            poll_frequency = document.get("poll_frequency", 0)
            average = document.get("average", 0)
            timer = document.get("timer", 0)
        print(timeout)
        print(baud_rate)
        print(parity)
        self.modbus_id_entry.delete(0, tk.END)
        self.modbus_id_entry.insert(0, modbus_id)
        self.baud_rate_entry.delete(0, tk.END)
        self.baud_rate_entry.insert(0, baud_rate)
        self.max_tries_entry.delete(0, tk.END)
        self.max_tries_entry.insert(0, max_tries)
        self.parity_entry.delete(0, tk.END)
        self.parity_entry.insert(0, parity)
        self.timeout_entry.delete(0, tk.END)
        self.timeout_entry.insert(0, timeout)
        self.stop_bits_entry.delete(0, tk.END)
        self.stop_bits_entry.insert(0, stop_bits)
        self.poll_frequency_entry.delete(0, tk.END)
        self.poll_frequency_entry.insert(0, poll_frequency)
        self.average_entry.delete(0, tk.END)
        self.average_entry.insert(0, average)
        self.timer_entry.delete(0, tk.END)
        self.timer_entry.insert(0, timer)

    
    def create_add_sensor_widget(self):
        page_name_label = tk.Label(self.add_sensor_frame, text="Add Sensor", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR, font=(
            "TkTextFont", 25), borderwidth=2, relief="solid", justify="center", padx=15, pady=5, highlightcolor="white", highlightbackground="red")
        page_name_label.config()
        # page_name_label.pack(fill="x",side="top",ipadx=5,ipady=15)
        page_name_label.grid(row=0, column=0, columnspan=5, pady=50)
        self.goback_button.grid_remove()
        sensor_type_label = tk.Label(
            self.add_sensor_frame, text="Sensor Type", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        sensor_type_label.grid(row=2, column=0, padx=10, pady=10, sticky="ne")

        self.sensor_type_combobox = ttk.Combobox(self.add_sensor_frame, values=[
                                                 "multivariate", "univariate"], width=22)
        self.sensor_type_combobox.grid(
            row=2, column=1, padx=10, pady=10, sticky="ne")

        self.slave_id_label = tk.Label(
            self.add_sensor_frame, text="Slave ID", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        self.slave_id_label.grid(
            row=1, column=0, padx=10, pady=10, sticky="ne")

        self.slave_id_entry = tk.Entry(self.add_sensor_frame, width=25)
        self.slave_id_entry.grid(
            row=1, column=1, padx=10, pady=10, sticky="ne")
        self.slave_id_entry.delete(0, tk.END)

        self.slave_id_entry.insert(0, str(self.slave_id_entry21.get()))

        description_label = tk.Label(
            self.add_sensor_frame, text="Description", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        description_label.grid(row=1, column=2, padx=10, pady=10, sticky="ne")

        self.description_text = tk.Entry(self.add_sensor_frame, width=25)
        self.description_text.grid(
            row=1, column=3, padx=10, pady=10, sticky="ne")

        icon_file_label = tk.Label(
            self.add_sensor_frame, text="icon file", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        icon_file_label.grid(row=2, column=2, padx=10, pady=10, sticky="ne")
        self.icon_file_entry = tk.Entry(self.add_sensor_frame, width=25)
        self.icon_file_entry.grid(
            row=2, column=3, padx=10, pady=10, sticky="ne")

        num_count_label = tk.Label(
            self.add_sensor_frame, text="Num Count", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        num_count_label.grid(row=3, column=2, padx=10, pady=10, sticky="ne")
        self.num_count_entry = tk.Entry(self.add_sensor_frame, width=25)
        self.num_count_entry.grid(
            row=3, column=3, padx=10, pady=10, sticky="ne")

        subsensor_label = tk.Label(
            self.add_sensor_frame, text="Subsensor", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        subsensor_label.grid(row=4, column=2, padx=10, pady=10, sticky="ne")
        self.subsensor_entry = tk.Entry(self.add_sensor_frame, width=25)
        self.subsensor_entry.grid(
            row=4, column=3, padx=10, pady=10, sticky="ne")

        sensorname_label = tk.Label(
            self.add_sensor_frame, text="Sensor name", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        sensorname_label.grid(row=3, column=0, padx=10, pady=10, sticky="ne")
        self.sensorname_entry = tk.Entry(self.add_sensor_frame, width=25)
        self.sensorname_entry.grid(
            row=3, column=1, padx=10, pady=10, sticky="ne")

        sensoraddress_label = tk.Label(
            self.add_sensor_frame, text="Sensor Address", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        sensoraddress_label.grid(
            row=4, column=0, padx=10, pady=10, sticky="ne")
        self.sensoraddress_entry = tk.Entry(self.add_sensor_frame, width=25)
        self.sensoraddress_entry.grid(
            row=4, column=1, padx=10, pady=10, sticky="ne")

        ui_label = tk.Label(self.add_sensor_frame,
                            text="UI placeholder", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        ui_label.grid(row=5, column=0, padx=10, pady=10, sticky="ne")
        self.ui_entry = tk.Entry(self.add_sensor_frame, width=25)
        self.ui_entry.grid(row=5, column=1, padx=10, pady=10, sticky="ne")

        reg_label = tk.Label(self.add_sensor_frame,
                             text="Register", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        reg_label.grid(row=5, column=2, padx=10, pady=10, sticky="ne")
        self.reg_entry = tk.Entry(self.add_sensor_frame, width=25)
        self.reg_entry.grid(row=5, column=3, padx=10, pady=10, sticky="ne")

        mod_label = tk.Label(self.add_sensor_frame,
                             text="Modbus ID", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        mod_label.grid(row=6, column=0, padx=10, pady=10, sticky="ne")
        self.mod_entry = tk.Entry(self.add_sensor_frame, width=25)
        self.mod_entry.grid(row=6, column=1, padx=10, pady=10, sticky="ne")
        self.mod_entry.delete(0, tk.END)
        self.mod_entry.insert(0, str(self.modbus_id_combobox.get()))
        refresh_button = tk.Button(
            self.add_sensor_frame, text="Refresh", bg=Utils.BTN_COLOR)
        refresh_button.grid(row=8, column=0, padx=10,
                            columnspan=5, pady=20, sticky="W")

        sensorid_label = tk.Label(
            self.add_sensor_frame, text="Sensor ID", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        sensorid_label.grid(row=6, column=2, padx=10, pady=10, sticky="ne")
        self.sensorid_entry = tk.Entry(self.add_sensor_frame, width=25)
        self.sensorid_entry.grid(
            row=6, column=3, padx=10, pady=10, sticky="ne")
        self.autofill_entry(self.sensorid_entry,  self.sensor_id_entry.get())

        unit_label = tk.Label(self.add_sensor_frame,
                              text="Unit", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        unit_label.grid(row=7, column=0, padx=10, pady=10, sticky="ne")
        self.unit_entry = tk.Entry(self.add_sensor_frame, width=25)
        self.unit_entry.grid(row=7, column=1, padx=10, pady=10, sticky="ne")

        browse_icon_file_button = tk.Button(
            self.add_sensor_frame, text="Browse", bg=Utils.BTN_COLOR, command=lambda: self.open_current_working_directory())
        browse_icon_file_button.grid(
            row=2, column=4, padx=10, pady=10, sticky="ne")

        flash_button = tk.Button(self.add_sensor_frame, text="Flash", bg=Utils.BTN_COLOR, command=lambda: self.connect_to_com_port(
            self.get_modbus_data(self.modbus_id_combobox.get()), 1))
        flash_button.grid(row=8, column=1, padx=10,
                          columnspan=5, pady=20, sticky="W")

        delete_button = tk.Button(
            self.add_sensor_frame, text="Delete", bg=Utils.BTN_COLOR)
     #   delete_button.grid(row=8, column=2, padx=10,
      #                     columnspan=5, pady=20, sticky="W")

        save_button = tk.Button(self.add_sensor_frame, text="Save",
                                bg=Utils.BTN_COLOR, command=lambda: self.save_configuration(2))
        save_button.grid(row=8, column=3, padx=10,
                         columnspan=5, pady=20, sticky="W")
        export_button = tk.Button(self.add_sensor_frame, text="Export", bg=Utils.BTN_COLOR)

    
    
    def show_modbussetting_widget(self):
        self.pack(fill="y")
        self.create_modbussetting_widget()
