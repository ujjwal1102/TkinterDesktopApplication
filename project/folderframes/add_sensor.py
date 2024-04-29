
import tkinter as tk
from tkinter import ttk
from .utils import Utils
from pymongo import MongoClient

from tkinter import messagebox
class AddSensor():
    def __init__(self,):
        super().__init__()
        print('Add Sensor')

    def create_add_sensor_widget(self,slave_id_entry21,modbus_id_combobox,generated_id ):
        page_name_label = tk.Label(self, text="Add Sensor", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR, font=(
            "TkTextFont", 25), borderwidth=2, relief="solid", justify="center", padx=15, pady=5, highlightcolor="white", highlightbackground="red")
        page_name_label.config()
        
        page_name_label.grid(row=0, column=0, columnspan=5, pady=50)
        
        sensor_type_label = tk.Label(
            self, text="Sensor Type", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        sensor_type_label.grid(row=2, column=0, padx=10, pady=10, sticky="ne")

        self.sensor_type_combobox = ttk.Combobox(self, values=[
                                                 "multivariate", "univariate"], width=22)
        self.sensor_type_combobox.grid(
            row=2, column=1, padx=10, pady=10, sticky="ne")

        self.slave_id_label = tk.Label(
            self, text="Slave ID", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        self.slave_id_label.grid(
            row=1, column=0, padx=10, pady=10, sticky="ne")

        self.slave_id_entry = tk.Entry(self, width=25)
        self.slave_id_entry.grid(
            row=1, column=1, padx=10, pady=10, sticky="ne")
        self.slave_id_entry.delete(0, tk.END)
        self.slave_id_entry.insert(0, str(slave_id_entry21))
        description_label = tk.Label(
            self, text="Description", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        description_label.grid(row=1, column=2, padx=10, pady=10, sticky="ne")

        self.description_text = tk.Entry(self, width=25)
        self.description_text.grid(
            row=1, column=3, padx=10, pady=10, sticky="ne")

        icon_file_label = tk.Label(
            self, text="icon file", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        icon_file_label.grid(row=2, column=2, padx=10, pady=10, sticky="ne")
        self.icon_file_entry = tk.Entry(self, width=25)
        self.icon_file_entry.grid(
            row=2, column=3, padx=10, pady=10, sticky="ne")

        num_count_label = tk.Label(
            self, text="Num Count", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        num_count_label.grid(row=3, column=2, padx=10, pady=10, sticky="ne")
        self.num_count_entry = tk.Entry(self, width=25)
        self.num_count_entry.grid(
            row=3, column=3, padx=10, pady=10, sticky="ne")

        subsensor_label = tk.Label(
            self, text="Subsensor", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        subsensor_label.grid(row=4, column=2, padx=10, pady=10, sticky="ne")
        self.subsensor_entry = tk.Entry(self, width=25)
        self.subsensor_entry.grid(
            row=4, column=3, padx=10, pady=10, sticky="ne")

        sensorname_label = tk.Label(
            self, text="Sensor name", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        sensorname_label.grid(row=3, column=0, padx=10, pady=10, sticky="ne")
        self.sensorname_entry = tk.Entry(self, width=25)
        self.sensorname_entry.grid(
            row=3, column=1, padx=10, pady=10, sticky="ne")

        sensoraddress_label = tk.Label(
            self, text="Sensor Address", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        sensoraddress_label.grid(
            row=4, column=0, padx=10, pady=10, sticky="ne")
        self.sensoraddress_entry = tk.Entry(self, width=25)
        self.sensoraddress_entry.grid(
            row=4, column=1, padx=10, pady=10, sticky="ne")

        ui_label = tk.Label(self,
                            text="UI placeholder", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        ui_label.grid(row=5, column=0, padx=10, pady=10, sticky="ne")
        self.ui_entry = tk.Entry(self, width=25)
        self.ui_entry.grid(row=5, column=1, padx=10, pady=10, sticky="ne")

        reg_label = tk.Label(self,
                             text="Register", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        reg_label.grid(row=5, column=2, padx=10, pady=10, sticky="ne")
        self.reg_entry = tk.Entry(self, width=25)
        self.reg_entry.grid(row=5, column=3, padx=10, pady=10, sticky="ne")

        mod_label = tk.Label(self,
                             text="Modbus ID", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        mod_label.grid(row=6, column=0, padx=10, pady=10, sticky="ne")
        self.mod_entry = tk.Entry(self, width=25)
        self.mod_entry.grid(row=6, column=1, padx=10, pady=10, sticky="ne")
        self.mod_entry.delete(0, tk.END)
        self.mod_entry.insert(0, str(modbus_id_combobox))
        refresh_button = tk.Button(
            self, text="Refresh", bg=Utils.BTN_COLOR)
        refresh_button.grid(row=8, column=0, padx=10,
                            columnspan=5, pady=20, sticky="W")

        sensorid_label = tk.Label(
            self, text="Sensor ID", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        sensorid_label.grid(row=6, column=2, padx=10, pady=10, sticky="ne")
        self.sensorid_entry = tk.Entry(self, width=25)
        self.sensorid_entry.grid(
            row=6, column=3, padx=10, pady=10, sticky="ne")
        # Utils.autofill_entry(self,self.sensorid_entry, generate_id)

        unit_label = tk.Label(
            self, text="Unit", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        unit_label.grid(row=7, column=0, padx=10, pady=10, sticky="ne")
        self.unit_entry = tk.Entry(self, width=25)
        self.unit_entry.grid(row=7, column=1, padx=10, pady=10, sticky="ne")

        browse_icon_file_button = tk.Button(
            self, text="Browse", bg=Utils.BTN_COLOR, command=lambda: self.open_current_working_directory())
        browse_icon_file_button.grid(
            row=2, column=4, padx=10, pady=10, sticky="ne")
        flash_button = tk.Button(self, text="Flash", bg=Utils.BTN_COLOR, command=lambda: self.connect_to_com_port(
            self.get_modbus_data(modbus_id_combobox), 1))
        flash_button.grid(row=8, column=1, padx=10,
                          columnspan=5, pady=20, sticky="W")
        delete_button = tk.Button(
            self, text="Delete", bg=Utils.BTN_COLOR)
        delete_button.grid(row=8, column=2, padx=10,
                           columnspan=5, pady=20, sticky="W")
        save_button = tk.Button(self, text="Save",
                                bg=Utils.BTN_COLOR, command=lambda: Utils.save_configuration(self,2,self.verify_all_entries()))
        save_button.grid(row=8, column=3, padx=10,
                         columnspan=5, pady=20, sticky="W")
        export_button = tk.Button(self, text="Export")
        export_button.grid(row=8, column=4, padx=10,
                           columnspan=5, pady=20, sticky="W")
    
    def show_add_sensor_widget(self):
        slave_id_entry21 = self.slave_id_entry21.get()
        modbus_id_combobox = self.modbus_id_combobox.get()
        generated_id = self.generate_id
        
        self.slavename = self.slave_name.get()
        self.pack(fill="y")
        for widgets in self.winfo_children():
            widgets.destroy()
        self.create_add_sensor_widget(slave_id_entry21,modbus_id_combobox,generated_id)

    def data_values(self) -> dict:  
        data_values_dict = {}
        data_values_dict["Sensor Type"] = self.sensor_type_combobox.get()
        data_values_dict["Slave ID"] = self.slave_id_entry.get()
        data_values_dict["Description"] = self.description_text.get()
        data_values_dict["icon file"] = self.icon_file_entry.get()
        data_values_dict["Sensor Address"] = self.sensoraddress_entry.get()
        data_values_dict["Num Count"] = self.num_count_entry.get()
        data_values_dict["Subsensor"] = self.subsensor_entry.get()
        data_values_dict["Sensor name"] = self.sensorname_entry.get()
        data_values_dict["UI placeholder"] = self.ui_entry.get()
        data_values_dict["Register"] = self.reg_entry.get()
        data_values_dict["Modbus ID"] = self.mod_entry.get()
        data_values_dict["Slave Name"] = self.slavename
        data_values_dict["Sensor ID"] = self.sensorid_entry.get()
        data_values_dict["Unit"] = self.unit_entry.get()
        print("data_values_dict : ",data_values_dict)
        return data_values_dict
        
    def verify_all_entries(self):
        data_list = []
        data_values_dict = self.data_values()  # Call the function to get the dictionary
        for key, value in data_values_dict.items():
            if value is None or value == '':
                data_list.append(key)
        if not data_list:  # Instead of 'data_list is []', use 'not data_list'
            return data_values_dict
        else:
            messagebox.showerror('Fields Empty', f'Error: {data_list} fields Empty')

        