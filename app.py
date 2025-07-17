import streamlit as st
import pandas as pd

# Load the vessel schedule data from a structured dictionary
data = [
    {"Vessel": "LIBERTY PEACE", "Voyage": "75", "Port": "Shuaiba, Kuwait", "Terminal": None, "Date of Arrival": "14:00 07/19/25", "Date of Departure": "18:00 07/20/25", "Status": "Pending Port Call", "Notes": "possible delays for cargo documentation"},
    {"Vessel": "LIBERTY PEACE", "Voyage": "75", "Port": "Hamad, Qatar", "Terminal": None, "Date of Arrival": "19:13 07/21/25", "Date of Departure": "19:13 07/22/25", "Status": "Completed OPS", "Notes": None},
    {"Vessel": "LIBERTY PEACE", "Voyage": "75", "Port": "Apra Harbor", "Terminal": None, "Date of Arrival": "2025-07-08 11:10", "Date of Departure": "2025-09-08 04:44", "Status": "Pending Port Call", "Notes": None},
    {"Vessel": "LIBERTY PEACE", "Voyage": "75", "Port": "Shuaiba, Kuwait", "Terminal": None, "Date of Arrival": "08:48 08/25/25", "Date of Departure": "22:00 08/31/25", "Status": "Pending Port Call", "Notes": None},
    {"Vessel": "LIBERTY PEACE", "Voyage": "75", "Port": "Beaumont, TX", "Terminal": None, "Date of Arrival": "2025-02-10 04:19", "Date of Departure": "2025-05-10 17:01", "Status": "In Operation", "Notes": None},
    {"Vessel": "LIBERTY PEACE", "Voyage": "75", "Port": "Jacksonville, FL", "Terminal": None, "Date of Arrival": "2025-08-10 20:47", "Date of Departure": "2025-09-10 20:47", "Status": "Pending Port Call", "Notes": None},
    {"Vessel": "LIBERTY PEACE", "Voyage": "76", "Port": "Charleston - T.C Dock, SC", "Terminal": None, "Date of Arrival": "2025-10-10 08:19", "Date of Departure": "2025-11-10 01:25", "Status": "Pending Port Call", "Notes": None},
    {"Vessel": "LIBERTY POWER", "Voyage": "24", "Port": "Charleston - T.C Dock, SC", "Terminal": None, "Date of Arrival": "2025-11-07 06:00", "Date of Departure": "2025-11-07 23:00", "Status": "Pending Port Call", "Notes": None},
    {"Vessel": "LIBERTY POWER", "Voyage": "24", "Port": "Charleston, SC", "Terminal": "Columbus Street Terminal", "Date of Arrival": "2025-12-07 01:30", "Date of Departure": "2025-12-07 06:30", "Status": "Pending Port Call", "Notes": "BUNKERS ONLY"},
    {"Vessel": "LIBERTY POWER", "Voyage": "24", "Port": "Jacksonville, FL", "Terminal": None, "Date of Arrival": "2025-12-07 19:02", "Date of Departure": "14:00 07/14/25", "Status": "Pending Port Call", "Notes": None},
    {"Vessel": "LIBERTY POWER", "Voyage": "24", "Port": "Beaumont, TX", "Terminal": None, "Date of Arrival": "12:00 07/18/25", "Date of Departure": "15:30 07/29/25", "Status": "Pending Port Call", "Notes": "Aviation cargo ALD July 25"},
    {"Vessel": "LIBERTY POWER", "Voyage": "25", "Port": "Shuaiba, Kuwait", "Terminal": None, "Date of Arrival": "20:14 08/30/25", "Date of Departure": "2025-05-09 04:46", "Status": "Pending Port Call", "Notes": "Cargo availability 9/1"},
    {"Vessel": "LIBERTY POWER", "Voyage": "25", "Port": "Duqm, Oman", "Terminal": None, "Date of Arrival": "2025-07-09 19:12", "Date of Departure": "2025-12-09 04:46", "Status": "Pending Port Call", "Notes": "Cargo availability 9/8."},
    {"Vessel": "LIBERTY POWER", "Voyage": "25", "Port": "Charleston - T.C Dock, SC", "Terminal": None, "Date of Arrival": "2025-12-10 18:06", "Date of Departure": "18:06 10/13/25", "Status": "Pending Port Call", "Notes": None},
    {"Vessel": "LIBERTY POWER", "Voyage": "25", "Port": "Jacksonville, FL", "Terminal": None, "Date of Arrival": "06:14 10/14/25", "Date of Departure": "06:14 10/15/25", "Status": "Pending Port Call", "Notes": None},
    {"Vessel": "LIBERTY POWER", "Voyage": "25", "Port": "Beaumont, TX", "Terminal": None, "Date of Arrival": "08:14 10/18/25", "Date of Departure": "08:14 10/19/25", "Status": "Pending Port Call", "Notes": None}
]

