

import tkinter as tk
from tkinter import ttk
from .utils import Utils
from pymongo import MongoClient
from tkinter import messagebox

class Mapping(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        print('Add Sensor')
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['modbus']
        self.Rcollection = self.db['slave range']
    def update_Rdocument(self, sensorid, actid):  # , updated_data):
        client = MongoClient("mongodb://localhost:27017/")
        db = client["modbus"]
        collection = db["configurations"]
        Adoc = collection.find_one({"slave_id": actid})
        if Adoc:
            channelid = Adoc.get("channel_id", 0)
            modbusid = Adoc.get("modbus_id", 0)
        mapped = [{"mapped": actid, "channel_id": channelid,
                   "act_modbus_id": modbusid}]
        updated_data = {
            "mapped": mapped,
        }
        # Update the document in MongoDB
        collection.update_one({"slave_id": sensorid}, {"$set": updated_data})

        #    collection = db["configurations"]
        Sdoc = collection.find_one({"slave_id": sensorid})
        if Sdoc:
            sensorname = Sdoc.get("sensor name", 0)
            modbusid = Sdoc.get("modbus_id", 0)
        mapped = [{"sensor_slave_id": sensorid,
                   "sensor_modbus_id": modbusid, "sensor_name": sensorname}]
        updated_data = {
            "mapped": mapped,
        }
        # Update the document in MongoDB
        collection.update_one({"slave_id": actid}, {"$set": updated_data})
        messagebox.showinfo("Updated", "Configuration Mapped successfully!")


    def create_mapping_widget(self):
        page_name_label = tk.Label(self, text="Mapping", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR, font=(
            "TkTextFont", 25), borderwidth=2, relief="solid", justify="center", padx=15, pady=5, highlightcolor="white", highlightbackground="red")
        page_name_label.grid(row=0, column=0, columnspan=5, pady=50)

        client = MongoClient("mongodb://localhost:27017/")
        db = client["modbus"]
        collection = db["configurations"]
        available_ids = set(str(doc["modbus_id"]) for doc in collection.find({}, {"modbus_id": 1}))
        available_ids = list(available_ids)

        Smodbus_id_label = tk.Label(self, text="Sensor Modbus ID:", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        Smodbus_id_label.grid(row=1, column=0, padx=10, pady=10, sticky="ne")

        Amodbus_id_label = tk.Label(self, text="Actuator Modbus ID:", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        Amodbus_id_label.grid(row=1, column=2, padx=10, pady=10, sticky="ne")

        self.Smodbus_id_combobox = ttk.Combobox(self, width=20, values=available_ids)
        self.Smodbus_id_combobox.grid(row=1, column=1, padx=10, pady=10, sticky="ne")
        self.Amodbus_id_combobox = ttk.Combobox(self, width=20, values=available_ids)
        self.Amodbus_id_combobox.grid(row=1, column=3, padx=10, pady=10, sticky="ne")

        def update_sensor_ids(event):
            selected_modbus_id = self.Smodbus_id_combobox.get()
            mapped_slave_ids = []
            cursor = collection.find({"modbus_id": selected_modbus_id})
            for document in cursor:
                mapped_slave_ids.append(document.get("slave_id"))
            self.Sslave_name['values'] = mapped_slave_ids  # Update the Sensor ID combobox values
        def update_actuator_ids(event):
            selected_modbus_id = self.Amodbus_id_combobox.get()
            mapped_slave_ids = []
            cursor = collection.find({"modbus_id": selected_modbus_id})
            for document in cursor:
                mapped_slave_ids.append(document.get("slave_id"))
            self.Aslave_name['values'] = mapped_slave_ids  # Update the Sensor ID combobox values

        self.Smodbus_id_combobox.bind("<<ComboboxSelected>>", update_sensor_ids)
        self.Amodbus_id_combobox.bind("<<ComboboxSelected>>", update_actuator_ids)

        Smapped_slave_ids = []
        Scursor = collection.find({"modbus_id": str(self.Smodbus_id_combobox.get())})
        for document in Scursor:
            Smapped_slave_ids.append(document.get("slave_id"))
        print(Smapped_slave_ids)

        slave_ids = collection.distinct("slave_id")

        Sslave_name_label = tk.Label(self, text="Sensor ID", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        Sslave_name_label.grid(row=2, column=0, padx=10, pady=10, sticky="ne")
        self.Sslave_name = ttk.Combobox(self, width=20, values=Smapped_slave_ids)
        self.Sslave_name.grid(row=2, column=1, padx=10, pady=10, sticky="ne")
        Aslave_name_label = tk.Label(self, text="Actuator ID", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        Aslave_name_label.grid(row=2, column=2, padx=10, pady=10, sticky="ne")
        self.Aslave_name = ttk.Combobox(self, width=20, values=slave_ids)
        self.Aslave_name.grid(row=2, column=3, padx=10, pady=10, sticky="ne")

        verify_uniqueness = tk.Button(self, text="Map", bg=Utils.BTN_COLOR,
                                    command=lambda: self.update_Rdocument(self.Sslave_name.get(), self.Aslave_name.get()))

        verify_uniqueness.grid(row=4, column=1, padx=5, pady=50, sticky="S")


        
        
    def show_mapping_widget(self):
        self.pack(fill="y")
        self.create_mapping_widget()
