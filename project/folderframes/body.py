
import tkinter as tk

from pymongo import MongoClient

from .utils import Utils


class Body(tk.Frame,Utils):
    def __init__(self, parent):
        super().__init__(parent)
        print('Body')

    def refresh_table(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.create_body_table_widget()
    def create_body_table_widget(self):

        table_frame = tk.Frame(self)
        canvas = tk.Canvas(table_frame)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = tk.Scrollbar(
            table_frame, orient=tk.VERTICAL, command=canvas.yview)
        xscrollbar = tk.Scrollbar(
            table_frame, orient=tk.HORIZONTAL, command=canvas.xview)

        xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(width=860, height=330)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.configure(xscrollcommand=xscrollbar.set)
        body_frame = tk.Frame(canvas)
        canvas.bind("<Configure>", lambda event: canvas.configure(
            scrollregion=canvas.bbox("all")))

        # body_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=body_frame, anchor="nw")

        self.search_entry = tk.Entry(body_frame, width=30)

        client = MongoClient("mongodb://localhost:27017/")
        db = client["modbus"]
        collection = db["configurations"]

        data = list(collection.find())
        d = (collection.find_one({"slave_id": self.search_entry.get()}))
        idx = 1
        self.search_label = tk.Button(body_frame, text="Search", padx=5, pady=5,
                                      bg=self.BTN_COLOR, command=lambda: self.open_edit_form(self.search_entry.get()))


        self.search_label.grid(row=0, column=1, pady=5)
        self.search_entry.grid(row=0, column=0, pady=5, padx=15)

        def filter_data(search_query):
            print((search_query))

        def refresh_table():
            search_query = self.search_entry.get()
            filtered_data = filter_data(search_query)


        headers = ['sr no', 'slave_type', 'modbus_id',
                   'description', 'slave_id', 'Edit', 'Delete']

        for col, header in enumerate(headers):
            label = tk.Label(body_frame, text=header, relief="solid",
                             width=12, padx=5, pady=5, bg="#FFFFFF", fg="#000000")
            label.grid(row=1, column=col, sticky="nsew")

            idx = 1
            for row, document in enumerate(data, start=3):
                for col, header in enumerate(headers):
                    if col == 0:
                        cell_value = idx
                        label = tk.Label(
                            body_frame, text=cell_value, relief="solid", width=15, padx=5, pady=5)
                        label.grid(row=row, column=col, sticky="nsew")
                    elif col == 5:
                        edit_button = tk.Button(
                            body_frame, text="Edit", bg="green", relief="solid", borderwidth=1)
                        edit_button.grid(row=row, column=col,
                                         padx=3, pady=3, sticky="nsew")
                        edit_button.bind(
                            "<Button-1>", lambda event, doc=document: self.open_edit_form(doc))

                    elif col == 6:
                        delete_button = tk.Button(
                            body_frame, text="Delete", bg="red", relief="solid", borderwidth=1)
                        delete_button.grid(
                            row=row, column=col, padx=3, pady=3, sticky="nsew")
                        delete_button.bind(
                            "<Button-1>", lambda event, doc=document: self.delete_document(doc))
                    else:
                        cell_value = document.get(header.lower(), "")

                        label = tk.Label(
                            body_frame, text=cell_value, relief="solid", width=15, padx=5, pady=5)
                        label.grid(row=row, column=col, sticky="nsew")

                idx += 1
                body_frame.rowconfigure(row, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        # Bind the Enter key to refresh the table
        self.search_entry.bind("<Return>", lambda event: refresh_table())
        canvas.configure(scrollregion=canvas.bbox("all"))

        table_frame.grid(row=1, column=1, padx=200, pady=100, sticky="nsew")
        table_frame.config(width=1000, height=600)
        
    def show_body_table_widget(self):
        print("widget created")
        self.pack(fill="both", pady=30)
        self.create_body_table_widget()
