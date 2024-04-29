import tkinter as tk
import random
import uuid
from tkinter import messagebox
from pymongo import MongoClient
import random
import time
from tkinter import filedialog


BG_COLOR = '#0F054C'
FONT_COLOR = '#F6F6F6'
BTN_COLOR = "#61CE70"


class Utils:
    BG_COLOR = '#0F054C'
    FONT_COLOR = '#F6F6F6'
    BTN_COLOR = "#61CE70"

    def __init__(self) -> None:
        self.filled_generated_id = None

    def autofill_entry(self, entry, value):
        print(entry, value)
        entry.delete(0, tk.END)
        entry.insert(0, value)

    def gen_id(self, device):
        
        if device == 1:
            print('device 1')
            uid = uuid.uuid4().int & 0xFFFF
            uid_hex = hex(uid)[2:].zfill(4)
            
            self.modbus_id_entry2.delete(0, tk.END)
            self.modbus_id_entry2.insert(0, uid_hex)
            
        if device == 2:
            print('device 2')
            range = self.slave_name.get()
            data = self.Rcollection.find_one({"sensor": range})
            print("sensor range", range)
            if data:
                range_start = data["range_start"]
                range_end = data["range_end"]
                print("range_start",range_start,"range_end",range_end,self.result_label)
                print(self.result_label)
                self.result_label.config(
                    text=f"Start: {range_start}, End: {range_end}")
                genid = random.randint(range_start, range_end)
                uid_hex = format(genid, '02x')
                
                self.slave_id_entry21.delete(0, tk.END)
                self.slave_id_entry21.insert(0, uid_hex)
            else:
                self.result_label.config(text="Sensor data not found")

        if device == 3:
            print('device 3')
            genid = random.randint(0, 255)
            uid_hex = format(genid, '02x')
            Utils.autofill_entry(self, self.slave_id_entry2, uid_hex)

    def verify_entry(self, device):

        client = MongoClient("mongodb://localhost:27017/")
        db = client["modbus"]
        if device == 1:
            collection = db["configurations"]
            existing_document = collection.find_one({"modbus_id": str(
                self.modbus_id_entry2.get())+"-"+str(self.modbus_name2.get())})
            existing_name = collection.find_one(
                {"modbus_name": self.modbus_name2.get()})

            self.available_ids = [str(doc["modbus_id"])
                                  for doc in collection.find({}, {"modbus_id": 1})]
            if existing_document or existing_name:
                messagebox.showerror(
                    "Uniqueness Verification", "The Modbus ID or name is not unique. Please enter a unique Modbus ID and name.")
            else:

                self.goback_button = tk.Button(self, text="Go to form", bg=BTN_COLOR,
                                               command=lambda name="AddModbus": self.show_add_modbus_widget(), justify="center")
                self.goback_button.grid(
                    row=4, column=1, padx=10, pady=10, sticky="W"+"E"+"N"+"S")
                print('Device 1')
                messagebox.showinfo("Uniqueness Verification",
                                    "The configuration is unique!")

       # print(genid)
        elif device == 2:
            collection = db["configurations"]
            # self.num_count_entry_data = self.num_count_entry.get()
            existing_document = collection.find_one(
                {"slave_id": self.slave_id_entry21.get()})
            existing_name = collection.find_one(
                {"sensor name": self.slave_name.get()})

            existing_sensorid = collection.find_one(
                {"sensor_id":  str(self.filled_generated_id)})
        #    print(existing_sensorid)
            data = collection.find_one(
                {"modbus_id": self.modbus_id_combobox.get()})

            mycheck = None
            print('existing_sensorid : ', existing_sensorid)
            if existing_document or existing_sensorid:

                check = 1
                print('Check : ', check)
            else:
                check = 0
                print('Check else : ', check)

            print('existing_document: ', existing_document)
            print('existing_sensorid: ', existing_sensorid)
            if check:
                messagebox.showerror(
                    "Uniqueness Verification", "The Modbus ID or name or Sensor ID is not unique. Please enter a unique Modbus ID and name.")
            else:
                self.goback_button = tk.Button(
                    self, text="Go to form", bg=BTN_COLOR, command=lambda name="AddSensor": self.show_add_sensor_widget(), justify="center")
                self.goback_button.grid(
                    row=5, column=1, padx=10, pady=10, sticky="W"+"E"+"N"+"S")
                print('Device 2')
                messagebox.showinfo("Uniqueness Verification",
                                    "The configuration is unique!")

        # Check if the Modbus ID exists in the database
        elif device == 3:
            collection = db["configurations"]
            existing_document = collection.find_one(
                {"slave_id": self.slave_id_entry2.get(), "modbus_id": self.modbus_id_combobox.get()})
            if existing_document is not None:
                messagebox.showerror(
                    "Uniqueness Verification", "The Modbus ID or name or Sensor ID is not unique. Please enter a unique Modbus ID and name.")
            else:

                self.goback_button = tk.Button(self, text="Go to form",
                                               command=lambda name="AddActuator": self.show_add_actuator_widget(), justify="center")
                self.goback_button.grid(
                    row=7, column=1, padx=10, pady=10, sticky="W"+"E"+"N"+"S")
                print('Device 2')
                messagebox.showinfo("Uniqueness Verification",
                                    "The configuration is unique!")

    def save_configuration(self, device, data_values_dict):
        if device == 1:
            modbus_id = self.modbus_id_entry.get()
            baud_rate = self.baud_rate_entry.get()
            max_tries = self.max_tries_entry.get()
            parity = self.parity_entry.get()
            timeout = self.timeout_entry.get()
            stop_bits = self.stop_bits_entry.get()
            poll_frequency = self.poll_frequency_entry.get()


            client = MongoClient("mongodb://localhost:27017/")
            db = client["modbus"]
            collection = db["configurations"]
            base_configuration = db['base_configurations']

            existing_config = collection.find_one({"modbus_id": modbus_id})

            if existing_config:
                messagebox.showerror(
                    "Save", "The Modbus ID already exists. Please enter a unique Modbus ID.")
            else:
                configuration = {
                    "modbus_id": modbus_id,
                    "baud_rate": baud_rate,
                    "max_tries": max_tries,
                    "parity": parity,
                    "timeout": timeout,
                    "stop_bits": stop_bits,
                    "poll_frequency": poll_frequency
                }

                # Insert the configuration document into the database
                collection.insert_one(configuration)
                base_configuration.insert_one(configuration)

                messagebox.showinfo(
                    "Save", "Configuration saved successfully!")
        if device == 2 or device == 3:
            print("ddata_values_dict",data_values_dict)
            slave_id = data_values_dict["Slave ID"] 
            Description = data_values_dict["Description"]
            if device == 2:
                sensortype = self.sensor_type_combobox.get()
            client = MongoClient("mongodb://localhost:27017/")
            db = client["modbus"]
            collection = db["configurations"]
            base_configuration = db['base_configurations']
            Rcollection = db["slave range"]
            existing_config = collection.find_one({"slave_id": slave_id})
            documents = Rcollection.find({"sensor": data_values_dict["Slave Name"]})
            if existing_config:
                messagebox.showerror(
                    "Save", "The Modbus ID already exists. Please enter a unique Modbus ID.")
            else:
                if device == 2:
                    ranges = []

                    subsensor = [
                        {"subsensor": data_values_dict["Subsensor"], "unit": data_values_dict["Unit"]}]
                    for document in documents:
                        #  ranges.append(document)
                        range_start = document.get("range_start")
                        ranges.append({"range_start": int(range_start)})
                        range_end = document.get("range_end")
                        ranges.append({"range_start": int(range_end)})
                    # Create a new configuration document
                    configuration = {
                        "slave_type": data_values_dict["Sensor Type"],
                        "slave_id": data_values_dict["Slave ID"],
                        "icon_file": data_values_dict["icon file"],
                        "num_count": data_values_dict["Num Count"],
                        "register": data_values_dict["Register"],
                        "sensor_id": data_values_dict["Slave ID"],
                        "sensor name": data_values_dict["Slave Name"],
                        "modbus_id": data_values_dict["Modbus ID"],
                        "description": data_values_dict["Description"],
                        "Ranges": ranges,  # - i want to add that fetched data here
                        "subsensors": subsensor,  # array will be there to add in mongodb
                        "ui_placeholder": data_values_dict["UI placeholder"],
                        "slave_address": data_values_dict["Sensor Address"],
                        "time": time.time()

                    }

                    collection.insert_one(configuration)
                    base_configuration.insert_one(configuration)
                    messagebox.showinfo("Save", "Configuration saved")

                if device == 3:
                    configuration = {
                        #  "slave_type": sensortype,
                        "slave_id": data_values_dict["Slave ID"],
                        "channel_id": data_values_dict["Channel ID"],
                        "relay_name": data_values_dict["Relay Name"],

                        "modbus_id": data_values_dict["Modbus ID"],
                        "description": data_values_dict["Description"],


                    }

                    # Insert the configuration document into the database
                    collection.insert_one(configuration)
                    base_configuration.insert_one(configuration)
                    messagebox.showinfo("Save", "Configuration saved")
