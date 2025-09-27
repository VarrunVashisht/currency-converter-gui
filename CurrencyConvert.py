import tkinter as tk
from tkinter import ttk, messagebox
from currency_converter import CurrencyConverter, RateNotFoundError

# ----- Model -----
c = CurrencyConverter()  # uses ECB rates bundled with the package
CURRENCIES = sorted(c.currencies)

# ----- Controller -----
def button_clicked():
    try:
        amount = float(entry_amount.get())
        cur_from = combo_from.get().strip().upper()
        cur_to = combo_to.get().strip().upper()

        if cur_from not in CURRENCIES or cur_to not in CURRENCIES:
            messagebox.showerror("Invalid currency", "Please choose valid currencies from the lists.")
            return

        result = c.convert(amount, cur_from, cur_to)
        result_label.config(
            text=f"{amount:.2f} {cur_from} = {result:.2f} {cur_to}"
        )
        status_var.set("Converted successfully.")
    except ValueError:
        messagebox.showerror("Invalid amount", "Please enter a valid number for the amount.")
    except RateNotFoundError:
        messagebox.showerror(
            "Rate not found",
            "Conversion rate unavailable for the selected currencies/date."
        )
    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong:\n{e}")

# ----- View -----
window = tk.Tk()
window.title("Currency Converter")
window.minsize(380, 240)

# Title
title = tk.Label(window, text="Currency Converter", font=("Arial", 18))
title.grid(row=0, column=0, columnspan=2, pady=(12, 6))

# Amount
tk.Label(window, text="Amount:", font=("Arial", 10)).grid(row=1, column=0, padx=12, pady=8, sticky="e")
entry_amount = tk.Entry(window, font=("Arial", 10))
entry_amount.grid(row=1, column=1, padx=12, pady=8, sticky="we")

# From currency
tk.Label(window, text="From:", font=("Arial", 10)).grid(row=2, column=0, padx=12, pady=8, sticky="e")
combo_from = ttk.Combobox(window, values=CURRENCIES, state="readonly")
combo_from.grid(row=2, column=1, padx=12, pady=8, sticky="we")

# To currency
tk.Label(window, text="To:", font=("Arial", 10)).grid(row=3, column=0, padx=12, pady=8, sticky="e")
combo_to = ttk.Combobox(window, values=CURRENCIES, state="readonly")
combo_to.grid(row=3, column=1, padx=12, pady=8, sticky="we")

# Defaults
if "USD" in CURRENCIES: combo_from.set("USD")
if "EUR" in CURRENCIES: combo_to.set("EUR")

# Convert button
convert_btn = tk.Button(window, text="Convert", command=button_clicked)
convert_btn.grid(row=4, column=0, columnspan=2, pady=10)

# Result
result_label = tk.Label(window, text="", font=("Arial", 12, "bold"))
result_label.grid(row=5, column=0, columnspan=2, pady=(4, 10))

# Status bar
status_var = tk.StringVar(value="Ready.")
status = tk.Label(window, textvariable=status_var, anchor="w", relief="sunken")
status.grid(row=6, column=0, columnspan=2, sticky="we")

# Make column 1 stretch
window.grid_columnconfigure(1, weight=1)

# Enter key triggers convert
window.bind("<Return>", lambda e: button_clicked())

window.mainloop()
