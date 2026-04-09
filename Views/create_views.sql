-- View 1: Fleet Financial Summary
-- This view combines your two "cost" tables (FuelReceipt and ServiceEvents) to show the total financial burden of every vehicle in your fleet. This is perfect for the "meaningful insight" requirement.

CREATE VIEW v_fleet_financials AS
SELECT 
    v.VIN, 
    v.Make, 
    v.Model,
    COALESCE(SUM(f.Cost), 0) AS Total_Fuel_Cost,
    COALESCE(SUM(s.Cost), 0) AS Total_Service_Cost,
    (COALESCE(SUM(f.Cost), 0) + COALESCE(SUM(s.Cost), 0)) AS Grand_Total_Cost
FROM Vehicles v
LEFT JOIN FuelReceipt f ON v.VIN = f.VIN
LEFT JOIN ServiceEvents s ON v.VIN = s.VIN
GROUP BY v.VIN;

-- View 2: Driver Activity Dashboard
-- This view joins Drivers and Trips to show who is doing the most work. It helps a manager see which drivers are active without having to look at the raw Trips table.

CREATE VIEW v_driver_activity AS
SELECT 
    d.Name, 
    d.LicenseNumber,
    COUNT(t.TripID) AS Total_Trips_Completed,
    SUM(t.Distance_Miles) AS Total_Miles_Driven
FROM Drivers d
LEFT JOIN Trips t ON d.LicenseNumber = t.LicenseNumber
GROUP BY d.LicenseNumber;
