import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, datetime
import os

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="FleetTrack",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL STYLE
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Mono', monospace;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #0a0a0f;
    border-right: 1px solid #1e1e2e;
}
section[data-testid="stSidebar"] * {
    color: #c9d1d9 !important;
}
section[data-testid="stSidebar"] .stRadio label {
    font-family: 'DM Mono', monospace;
    font-size: 0.82rem;
    letter-spacing: 0.05em;
}

/* ── Main background ── */
.stApp { background: #0d0d17; }

/* ── Headings ── */
h1, h2, h3 {
    font-family: 'Syne', sans-serif !important;
    letter-spacing: -0.02em;
}

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: #13131f;
    border: 1px solid #1e1e2e;
    border-radius: 8px;
    padding: 1rem 1.25rem;
}
[data-testid="metric-container"] label {
    color: #6e7681 !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #e6edf3 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 1.6rem !important;
}

/* ── Dataframes ── */
.stDataFrame { border-radius: 8px; overflow: hidden; }

/* ── Buttons ── */
.stButton > button {
    background: #238636;
    color: #fff;
    border: none;
    border-radius: 6px;
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    letter-spacing: 0.05em;
    padding: 0.5rem 1.25rem;
    transition: background 0.2s;
}
.stButton > button:hover { background: #2ea043; }

/* ── Form inputs ── */
.stTextInput input, .stNumberInput input,
.stDateInput input, .stSelectbox select {
    background: #13131f !important;
    border: 1px solid #30363d !important;
    border-radius: 6px !important;
    color: #e6edf3 !important;
    font-family: 'DM Mono', monospace !important;
}

/* ── Section header pill ── */
.section-pill {
    display: inline-block;
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.7rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #58a6ff;
    margin-bottom: 0.75rem;
}

/* ── Page title bar ── */
.page-title {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #e6edf3;
    margin-bottom: 0.25rem;
}
.page-sub {
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    color: #484f58;
    margin-bottom: 2rem;
    letter-spacing: 0.05em;
}

/* ── Divider ── */
hr { border-color: #1e1e2e !important; }

/* ── Success / error alerts ── */
.stAlert { border-radius: 8px; }

/* ── Tab styling ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: #13131f;
    border-radius: 8px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 6px;
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.05em;
    color: #6e7681;
    padding: 6px 16px;
}
.stTabs [aria-selected="true"] {
    background: #238636 !important;
    color: #fff !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  DB CONNECTION
# ─────────────────────────────────────────────
@st.cache_resource
def get_connection():
    return mysql.connector.connect(
        host=st.secrets.get("DB_HOST", "localhost"),
        user=st.secrets.get("DB_USER", "root"),
        password=st.secrets.get("DB_PASSWORD", ""),
        database=st.secrets.get("DB_NAME", "FleetMaintenance"),
    )

def run_query(sql: str, params=None) -> pd.DataFrame:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(sql, params or ())
    rows = cursor.fetchall()
    cursor.close()
    return pd.DataFrame(rows)

def run_write(sql: str, params=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql, params or ())
    conn.commit()
    cursor.close()

# ─────────────────────────────────────────────
#  SIDEBAR NAV
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding:1.5rem 0 1rem 0;'>
        <div style='font-family:Syne,sans-serif;font-size:1.4rem;font-weight:800;color:#e6edf3;'>
            🚛 FleetTrack
        </div>
        <div style='font-size:0.65rem;color:#484f58;letter-spacing:0.1em;margin-top:2px;'>
            MAINTENANCE SYSTEM
        </div>
    </div>
    <hr style='border-color:#1e1e2e;margin-bottom:1.5rem;'/>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        [
            "📊  Dashboard",
            "🚗  Vehicles",
            "👤  Drivers",
            "⛽  Fuel Receipts",
            "🔧  Service Events",
            "🗺️  Trips",
            "🔗  Assignments",
        ],
        label_visibility="collapsed",
    )

    st.markdown("<hr style='border-color:#1e1e2e;margin-top:2rem;'/>", unsafe_allow_html=True)
    st.markdown(
        "<div style='font-size:0.65rem;color:#484f58;letter-spacing:0.08em;padding-top:0.5rem;'>"
        "FleetMaintenance DB · v1.0</div>",
        unsafe_allow_html=True,
    )

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def pill(label):
    st.markdown(f"<div class='section-pill'>{label}</div>", unsafe_allow_html=True)

def page_header(title, subtitle):
    st.markdown(f"<div class='page-title'>{title}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='page-sub'>{subtitle}</div>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGES
# ─────────────────────────────────────────────

# ── DASHBOARD ──────────────────────────────
if page == "📊  Dashboard":
    page_header("Dashboard", "Fleet overview — live from database")

    # KPI row
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        n = run_query("SELECT COUNT(*) AS n FROM Vehicles").iloc[0]["n"]
        st.metric("Total Vehicles", n)
    with c2:
        n = run_query("SELECT COUNT(*) AS n FROM Drivers").iloc[0]["n"]
        st.metric("Active Drivers", n)
    with c3:
        n = run_query("SELECT COALESCE(SUM(Cost),0) AS n FROM FuelReceipt").iloc[0]["n"]
        st.metric("Total Fuel Spend", f"${float(n):,.2f}")
    with c4:
        n = run_query("SELECT COALESCE(SUM(Cost),0) AS n FROM ServiceEvents").iloc[0]["n"]
        st.metric("Total Service Spend", f"${float(n):,.2f}")

    st.markdown("<br/>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    with col_a:
        pill("FUEL SPEND BY VEHICLE")
        df = run_query("""
            SELECT CONCAT(v.Make,' ',v.Model) AS Vehicle,
                   ROUND(SUM(f.Cost),2) AS Total_Cost
            FROM FuelReceipt f JOIN Vehicles v ON f.VIN=v.VIN
            GROUP BY f.VIN ORDER BY Total_Cost DESC
        """)
        if not df.empty:
            fig = px.bar(df, x="Vehicle", y="Total_Cost",
                         color="Total_Cost",
                         color_continuous_scale=["#1a3a2a","#238636","#56d364"],
                         template="plotly_dark",
                         labels={"Total_Cost":"$ Spent"})
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                coloraxis_showscale=False,
                margin=dict(l=0,r=0,t=10,b=0),
                font_family="DM Mono",
            )
            st.plotly_chart(fig, use_container_width=True)

    with col_b:
        pill("SERVICE COST BY TYPE")
        df2 = run_query("""
            SELECT Type, ROUND(SUM(Cost),2) AS Total
            FROM ServiceEvents GROUP BY Type ORDER BY Total DESC LIMIT 8
        """)
        if not df2.empty:
            fig2 = px.pie(df2, names="Type", values="Total",
                          hole=0.55,
                          color_discrete_sequence=px.colors.sequential.Greens_r,
                          template="plotly_dark")
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0,r=0,t=10,b=0),
                font_family="DM Mono",
                showlegend=True,
                legend=dict(font=dict(size=10)),
            )
            st.plotly_chart(fig2, use_container_width=True)

    pill("RECENT TRIPS")
    df3 = run_query("""
        SELECT t.Date, d.Name AS Driver,
               CONCAT(v.Make,' ',v.Model) AS Vehicle,
               t.FromLocation, t.ToLocation,
               t.Distance_Miles AS Miles
        FROM Trips t
        JOIN Drivers d ON t.LicenseNumber=d.LicenseNumber
        JOIN Vehicles v ON t.VIN=v.VIN
        ORDER BY t.Date DESC LIMIT 10
    """)
    st.dataframe(df3, use_container_width=True, hide_index=True)


# ── VEHICLES ───────────────────────────────
elif page == "🚗  Vehicles":
    page_header("Vehicles", "Manage the fleet roster")
    tab1, tab2 = st.tabs(["  View All  ", "  Add Vehicle  "])

    with tab1:
        df = run_query("SELECT * FROM Vehicles ORDER BY Year DESC")
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab2:
        pill("NEW VEHICLE")
        with st.form("add_vehicle"):
            c1, c2 = st.columns(2)
            vin   = c1.text_input("VIN", max_chars=17)
            make  = c2.text_input("Make")
            model = c1.text_input("Model")
            year  = c2.number_input("Year", min_value=1990, max_value=2030, value=2023)
            color = c1.text_input("Color")
            mileage = c2.number_input("Mileage", min_value=0, value=0)
            submitted = st.form_submit_button("Add Vehicle")
            if submitted:
                try:
                    run_write(
                        "INSERT INTO Vehicles VALUES (%s,%s,%s,%s,%s,%s)",
                        (vin, make, model, int(year), color, int(mileage)),
                    )
                    st.success(f"Vehicle {vin} added.")
                    st.cache_resource.clear()
                except Exception as e:
                    st.error(str(e))


# ── DRIVERS ────────────────────────────────
elif page == "👤  Drivers":
    page_header("Drivers", "Driver roster and records")
    tab1, tab2 = st.tabs(["  View All  ", "  Add Driver  "])

    with tab1:
        df = run_query("SELECT * FROM Drivers ORDER BY Name")
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab2:
        pill("NEW DRIVER")
        with st.form("add_driver"):
            c1, c2 = st.columns(2)
            lic   = c1.text_input("License Number")
            name  = c2.text_input("Full Name")
            phone = c1.text_input("Phone Number")
            submitted = st.form_submit_button("Add Driver")
            if submitted:
                try:
                    run_write(
                        "INSERT INTO Drivers VALUES (%s,%s,%s)",
                        (lic, name, phone),
                    )
                    st.success(f"Driver '{name}' added.")
                    st.cache_resource.clear()
                except Exception as e:
                    st.error(str(e))


# ── FUEL RECEIPTS ──────────────────────────
elif page == "⛽  Fuel Receipts":
    page_header("Fuel Receipts", "Track fueling events across the fleet")
    tab1, tab2 = st.tabs(["  View All  ", "  Add Receipt  "])

    with tab1:
        df = run_query("""
            SELECT f.ReceiptID, f.Date,
                   CONCAT(v.Make,' ',v.Model,' (',v.VIN,')') AS Vehicle,
                   f.GallonsPurchased, f.Cost
            FROM FuelReceipt f JOIN Vehicles v ON f.VIN=v.VIN
            ORDER BY f.Date DESC
        """)
        st.dataframe(df, use_container_width=True, hide_index=True)

        pill("COST TREND")
        trend = run_query("""
            SELECT DATE_FORMAT(Date,'%Y-%m') AS Month,
                   ROUND(SUM(Cost),2) AS Total
            FROM FuelReceipt GROUP BY Month ORDER BY Month
        """)
        if not trend.empty:
            fig = px.line(trend, x="Month", y="Total",
                          markers=True,
                          template="plotly_dark",
                          labels={"Total":"$ Spent","Month":"Month"},
                          color_discrete_sequence=["#56d364"])
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0,r=0,t=10,b=0),
                font_family="DM Mono",
            )
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        pill("NEW FUEL RECEIPT")
        vins = run_query("SELECT VIN, CONCAT(Make,' ',Model) AS label FROM Vehicles")
        vin_map = {f"{r['label']} ({r['VIN']})": r["VIN"] for _, r in vins.iterrows()}

        with st.form("add_fuel"):
            c1, c2 = st.columns(2)
            chosen_vin = c1.selectbox("Vehicle", list(vin_map.keys()))
            receipt_date = c2.date_input("Date", value=date.today())
            cost    = c1.number_input("Cost ($)", min_value=0.0, format="%.2f")
            gallons = c2.number_input("Gallons Purchased", min_value=0.0, format="%.2f")
            submitted = st.form_submit_button("Add Receipt")
            if submitted:
                try:
                    run_write(
                        "INSERT INTO FuelReceipt (Date,Cost,GallonsPurchased,VIN) VALUES (%s,%s,%s,%s)",
                        (receipt_date, cost, gallons, vin_map[chosen_vin]),
                    )
                    st.success("Fuel receipt added.")
                    st.cache_resource.clear()
                except Exception as e:
                    st.error(str(e))


# ── SERVICE EVENTS ─────────────────────────
elif page == "🔧  Service Events":
    page_header("Service Events", "Maintenance history for every vehicle")
    tab1, tab2 = st.tabs(["  View All  ", "  Log Event  "])

    with tab1:
        df = run_query("""
            SELECT s.ServiceID, s.Date,
                   CONCAT(v.Make,' ',v.Model) AS Vehicle,
                   s.Type, s.Cost
            FROM ServiceEvents s JOIN Vehicles v ON s.VIN=v.VIN
            ORDER BY s.Date DESC
        """)
        st.dataframe(df, use_container_width=True, hide_index=True)

        col_a, col_b = st.columns(2)
        with col_a:
            pill("TOP COST VEHICLES")
            top = run_query("""
                SELECT CONCAT(v.Make,' ',v.Model) AS Vehicle,
                       ROUND(SUM(s.Cost),2) AS Total
                FROM ServiceEvents s JOIN Vehicles v ON s.VIN=v.VIN
                GROUP BY s.VIN ORDER BY Total DESC
            """)
            fig = px.bar(top, x="Total", y="Vehicle", orientation="h",
                         template="plotly_dark",
                         color_discrete_sequence=["#238636"])
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0,r=0,t=10,b=0),
                font_family="DM Mono",
            )
            st.plotly_chart(fig, use_container_width=True)

        with col_b:
            pill("EVENTS BY TYPE")
            types = run_query("""
                SELECT Type, COUNT(*) AS Count
                FROM ServiceEvents GROUP BY Type ORDER BY Count DESC
            """)
            fig2 = px.bar(types, x="Count", y="Type", orientation="h",
                          template="plotly_dark",
                          color_discrete_sequence=["#1f6feb"])
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0,r=0,t=10,b=0),
                font_family="DM Mono",
            )
            st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        pill("LOG SERVICE EVENT")
        vins = run_query("SELECT VIN, CONCAT(Make,' ',Model) AS label FROM Vehicles")
        vin_map = {f"{r['label']} ({r['VIN']})": r["VIN"] for _, r in vins.iterrows()}
        SERVICE_TYPES = [
            "Oil Change","Tire Rotation","Tire Replacement","Brake Inspection",
            "Brake Pad Replacement","Air Filter Replacement","Transmission Service",
            "Transmission Repair","Wheel Alignment","Engine Tune-Up",
            "AC Repair","Annual Inspection","Software Update/Check","Other",
        ]
        with st.form("add_service"):
            c1, c2 = st.columns(2)
            chosen_vin   = c1.selectbox("Vehicle", list(vin_map.keys()))
            svc_date     = c2.date_input("Date", value=date.today())
            svc_type     = c1.selectbox("Service Type", SERVICE_TYPES)
            cost         = c2.number_input("Cost ($)", min_value=0.0, format="%.2f")
            submitted    = st.form_submit_button("Log Event")
            if submitted:
                try:
                    run_write(
                        "INSERT INTO ServiceEvents (Date,Type,Cost,VIN) VALUES (%s,%s,%s,%s)",
                        (svc_date, svc_type, cost, vin_map[chosen_vin]),
                    )
                    st.success("Service event logged.")
                    st.cache_resource.clear()
                except Exception as e:
                    st.error(str(e))


# ── TRIPS ──────────────────────────────────
elif page == "🗺️  Trips":
    page_header("Trips", "Journey log across the fleet")
    tab1, tab2 = st.tabs(["  View All  ", "  Log Trip  "])

    with tab1:
        df = run_query("""
            SELECT t.TripID, t.Date, d.Name AS Driver,
                   CONCAT(v.Make,' ',v.Model) AS Vehicle,
                   t.FromLocation, t.ToLocation,
                   t.Distance_Miles AS Miles
            FROM Trips t
            JOIN Drivers d ON t.LicenseNumber=d.LicenseNumber
            JOIN Vehicles v ON t.VIN=v.VIN
            ORDER BY t.Date DESC
        """)
        st.dataframe(df, use_container_width=True, hide_index=True)

        pill("MILES PER DRIVER")
        miles = run_query("""
            SELECT d.Name, ROUND(SUM(t.Distance_Miles),1) AS Total_Miles
            FROM Trips t JOIN Drivers d ON t.LicenseNumber=d.LicenseNumber
            GROUP BY d.Name ORDER BY Total_Miles DESC
        """)
        fig = px.bar(miles, x="Name", y="Total_Miles",
                     template="plotly_dark",
                     color_discrete_sequence=["#1f6feb"],
                     labels={"Total_Miles":"Miles","Name":"Driver"})
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0,r=0,t=10,b=0),
            font_family="DM Mono",
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        pill("LOG TRIP")
        vins = run_query("SELECT VIN, CONCAT(Make,' ',Model) AS label FROM Vehicles")
        vin_map = {f"{r['label']} ({r['VIN']})": r["VIN"] for _, r in vins.iterrows()}
        drivers = run_query("SELECT LicenseNumber, Name FROM Drivers ORDER BY Name")
        drv_map = {f"{r['Name']} ({r['LicenseNumber']})": r["LicenseNumber"] for _, r in drivers.iterrows()}

        with st.form("add_trip"):
            c1, c2 = st.columns(2)
            chosen_vin = c1.selectbox("Vehicle", list(vin_map.keys()))
            chosen_drv = c2.selectbox("Driver", list(drv_map.keys()))
            trip_date  = c1.date_input("Date", value=date.today())
            distance   = c2.number_input("Distance (Miles)", min_value=0.0, format="%.1f")
            from_loc   = c1.text_input("From Location")
            to_loc     = c2.text_input("To Location")
            submitted  = st.form_submit_button("Log Trip")
            if submitted:
                try:
                    run_write(
                        "INSERT INTO Trips (Date,Distance_Miles,FromLocation,ToLocation,VIN,LicenseNumber) VALUES (%s,%s,%s,%s,%s,%s)",
                        (trip_date, distance, from_loc, to_loc,
                         vin_map[chosen_vin], drv_map[chosen_drv]),
                    )
                    st.success("Trip logged.")
                    st.cache_resource.clear()
                except Exception as e:
                    st.error(str(e))


# ── ASSIGNMENTS ────────────────────────────
elif page == "🔗  Assignments":
    page_header("Assignments", "Driver ↔ Vehicle assignment history")
    tab1, tab2 = st.tabs(["  View All  ", "  New Assignment  "])

    with tab1:
        df = run_query("""
            SELECT a.AssignmentID, d.Name AS Driver,
                   CONCAT(v.Make,' ',v.Model,' (',v.VIN,')') AS Vehicle,
                   a.StartDate, IFNULL(CAST(a.EndDate AS CHAR),'Active') AS EndDate
            FROM DriverVehicleAssignment a
            JOIN Drivers d ON a.LicenseNumber=d.LicenseNumber
            JOIN Vehicles v ON a.VIN=v.VIN
            ORDER BY a.StartDate DESC
        """)
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab2:
        pill("NEW ASSIGNMENT")
        vins = run_query("SELECT VIN, CONCAT(Make,' ',Model) AS label FROM Vehicles")
        vin_map = {f"{r['label']} ({r['VIN']})": r["VIN"] for _, r in vins.iterrows()}
        drivers = run_query("SELECT LicenseNumber, Name FROM Drivers ORDER BY Name")
        drv_map = {f"{r['Name']} ({r['LicenseNumber']})": r["LicenseNumber"] for _, r in drivers.iterrows()}

        with st.form("add_assignment"):
            c1, c2 = st.columns(2)
            chosen_drv  = c1.selectbox("Driver", list(drv_map.keys()))
            chosen_vin  = c2.selectbox("Vehicle", list(vin_map.keys()))
            start_date  = c1.date_input("Start Date", value=date.today())
            open_ended  = c2.checkbox("Currently Active (no end date)", value=True)
            end_date    = None
            if not open_ended:
                end_date = c2.date_input("End Date", value=date.today())
            submitted = st.form_submit_button("Create Assignment")
            if submitted:
                try:
                    run_write(
                        "INSERT INTO DriverVehicleAssignment (StartDate,EndDate,VIN,LicenseNumber) VALUES (%s,%s,%s,%s)",
                        (start_date, end_date,
                         vin_map[chosen_vin], drv_map[chosen_drv]),
                    )
                    st.success("Assignment created.")
                    st.cache_resource.clear()
                except Exception as e:
                    st.error(str(e))
