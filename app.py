Python 3.12.6 (tags/v3.12.6:a4a2d2b, Sep  6 2024, 20:11:23) [MSC v.1940 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import streamlit as st
import pandas as pd

# Title and greeting
st.title("🛳️ LGLDubaiBot")
st.markdown("Welcome! Kindly query about the vessel.")

# Load the vessel schedule data
data = [
    ["LIBERTY PEACE", 75, "Shuaiba, Kuwait", None, "14:00 07/19/25", "18:00 07/20/25", "Pending Port Call", "possible delays for cargo documentation"],
    ["LIBERTY PEACE", 75, "Hamad, Qatar", None, "19:13 07/21/25", "19:13 07/22/25", "Completed OPS", None],
    ["LIBERTY PEACE", 75, "Apra Harbor", None, "2025-07-08 11:10", "2025-09-08 04:44", "Pending Port Call", None],
    ["LIBERTY PEACE", 75, "Shuaiba, Kuwait", None, "08:48 08/25/25", "22:00 08/31/25", "Pending Port Call", None],
    ["LIBERTY PEACE", 75, "Beaumont, TX", None, "2025-02-10 04:19", "2025-05-10 17:01", "In Operation", None],
    ["LIBERTY PEACE", 75, "Jacksonville, FL", None, "2025-08-10 20:47", "2025-09-10 20:47", "Pending Port Call", None],
    ["LIBERTY PEACE", 76, "Charleston - T.C Dock, SC", None, "2025-10-10 08:19", "2025-11-10 01:25", "Pending Port Call", None],
    ["LIBERTY POWER", 24, "Charleston - T.C Dock, SC", None, "2025-11-07 06:00", "2025-11-07 23:00", "Pending Port Call", None],
    ["LIBERTY POWER", 24, "Charleston, SC", "Columbus Street Terminal", "2025-12-07 01:30", "2025-12-07 06:30", "Pending Port Call", "BUNKERS ONLY"],
    ["LIBERTY POWER", 24, "Jacksonville, FL", None, "2025-12-07 19:02", "14:00 07/14/25", "Pending Port Call", None],
    ["LIBERTY POWER", 24, "Beaumont, TX", None, "12:00 07/18/25", "15:30 07/29/25", "Pending Port Call", "Aviation cargo ALD July 25"],
    ["LIBERTY POWER", 25, "Shuaiba, Kuwait", None, "20:14 08/30/25", "2025-05-09 04:46", "Pending Port Call", "Cargo availability 9/1"],
    ["LIBERTY POWER", 25, "Duqm, Oman", None, "2025-07-09 19:12", "2025-12-09 04:46", "Pending Port Call", "Cargo availability 9/8."],
    ["LIBERTY POWER", 25, "Charleston - T.C Dock, SC", None, "2025-12-10 18:06", "18:06 10/13/25", "Pending Port Call", None],
    ["LIBERTY POWER", 25, "Jacksonville, FL", None, "06:14 10/14/25", "06:14 10/15/25", "Pending Port Call", None],
    ["LIBERTY POWER", 25, "Beaumont, TX", None, "08:14 10/18/25", "08:14 10/19/25", "Pending Port Call", None]
]

columns = ["Vessel", "Voyage", "Port", "Terminal", "Date of Arrival", "Date of Departure", "Status", "Notes"]
df = pd.DataFrame(data, columns=columns)

... # Step 1: Select Vessel
... vessels = sorted(df["Vessel"].unique())
... selected_vessel = st.selectbox("Select a vessel:", vessels)
... 
... if selected_vessel:
...     # Step 2: Select Voyage
...     voyages = sorted(df[df["Vessel"] == selected_vessel]["Voyage"].unique())
...     selected_voyage = st.selectbox("Select a voyage:", voyages)
... 
...     if selected_voyage:
...         # Step 3: Select Port
...         ports = df[(df["Vessel"] == selected_vessel) & (df["Voyage"] == selected_voyage)]["Port"].unique()
...         selected_port = st.selectbox("Select a port:", ports)
... 
...         if selected_port:
...             # Display port call details
...             result = df[(df["Vessel"] == selected_vessel) &
...                         (df["Voyage"] == selected_voyage) &
...                         (df["Port"] == selected_port)]
... 
...             if not result.empty:
...                 st.subheader("📋 Port Call Details")
...                 for _, row in result.iterrows():
...                     st.markdown(f"""
...                     - **Vessel**: {row['Vessel']}
...                     - **Voyage**: {row['Voyage']}
...                     - **Port**: {row['Port']}
...                     - **Terminal**: {row['Terminal'] if pd.notna(row['Terminal']) else 'N/A'}
...                     - **Arrival**: {row['Date of Arrival']}
...                     - **Departure**: {row['Date of Departure']}
...                     - **Status**: {row['Status']}
...                     - **Notes**: {row['Notes'] if pd.notna(row['Notes']) else 'N/A'}
...                     """)
...             else:
...                 st.warning("No matching port call details found.")
... 