df = pd.DataFrame(data)

# Initialize session state for conversation
if "stage" not in st.session_state:
    st.session_state.stage = "greeting"
    st.session_state.vessel = None
    st.session_state.voyage = None
    st.session_state.port = None

st.title("🛳️ LGLDubaiBot")

# Display conversation
if st.session_state.stage == "greeting":
    st.markdown("**LGLDubaiBot:** Hi! 👋 Welcome to LGLDubaiBot. Please ask me anything about a vessel.")
    user_input = st.text_input("You:", key="vessel_input")
    if user_input:
        vessels = df["Vessel"].unique()
        matches = [v for v in vessels if user_input.strip().upper() in v.upper()]
        if matches:
            st.session_state.vessel = matches[0]
            st.session_state.stage = "voyage"
        else:
            st.markdown("**LGLDubaiBot:** Sorry, I couldn't find that vessel. Please try again.")

elif st.session_state.stage == "voyage":
    voyages = df[df["Vessel"] == st.session_state.vessel]["Voyage"].unique()
    st.markdown(f"**LGLDubaiBot:** I found vessel **{st.session_state.vessel}**. Available voyages: {', '.join(voyages)}")
    user_input = st.text_input("Select a voyage:", key="voyage_input")
    if user_input and user_input in voyages:
        st.session_state.voyage = user_input
        st.session_state.stage = "port"
    elif user_input:
        st.markdown("**LGLDubaiBot:** Please enter a valid voyage number.")

elif st.session_state.stage == "port":
    ports = df[(df["Vessel"] == st.session_state.vessel) & (df["Voyage"] == st.session_state.voyage)]["Port"].unique()
    st.markdown(f"**LGLDubaiBot:** Voyage **{st.session_state.voyage}** includes the following ports: {', '.join(ports)}")
    user_input = st.text_input("Select a port:", key="port_input")
    if user_input and user_input in ports:
        st.session_state.port = user_input
        st.session_state.stage = "details"
    elif user_input:
        st.markdown("**LGLDubaiBot:** Please enter a valid port name.")

elif st.session_state.stage == "details":
    row = df[(df["Vessel"] == st.session_state.vessel) &
             (df["Voyage"] == st.session_state.voyage) &
             (df["Port"] == st.session_state.port)].iloc[0]
    st.markdown(f"**LGLDubaiBot:** Here are the port call details for **{row['Vessel']}**, Voyage **{row['Voyage']}**, Port **{row['Port']}**:")
    st.markdown(f"- **Terminal**: {row['Terminal'] or 'N/A'}")
    st.markdown(f"- **Arrival**: {row['Date of Arrival']}")
    st.markdown(f"- **Departure**: {row['Date of Departure']}")
    st.markdown(f"- **Status**: {row['Status']}")
    st.markdown(f"- **Notes**: {row['Notes'] or 'None'}")
    if st.button("Ask another question"):
        st.session_state.stage = "greeting"
        st.session_state.vessel = None
        st.session_state.voyage = None
        st.session_state.port = None

