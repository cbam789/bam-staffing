import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import math
import os


def process_staffing_data(demand_path, expected_productivity):
    # Load demand data
    df = pd.read_excel(demand_path)

    if "Hour" not in df.columns or "Demand" not in df.columns:
        print("Error: Excel file must contain 'Hour' and 'Demand' columns.")
        return

    # Group demand by hour
    hourly_demand = df.groupby("Hour")["Demand"].sum().reindex(range(24), fill_value=0)

    # Calculate recommended staff and coverage
    recommended_staff = hourly_demand.apply(
        lambda x: math.ceil(x / expected_productivity)
    )
    coverage = recommended_staff * expected_productivity

    # Save to Excel
    output_df = pd.DataFrame(
        {
            "Hour": hourly_demand.index,
            "Total_Demand": hourly_demand.values,
            "Recommended_Staff": recommended_staff.values,
            f"Estimated_Coverage (x{expected_productivity})": coverage.values,
        }
    )

    output_path = "staffing_output.xlsx"
    with pd.ExcelWriter(output_path) as writer:
        output_df.to_excel(writer, index=False, sheet_name="Staffing Plan")

    print(f"Output saved to {output_path}")

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.plot(
        hourly_demand.index,
        hourly_demand.values,
        label="Actual Demand",
        color="skyblue",
        marker="o",
    )
    plt.plot(
        coverage.index,
        coverage.values,
        label=f"Coverage (x{expected_productivity})",
        color="orange",
        marker="s",
    )

    # ✅ Insert the logo image on the chart here
    try:
        logo_img = mpimg.imread("assets/bamsta_logo.png")  # adjust path if needed
        plt.figimage(logo_img, xo=50, yo=50, alpha=0.15, zorder=1)
    except Exception as e:
        print(f"Could not load logo: {e}")

    plt.xlabel("Hour of Day")
    plt.ylabel("Demand Units per Hour")
    plt.title("Demand vs Coverage by Recommended Staff")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    chart_path = "supply_vs_demand_chart.png"
    plt.savefig(chart_path)
    plt.show()

    print(f"Chart saved to {chart_path}")
