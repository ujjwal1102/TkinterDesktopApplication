
import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient
from .utils import Utils


class AddRange(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.result_label = tk.Label(self, text="")
        self.result_label.pack()
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['modbus']

        self.Rcollection = self.db['slave range']
        self.sensor_list = self.updated_tree_table(
            list(self.Rcollection.find()))
        self.base_Rcollection = self.db['base_slave_range']
        self.base_configuration = self.client['base_configurations']
        print('Add Range Frame')

    def updated_tree_table(self, mydata):
        data = []
        for i in mydata:
            data.append((
                i['sensor'], i["range_start"], i["range_end"]
            ))
        return data

    def create_add_range_widget(self):
        if hasattr(self, "addrange_frame_created"):
            # Widget already created, destroy and recreate
            self.destroy_add_range_widget()
        self.addrange_frame_created = True
        self.sensor_label = tk.Label(
            self, text="Sensor:", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        self.sensor_label.pack()
        self.sensor_entry = tk.Entry(self)
        self.sensor_entry.pack()

        self.range_start_label = tk.Label(
            self, text="Range Start:", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        self.range_start_label.pack()
        self.range_start_entry = tk.Entry(self)
        self.range_start_entry.pack()

        self.range_end_label = tk.Label(
            self, text="Range End:", bg=Utils.BG_COLOR, fg=Utils.FONT_COLOR)
        self.range_end_label.pack()
        self.range_end_entry = tk.Entry(self)
        self.range_end_entry.pack()
        self.edit_button = tk.Button(
            self, text="Select", bg=Utils.BTN_COLOR, command=self.edit_selected_row)
        self.edit_button.pack()
        self.delete_button = tk.Button(
            self, text="Delete", bg=Utils.BTN_COLOR, command=self.delete_selected_row)
        self.delete_button.pack()
        self.tree = ttk.Treeview(self, columns=(
            "sensor", "range_start", "range_end"), show="headings")
        self.tree.column("sensor", width=100)
        self.tree.column("range_start", width=100)
        self.tree.column("range_end", width=100)
        self.tree.heading("sensor", text="Sensor")
        self.tree.heading("range_start", text="Range Start")
        self.tree.heading("range_end", text="Range End")
        self.tree.pack(fill="both", expand=True)

    # Populate the table with data from MongoDB
        self.populate_table()
        self.add_update_button = tk.Button(
            self, text="Add/Update Range", bg=Utils.BTN_COLOR, command=self.add_update_range)
        self.add_update_button.pack()
        # self.goback_button = tk.Button(self, text="Go to form", bg=Utils.BTN_COLOR,
        #                                command=lambda name="AddModbus": self.show_frame(name), justify="center")
        # self.goback_button.pack()
        self.print_button = tk.Button(
            self, text="Print Sensor List", bg=Utils.BTN_COLOR, command=self.print_sensor_list)
        self.print_button.pack()

        self.result_label = tk.Label(self, text="")
       # self.result_label.pack()

    def add_update_range(self):

        sensor = self.sensor_entry.get()
        range_start = self.range_start_entry.get()
        range_end = self.range_end_entry.get()

        print("add/update button clicked")
        if range_start and range_end:
            try:
                range_start = int(range_start)
                range_end = int(range_end)
                print("add/update button clicked2")
                selected_items = self.tree.selection()
                print(selected_items)
                if selected_items:
                    existing_sensor = selected_items[0]
                    item_values = self.tree.item(existing_sensor)
                    selected_items = item_values["values"][0]
                else:
                    existing_sensor = None
                    selected_items = "null"
                print(selected_items)
                print(sensor)
                # Check for range conflicts
                if self.check_range_conflict(range_start, range_end, sensor):
                    if selected_items != sensor:
                        print(self.sensor_list)
                        for sen in self.sensor_list:
                            print("in for")
                            if sen == sensor:
                                print("in if")
                                self.result_label.config(
                                    text="Sensor name already exist")
                                return
                        self.result_label.config(
                            text="Range conflict detected")
                        existing_sensor = None
                        return
                existing_sensor = False
                for item in self.tree.get_children():
                    item_sensor = self.tree.set(item, "sensor")
                    if item_sensor == sensor:
                        existing_sensor = item
                        break
                # for sensor in self.sensor_list:
                selected_items = self.tree.selection()
                # if selected_items:
                print(selected_items)
                print("existing_sensor:", existing_sensor)
                if selected_items:
                    print("existed data1")
                    existing_sensor = selected_items[0]
                    item_values = self.tree.item(existing_sensor)
                    sensor = item_values["values"][0]
                    range_start = item_values["values"][1]
                    range_end = item_values["values"][2]
                    print(sensor, range_start, range_end)
                    # Update an existing row
                    # item_values = self.tree.item(existing_sensor)["sensor"]
                    # item_values = self.tree.item(existing_sensor)
                    # original_sensor = item_values["values"][0]
                    # original_range_start = item_values["values"][1]
                    # original_range_end = item_values["values"][2]

                    # Update the values in the selected row of the treeview
              #  self.tree.item(existing_sensor, values=(sensor, range_start, range_end))
                    print("existed data2")
                    # index = self.tree.index(self.tree.focus())
                    # print(index)
                    if len(item_values["values"]) == 3:
                        print("exited data3")
                        # # Retrieve the original values of the selected row
                        # original_sensor = item_values[0]
                        # original_range_start = item_values[1]
                        # original_range_end = item_values[2]

                        # # Update the values in the selected row of the treeview
                        # self.tree.item(existing_sensor, values=(sensor, range_start, range_end))

                        # Perform the update operation in MongoDB
                        client = MongoClient("mongodb://localhost:27017/")
                        db = client["modbus"]
                        collection = db["slave range"]
                        # base_Rcollection = db['base_slave_range']
                        # Update the document in the collection based on the original values of the selected row
                        ##############################################################################################
                        collection.delete_one(
                            {"sensor": sensor, "range_start": range_start, "range_end": range_end})
                        self.tree.delete(selected_items)
                        # collection.update_one(
                        #     {"sensor": sensor, "range_start": int(range_start), "range_end": int(range_end)},
                        #     {"$set": {"sensor": sensor, "range_start": range_start, "range_end": range_end}}
                        # )
                        sensor = self.sensor_entry.get()
                        range_start = self.range_start_entry.get()
                        range_end = self.range_end_entry.get()
                        self.sensor_list.append(
                            (sensor, int(range_start), int(range_end)))
                        data = {
                            "sensor": sensor,
                            "range_start": int(range_start),
                            "range_end": int(range_end)
                        }

                        print(data)
                        self.Rcollection.insert_one(data)
                        self.base_Rcollection.insert_one(data)

                        # print(existing_sensor)

                        # self.delete_selected_row()

                      #  index = self.tree.index(data)
                        # Insert the updated row at the same position in the Treeview
                      #  item_id = self.tree.insert("",index, values=(sensor, int(range_start), int(range_end)))
                      #  self.tree.selection_set(item_id)
                        self.result_label.config(text="Sensor range updated")
                        # self.Rcollection.insert_one(data)
                        selected_items = None  # Reset the selected item after the update
                        existing_sensor = None
                    else:
                        print("Invalid row selection")
                else:
                    # Add a new row
                    self.sensor_list.append(
                        (sensor, int(range_start), int(range_end)))
                    data = {
                        "sensor": sensor,
                        "range_start": int(range_start),
                        "range_end": int(range_end)
                    }
                    self.Rcollection.insert_one(data)
                    self.base_Rcollection.insert_one(data)

                    self.result_label.config(text="Sensor range added")
                    existing_sensor = None
                    selected_items = None
                self.refresh_rangetable()
            except ValueError:
                self.result_label.config(text="Invalid range values")
        else:
            self.result_label.config(text="Please enter range values")

    def print_sensor_list(self):
        for sensor in self.sensor_list:
            print(
                f"Sensor: {sensor[0]}, Range Start: {sensor[1]}, Range End: {sensor[2]}")

    def check_range_conflict(self, new_start, new_end, sens):
        print("enter")
        for sensor in self.sensor_list:
            print(sensor)
            print("yo", sensor)
            start = sensor[1]
            end = sensor[2]
            if new_start <= end and new_end >= start:
                print("true")
                return True

        for sen in self.sensor_list:
            print("in for")
            if sen == sens:
                print("in if")

                return True
        return False

    def destroy_add_range_widget(self):
        # Destroy all the widgets created for the Add Range frame

        if hasattr(self, "sensor_label"):
            self.sensor_label.destroy()
        if hasattr(self, "sensor_entry"):
            self.sensor_entry.destroy()
        if hasattr(self, "range_start_label"):
            self.range_start_label.destroy()
        if hasattr(self, "range_start_entry"):
            self.range_start_entry.destroy()
        if hasattr(self, "range_end_label"):
            self.range_end_label.destroy()
        if hasattr(self, "range_end_entry"):
            self.range_end_entry.destroy()
        if hasattr(self, "edit_button"):
            self.edit_button.destroy()
        if hasattr(self, "delete_button"):
            self.delete_button.destroy()
        if hasattr(self, "tree"):
            self.tree.destroy()
        if hasattr(self, "add_update_button"):
            self.add_update_button.destroy()
        if hasattr(self, "goback_button"):
            self.goback_button.destroy()
        if hasattr(self, "print_button"):
            self.print_button.destroy()
        if hasattr(self, "result_label"):
            self.result_label.destroy()

    def populate_table(self):

        self.tree.delete(*self.tree.get_children())
        client = MongoClient("mongodb://localhost:27017/")
        db = client["modbus"]
        collection = db["slave range"]

        data = list(collection.find())

        for row in data:
            item_id = self.tree.insert("", "end", values=(
                row["sensor"], row["range_start"], row["range_end"]))

            self.tree.set(item_id, "sensor", row["sensor"])
            self.tree.set(item_id, "range_start", row["range_start"])
            self.tree.set(item_id, "range_end", row["range_end"])

    def refresh_rangetable(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.populate_table()

    def edit_selected_row(self):
        selected_item = self.tree.focus()
        if selected_item:
            print("yes1")
            item_values = self.tree.item(selected_item)["values"]
            if len(item_values) == 3:
                # Extract the values from the selected row
                sensor = item_values[0]
                range_start = item_values[1]
                range_end = item_values[2]

                # Set the entry fields with the selected row values for editing
                self.sensor_entry.delete(0, tk.END)
                self.sensor_entry.insert(tk.END, sensor)
                self.range_start_entry.delete(0, tk.END)
                self.range_start_entry.insert(tk.END, range_start)
                self.range_end_entry.delete(0, tk.END)
                self.range_end_entry.insert(tk.END, range_end)
                # Update the data in the collection
                client = MongoClient("mongodb://localhost:27017/")
                db = client["modbus"]
                collection = db["slave range"]

                new_sensor = self.sensor_entry.get()
                new_range_start = self.range_start_entry.get()
                new_range_end = self.range_end_entry.get()

                # Update the document in the collection
                #  self.refresh_rangetable()
            else:
                print("Invalid row selection")
        else:
            print("No row selected")

    def delete_selected_row(self):
        selected_items = self.tree.selection()
        print(selected_items)
        if selected_items:
            for item in selected_items:
                print(item)
                # Retrieve the values of the selected row
                item_values = self.tree.item(item)["values"]
                if len(item_values) == 3:
                    # Extract the values from the selected row
                    sensor = item_values[0]
                    range_start = item_values[1]
                    range_end = item_values[2]
                    print(sensor, range_start, range_end)
                    # Perform the deletion operation in MongoDB
                    client = MongoClient("mongodb://localhost:27017/")
                    db = client["modbus"]
                    collection = db["slave range"]

                    # Delete the document from the collection based on the selected row values
                    collection.delete_one(
                        {"sensor": str(sensor), "range_start": range_start, "range_end": range_end})
                    print(type(range_start))
                    # Delete the row from the tree
                    self.tree.delete(item)
                    print('Item Deleted')
                else:
                    print("Invalid row selection")
        else:
            print("No row selected")

    def show_add_range_widget(self):
        self.pack(fill="y")
        self.create_add_range_widget()
