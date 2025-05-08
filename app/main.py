import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import math
import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image, ImageTk


# === Your main application window ===
def bam_staffing_app():
    root = tk.Tk()
    root.title("BamSta - Smart Staffing")
    root.geometry("800x600")
    root.configure(bg="white")

    def browse_file():
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            entry_file.delete(0, tk.END)
            entry_file.insert(0, file_path)

    def run_analysis():
        file_path = entry_file.get()
        try:
            expected_productivity = int(entry_productivity.get())
        except ValueError:
            messagebox.showerror("Error", "Productivity must be an integer.")
            return

        if not file_path or not os.path.exists(file_path):
            messagebox.showerror("Error", "Invalid file path.")
            return

        # Process data
        df = pd.read_excel(file_path)
        if "Hour" not in df.columns or "Demand" not in df.columns:
            messagebox.showerror(
                "Error", "Excel must have 'Hour' and 'Demand' columns."
            )
            return

        hourly_demand = (
            df.groupby("Hour")["Demand"].sum().reindex(range(24), fill_value=0)
        )
        recommended_staff = hourly_demand.apply(
            lambda x: math.ceil(x / expected_productivity)
        )
        coverage = recommended_staff * expected_productivity

        # Save Excel
        output_df = pd.DataFrame(
            {
                "Hour": hourly_demand.index,
                "Total_Demand": hourly_demand.values,
                "Recommended_Staff": recommended_staff.values,
                f"Estimated_Coverage (x{expected_productivity})": coverage.values,
            }
        )
        output_df.to_excel("staffing_output.xlsx", index=False)

        # Plot
        plt.figure(figsize=(12, 6))
        plt.plot(
            hourly_demand.index,
            hourly_demand.values,
            label="Actual Demand",
            marker="o",
            color="skyblue",
        )
        plt.plot(
            coverage.index,
            coverage.values,
            label="Estimated Coverage",
            marker="s",
            color="orange",
        )
        plt.title("Demand vs Coverage by Recommended Staff")
        plt.xlabel("Hour of Day")
        plt.ylabel("Units")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        # Add logo to chart
        logo_path = "assets/bamsta_logo.png"
        if os.path.exists(logo_path):
            logo_img = mpimg.imread(logo_path)
            plt.figimage(logo_img, xo=50, yo=50, alpha=0.15, zorder=1)

        chart_path = "supply_vs_demand_chart.png"
        plt.savefig(chart_path)
        plt.show()

        messagebox.showinfo(
            "Success",
            f"Output saved to 'staffing_output.xlsx'\nChart saved to '{chart_path}'",
        )

    # === UI Layout ===
    ttk.Label(root, text="Demand File:", background="white").pack(pady=(30, 5))
    entry_file = ttk.Entry(root, width=50)
    entry_file.pack()
    ttk.Button(root, text="Browse", command=browse_file).pack(pady=5)

    ttk.Label(
        root, text="Expected Productivity (Units per Staff):", background="white"
    ).pack(pady=5)
    entry_productivity = ttk.Entry(root, width=10)
    entry_productivity.insert(0, "10")
    entry_productivity.pack()

    ttk.Button(root, text="Run Staffing Analysis", command=run_analysis).pack(pady=20)

    root.mainloop()


# === Splash screen ===
def show_splash():
    splash = tk.Tk()
    splash.overrideredirect(True)
    splash.geometry("500x300+500+300")

    img_path = "assets/bamstasplash.png"
    if os.path.exists(img_path):
        img = Image.open(img_path)
        splash_img = ImageTk.PhotoImage(img)
        splash_label = tk.Label(splash, image=splash_img)
        splash_label.image = splash_img  # prevent garbage collection
        splash_label.pack()
    else:
        splash_label = tk.Label(splash, text="Loading BamSta...", font=("Arial", 24))
        splash_label.pack(pady=100)

    # After delay, show main app
    def start_main():
        splash.destroy()
        bam_staffing_app()

    splash.after(3000, start_main)
    splash.mainloop()


# === Start here ===
if __name__ == "__main__":
    show_splash()
