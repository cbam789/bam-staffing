import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os

from app.processor import (
    process_staffing_data,
    plot_supply_demand,
)  # Make sure plot_supply_demand is in processor.py


def get_expected_productivity():
    root = tk.Tk()
    root.withdraw()
    answer = simpledialog.askfloat(
        "Expected Productivity", "How many demand units can 1 staff handle?"
    )
    root.destroy()
    return answer or 10  # Default fallback


class BamStaffingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bam Staffing - Gap Visualizer")

        self.supply_path = tk.StringVar()
        self.demand_path = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Supply File:").grid(row=0, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.supply_path, width=40).grid(
            row=0, column=1
        )
        tk.Button(self.root, text="Browse", command=self.browse_supply).grid(
            row=0, column=2
        )

        tk.Label(self.root, text="Demand File:").grid(row=1, column=0, sticky="e")
        tk.Entry(self.root, textvariable=self.demand_path, width=40).grid(
            row=1, column=1
        )
        tk.Button(self.root, text="Browse", command=self.browse_demand).grid(
            row=1, column=2
        )

        tk.Button(
            self.root,
            text="Generate Chart",
            command=self.generate_chart,
            bg="green",
            fg="white",
        ).grid(row=2, column=1, pady=10)

    def browse_supply(self):
        file = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if file:
            self.supply_path.set(file)

    def browse_demand(self):
        file = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if file:
            self.demand_path.set(file)

    def generate_chart(self):
        if not self.supply_path.get() or not self.demand_path.get():
            messagebox.showerror(
                "Missing Files", "Please select both supply and demand files."
            )
            return

        try:
            productivity = get_expected_productivity()
            supply, demand = process_staffing_data(
                self.supply_path.get(), self.demand_path.get(), productivity
            )

            chart_path = os.path.join(os.getcwd(), "staffing_gap_chart.png")
            plot_supply_demand(supply, demand, chart_path)

            messagebox.showinfo(
                "Success", f"Chart generated and saved to:\n{chart_path}"
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))
