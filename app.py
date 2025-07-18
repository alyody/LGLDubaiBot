import streamlit as st
import pandas as pd

# Load Excel file from GitHub
df = pd.read_excel(
    "https://raw.githubusercontent.com/alyody/LGLDubaiBot/main/LGL%20Vessel%20Schedule.xlsx",
    engine="openpyxl"
)

# Standardize date formats
df["Date of Arrival"] = pd.to_datetime(df["Date of Arrival"], errors='coerce')
df["Date of Departure"] = pd.to_datetime(df["Date of Departure"], errors='coerce')

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.stage = "vessel"
    st.session_state.vessel = None
    st.session_state.voyage = None
    st.session_state.port = None

st.title("🛳️ LGLDubaiBot")

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

# Reset function
def reset_bot():
    st.session_state.stage = "vessel"
    st.session_state.vessel = None
    st.session_state.voyage = None
    st.session_state.port = None
    st.session_state.messages = []

# Stage 1: Vessel selection
if st.session_state.stage == "vessel":
    vessel_input = st.chat_input("Hi! 👋 Welcome to LGLDubaiBot. Please enter a vessel name:")
    if vessel_input:
        st.session_state.messages.append({"role": "user", "content": vessel_input})
        vessel_input_clean = vessel_input.strip().lower()
        vessels = df["Vessel"].dropna().unique()
        matches = [v for v in vessels if vessel_input_clean in v.lower()]
        if matches:
            selected_vessel = matches[0]
            st.session_state.vessel = selected_vessel
            st.session_state.stage = "voyage"
            st.session_state.messages.append({"role": "assistant", "content": f"Great! I found **{selected_vessel}**. Please select a voyage:"})
            st.rerun()
        else:
            st.session_state.messages.append({"role": "assistant", "content": "❌ Sorry, I couldn't find that vessel. Please try again."})
            st.rerun()

# Stage 2: Voyage selection
elif st.session_state.stage == "voyage":
    voyages = df[df["Vessel"].str.lower() == st.session_state.vessel.lower()]["Voyage"].dropna().unique()
    st.chat_message("assistant").markdown("Please select a voyage:")
    for v in voyages:
        if st.button(f"Voyage {v}"):
            st.session_state.voyage = v
            st.session_state.stage = "port"
            st.session_state.messages.append({"role": "assistant", "content": f"You selected **Voyage {v}**. Now choose a port:"})
            st.rerun()

# Stage 3: Port selection
elif st.session_state.stage == "port":
    ports = df[
        (df["Vessel"].str.lower() == st.session_state.vessel.lower()) &
        (df["Voyage"] == st.session_state.voyage)
    ]["Port"].dropna().unique()
    st.chat_message("assistant").markdown("Please select a port:")
    for p in ports:
        if st.button(f"{p}"):
            st.session_state.port = p
            st.session_state.stage = "details"
            st.session_state.messages.append({"role": "assistant", "content": f"You selected **{p}**. Here are the port call details:"})
            st.rerun()

# Stage 4: Show details
elif st.session_state.stage == "details":
    filtered = df[
        (df["Vessel"].str.lower() == st.session_state.vessel.lower()) &
        (df["Voyage"] == st.session_state.voyage) &
        (df["Port"] == st.session_state.port)
    ]
    if not filtered.empty:
        row = filtered.iloc[0]
        arrival = row['Date of Arrival'].strftime("%Y-%m-%d %H:%M") if pd.notnull(row['Date of Arrival']) else "N/A"
        departure = row['Date of Departure'].strftime("%Y-%m-%d %H:%M") if pd.notnull(row['Date of Departure']) else "N/A"
        details = f"""
- **Vessel**: {row['Vessel']}
- **Voyage**: {row['Voyage']}
- **Port**: {row['Port']}
- **Terminal**: {row['Terminal'] or 'N/A'}
- **Arrival**: {arrival}
- **Departure**: {departure}
- **Status**: {row['Status']}
- **Notes**: {row['Notes'] or 'None'}
"""
        st.chat_message("assistant").markdown(details)
    else:
        st.chat_message("assistant").markdown("❌ Sorry, I couldn't find the port call details.")

    if st.button("🔁 Ask another question"):
        reset_bot()
        st.rerun()
