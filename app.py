import streamlit as st
import pandas as pd

# Sample vessel schedule data
data = [
    {"Vessel": "LIBERTY PEACE", "Voyage": "75", "Port": "Shuaiba, Kuwait", "Terminal": None, "Date of Arrival": "14:00 07/19/25", "Date of Departure": "18:00 07/20/25", "Status": "Pending Port Call", "Notes": "possible delays for cargo documentation"},
    {"Vessel": "LIBERTY PEACE", "Voyage": "75", "Port": "Hamad, Qatar", "Terminal": None, "Date of Arrival": "19:13 07/21/25", "Date of Departure": "19:13 07/22/25", "Status": "Completed OPS", "Notes": None},
    {"Vessel": "LIBERTY PEACE", "Voyage": "76", "Port": "Charleston - T.C Dock, SC", "Terminal": None, "Date of Arrival": "2025-10-10 08:19", "Date of Departure": "2025-11-10 01:25", "Status": "Pending Port Call", "Notes": None},
    {"Vessel": "LIBERTY POWER", "Voyage": "24", "Port": "Charleston, SC", "Terminal": "Columbus Street Terminal", "Date of Arrival": "2025-12-07 01:30", "Date of Departure": "2025-12-07 06:30", "Status": "Pending Port Call", "Notes": "BUNKERS ONLY"},
    {"Vessel": "LIBERTY POWER", "Voyage": "25", "Port": "Duqm, Oman", "Terminal": None, "Date of Arrival": "2025-07-09 19:12", "Date of Departure": "2025-12-09 04:46", "Status": "Pending Port Call", "Notes": "Cargo availability 9/8."}
]

df = pd.DataFrame(data)

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

# Stage: Vessel selection
if st.session_state.stage == "vessel":
    prompt = "Hi! 👋 Welcome to LGLDubaiBot. Please enter a vessel name:"
    st.chat_message("assistant").markdown(prompt)
    vessel_input = st.chat_input("Type a vessel name...")
    if vessel_input:
        st.session_state.messages.append({"role": "user", "content": vessel_input})
        vessels = df["Vessel"].unique()
        matches = [v for v in vessels if vessel_input.strip().lower() in v.lower()]
        if matches:
            st.session_state.messages.append({"role": "assistant", "content": f"Found these vessels matching **{vessel_input}**. Please select one:"})
            for match in matches:
                if st.button(match):
                    st.session_state.vessel = match
                    st.session_state.stage = "voyage"
                    st.session_state.messages.append({"role": "assistant", "content": f"Great! You selected **{match}**. Please select a voyage:"})
                    st.rerun()
        else:
            st.session_state.messages.append({"role": "assistant", "content": "Sorry, I couldn't find that vessel. Please try again."})

# Stage: Voyage selection
elif st.session_state.stage == "voyage":
    voyages = df[df["Vessel"] == st.session_state.vessel]["Voyage"].unique()
    for v in voyages:
        if st.button(f"Voyage {v}"):
            st.session_state.voyage = v
            st.session_state.stage = "port"
            st.session_state.messages.append({"role": "assistant", "content": f"You selected **Voyage {v}**. Now choose a port:"})
            st.rerun()

# Stage: Port selection
elif st.session_state.stage == "port":
    ports = df[(df["Vessel"] == st.session_state.vessel) & (df["Voyage"] == st.session_state.voyage)]["Port"].unique()
    for p in ports:
        if st.button(p):
            st.session_state.port = p
            st.session_state.stage = "details"
            st.session_state.messages.append({"role": "assistant", "content": f"You selected **{p}**. Here are the port call details:"})
            st.rerun()

# Stage: Show details
elif st.session_state.stage == "details":
    row = df[(df["Vessel"] == st.session_state.vessel) &
             (df["Voyage"] == st.session_state.voyage) &
             (df["Port"] == st.session_state.port)].iloc[0]
    details = f"""
- **Vessel**: {row['Vessel']}
- **Voyage**: {row['Voyage']}
- **Port**: {row['Port']}
- **Terminal**: {row['Terminal'] or 'N/A'}
- **Arrival**: {row['Date of Arrival']}
- **Departure**: {row['Date of Departure']}
- **Status**: {row['Status']}
- **Notes**: {row['Notes'] or 'None'}
"""
    st.chat_message("assistant").markdown(details)
    if st.button("🔁 Ask another question"):
        reset_bot()
        st.rerun()
