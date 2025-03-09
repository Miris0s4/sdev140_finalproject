import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk

class GroceryStoreApp(tk.Tk):
    def __init__(self):                                   
        super().__init__()

        self.title("Sosa's Market")
        self.geometry("500x500")

# Creating the background image
        self.canvas = tk.Canvas(self, width=500, height=500)
        self.canvas.pack(fill="both", expand=True)

        try:
# Using Pillow for resizing
            self.background_image = Image.open("homedesign.png")
            self.background_image = self.background_image.resize((500, 500))
            self.background_image_tk = ImageTk.PhotoImage(self.background_image)
            
            self.canvas.create_image(0, 0, anchor="nw", image=self.background_image_tk)
        except Exception as e:
            print(f"Error loading background image: {e}")

# The grocery items and their prices
        self.all_items = [("Oranges", 2.50), ("Bread", 1.99), ("Eggs", 3.00),
                          ("Apples", 1.50), ("Carrots", 1.20), ("Peaches", 2.75)]

# Items to be displayed in the listbox. This will change when items are removed or added
        self.items = []

# The listbox starts empty to display items and prices
        self.item_listbox = tk.Listbox(self, width=40, height=10, bg="#fcffa6", fg="#000000", font=("Arial", 12), bd=2, relief="solid")
        self.item_listbox.place(relx=0.5, rely=0.4, anchor="center")

# Frame for buttons at the bottom
        button_frame = tk.Frame(self, bg="#98cd9a")
        button_frame.place(relx=0.5, rely=0.72, anchor="center")

# Add Item Button
        self.add_button = tk.Button(button_frame, text="Add Item", command=self.add_item, bg="#4CAF50", fg="white", font=("Arial", 12))
        self.add_button.pack(side=tk.LEFT, padx=10)

# Remove Item Button
        self.remove_button = tk.Button(button_frame, text="Remove Item", command=self.remove_item, bg="#f44336", fg="white", font=("Arial", 12))
        self.remove_button.pack(side=tk.LEFT, padx=10)

# Help Button
        self.help_button = tk.Button(button_frame, text="Help", command=self.show_user_manual, bg="#2196F3", fg="white", font=("Arial", 12))
        self.help_button.pack(side=tk.LEFT, padx=10)

# Initial setup label for total price
        self.total_label = tk.Label(self, text="Total Price: $0.00", bg="#98cd9a", fg="#000000", font=("Arial", 12))
        self.total_label.place(relx=0.5, rely=0.65, anchor="center")

    def update_item_listbox(self):
        """Updates the listbox with the current items and prices"""
        self.item_listbox.delete(0, tk.END)
        for item, price in self.items:
            self.item_listbox.insert(tk.END, f"{item}: ${price:.2f}")
        self.update_total_price()

    def update_total_price(self):
        """Calculate the total price of all items."""
        total = sum(price for _, price in self.items)
        self.total_label.config(text=f"Total Price: ${total:.2f}")

    def add_item(self):
        """Add a new item to the list"""
        new_item = self.simple_input_dialog("Select Item", "Select the name of the item:")
        if not new_item:
            return

        selected_price = dict(self.all_items).get(new_item)

# Prompt for the price of the selected item
        price = self.simple_price_input_dialog("Enter Price", f"Enter the price for {new_item}:", selected_price)

        if price is None:
            return

# Add the selected item and price to the list
        self.items.append((new_item, price))
        self.update_item_listbox()

    def remove_item(self):
        """Remove the selected item from the list"""
        try:
            selected_item_index = self.item_listbox.curselection()[0]
            item_to_remove = self.item_listbox.get(selected_item_index).split(":")[0]
# Remove the item from the list based on its name
            self.items = [item for item in self.items if item[0] != item_to_remove]
            self.update_item_listbox()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select an item to remove.")

    def simple_input_dialog(self, title, prompt):
        """Displays a simple input dialog to get user input for item selection"""
        input_dialog = tk.Toplevel(self)
        input_dialog.title(title)

        label = tk.Label(input_dialog, text=prompt)
        label.pack(pady=10)

# Dropdown list (Combobox) for selecting items
        combobox = ttk.Combobox(input_dialog, values=[item[0] for item in self.all_items])
        combobox.pack(pady=10)
        combobox.set("Select an item")

        def on_ok():
            input_dialog.result = combobox.get()
            input_dialog.destroy()

        ok_button = tk.Button(input_dialog, text="OK", command=on_ok)
        ok_button.pack(pady=10)

        input_dialog.result = None
        input_dialog.wait_window(input_dialog)
        return input_dialog.result

    def simple_price_input_dialog(self, title, prompt, suggested_price):
        """Displays a simple input dialog to get user input for the price"""
        input_dialog = tk.Toplevel(self)
        input_dialog.title(title)

        label = tk.Label(input_dialog, text=prompt)
        label.pack(pady=10)

# Display the suggested price for the selected item
        price_label = tk.Label(input_dialog, text=f"Suggested Price: ${suggested_price:.2f}")
        price_label.pack(pady=10)

        entry = tk.Entry(input_dialog)
        entry.pack(pady=10)

        def on_ok():
            try:
                entered_price = float(entry.get())
# Allow a small tolerance of $0.01 so user can insert the correct price
                if abs(entered_price - suggested_price) < 0.01:
                    input_dialog.result = entered_price
                    input_dialog.destroy()
                else:
                    messagebox.showerror("Invalid Price", f"Please enter the suggested price of ${suggested_price:.2f}.")
    
            except ValueError:
                messagebox.showerror("Invalid Price", "Please enter a valid price.")

        ok_button = tk.Button(input_dialog, text="OK", command=on_ok)
        ok_button.pack(pady=10)

        input_dialog.result = None
        input_dialog.wait_window(input_dialog)
        return input_dialog.result

    def show_user_manual(self):
        """Show the user manual in a new window"""
        manual_window = tk.Toplevel(self)
        manual_window.title("User Manual")
        manual_window.geometry("600x400")

# Add instructions or user guide
        manual_text = """
        Welcome to Sosa's Market!

        Here’s how to use the app:

        1. Add an Item: Click the 'Add Item' button to add an item to the shopping list.
           You can choose from a predefined list of items and their prices.

        2. Remove an Item: Click the 'Remove Item' button to remove the selected item 
           from the shopping list.

        3. Total Price: The total price of the items in your shopping list will be shown 
           at the bottom.

        4. Help: Click the 'Help' button to view this manual.
        """
        manual_label = tk.Label(manual_window, text=manual_text, justify="left", font=("Arial", 12), padx=10, pady=10)
        manual_label.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    app = GroceryStoreApp()
    app.mainloop()
