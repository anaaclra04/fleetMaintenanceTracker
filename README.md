# fleetMaintenanceTracker

A Streamlit web application for tracking fleet vehicle maintenance, fuel receipts, trips, and driver assignments, backed by a MySQL database, built as a SQL project for COP4710.

## Description

The app connects to a MySQL database named `FleetMaintenance` and provides a multi-page interface with the following sections:

- **Dashboard** — KPI metrics (total vehicles, active drivers, total fuel spend, total service spend), a bar chart of fuel spend by vehicle, a pie chart of service cost by type, and a table of recent trips.
- **Vehicles** — View all vehicles and add new ones (VIN, make, model, year, color, mileage).
- **Drivers** — View all drivers and add new ones (license number, name, phone number).
- **Fuel Receipts** — View all fueling events with a monthly cost trend line chart, and log new fuel receipts.
- **Service Events** — View maintenance history with charts for top-cost vehicles and event counts by type, and log new service events from a predefined list of service types.
- **Trips** — View the journey log with a miles-per-driver bar chart, and log new trips with origin, destination, distance, vehicle, and driver.
- **Assignments** — View driver-to-vehicle assignment history and create new assignments with optional end dates.

All pages support creating new records via forms that write directly to the MySQL database.

## Tech Stack

- Python
- Streamlit 1.35.0
- MySQL (via mysql-connector-python 8.4.0)
- pandas 2.2.2
- Plotly 5.22.0

## Installation

```bash
pip3 install -r requirements.txt
```

## Usage

```bash
python3 -m streamlit run app.py
```

To access the database directly:

```bash
mysql -u root -p FleetMaintenance
```

Database connection settings (host, user, password, database name) are read from Streamlit secrets, defaulting to a local `root` connection to `FleetMaintenance`.

## ER Diagram


<img width="2284" height="1730" alt="Screenshot 2026-04-07 at 7 21 32 PM" src="https://github.com/user-attachments/assets/f75b5b42-3db1-4439-9b45-cd3c2e5a05cf" />
