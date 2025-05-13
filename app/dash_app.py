import os
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from flask import session
import dash
from dash import dcc, html
from dash.dependencies import Input, Output


def create_dash_app(flask_app):
    dash_app = dash.Dash(
        __name__,
        server=flask_app,
        url_base_pathname="/dash/",
        suppress_callback_exceptions=True,
    )

    dash_app.layout = html.Div(
        [
            html.H2("📊 Hourly Staffing vs Demand"),
            html.Label("Units produced per person per hour:"),
            dcc.Slider(
                id="rate-slider",
                min=1,
                max=10,
                step=1,
                value=5,
                marks={i: str(i) for i in range(1, 11)},
            ),
            dcc.Graph(id="line-chart"),
            html.Div(id="summary", style={"fontSize": "18px", "marginTop": "10px"}),
        ]
    )

    @dash_app.callback(
        [Output("line-chart", "figure"), Output("summary", "children")],
        [Input("rate-slider", "value")],
    )
    def update_chart(rate):
        file_path = session.get("uploaded_file")

        # ✅ Dev fallback
        if not file_path:
            file_path = "uploads/Demand.xlsx"

        if not os.path.exists(file_path):
            return {}, html.Div("⚠️ No uploaded Excel file found.")

        df = pd.read_excel(file_path, sheet_name="Staffing Plan")
        df["Hour"] = df["Hour"].astype(int)

        # Calculate staffing logic
        df["Recommended"] = np.ceil(df["Demand"] / rate)
        df["Actual"] = df["Recommended"]  # Placeholder — replace later
        df["Delta"] = df["Actual"] - df["Recommended"]
        df["Color"] = df["Delta"].apply(lambda x: "red" if x < 0 else "green")

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=df["Hour"], y=df["Actual"], mode="lines+markers", name="Actual"
            )
        )
        fig.add_trace(
            go.Scatter(
                x=df["Hour"],
                y=df["Recommended"],
                mode="lines+markers",
                name="Recommended",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=df["Hour"],
                y=df["Delta"],
                mode="markers",
                name="Delta (Actual - Recommended)",
                marker=dict(color=df["Color"], size=10, symbol="x"),
            )
        )

        fig.update_layout(
            title=f"Hourly Staffing vs Demand (Rate: {rate} units/hr/person)",
            xaxis_title="Hour",
            yaxis_title="Staff Count",
            hovermode="x unified",
        )

        overstaff = (df["Delta"] > 0).sum()
        understaff = df["Delta"].apply(lambda x: max(0, -x)).sum()

        summary = [
            f"🧮 Currently understaffed by {understaff:.0f} people total.",
            f"✅ Overstaffed for {overstaff} hour(s).",
        ]
        if overstaff >= 3:
            summary.append("⚠️ Consider shift adjustments to avoid slowdown.")

        return fig, html.Div([html.P(s) for s in summary])

    return dash_app
