-- Core CRUD Operations

-- 1. Insert the Vehicle (The Parent)
INSERT INTO Vehicles (VIN, Make, Model, Year, Color, Mileage) 
VALUES ('12345ABCDE67890', 'Toyota', 'Camry', 2024, 'Silver', 500);

-- 2. Insert the Driver (The other Parent)
INSERT INTO Drivers (LicenseNumber, Name, PhoneNumber) 
VALUES ('FL-999999', 'John Doe', '407-555-0199');

-- Insert: adding a new trip
INSERT INTO Trips (Date, Distance_Miles, FromLocation, ToLocation, VIN, LicenseNumber)
VALUES ('2026-04-08', 45.5, 'Orlando', 'Tampa', '12345ABCDE67890', 'FL-999999');

-- Update: Updating a vehicle's mileage after a service.
UPDATE Vehicles SET Mileage = 55000 WHERE VIN = '12345ABCDE67890';

-- Delete: Deleting a fuel receipt (or using a "Soft Delete" by setting a status to 'Inactive').
DELETE FROM FuelReceipt WHERE ReceiptID = 10;

-- Search & Filtering Queries (4 pts)

-- Filter by Date: "Show me all service events from last month."
SELECT * FROM ServiceEvents 
WHERE Date BETWEEN '2026-03-01' AND '2026-03-31';

-- Search by Driver: "Find all trips taken by a specific driver."
SELECT * FROM Trips 
WHERE LicenseNumber = 'FL-999999' 
ORDER BY Date DESC;

-- Reports & Aggregations (6 pts)

-- Report 1: Total Spending per Vehicle
SELECT v.Make, v.Model, SUM(s.Cost) AS Total_Maintenance_Cost
FROM Vehicles v
JOIN ServiceEvents s ON v.VIN = s.VIN
GROUP BY v.VIN;

-- Report 2: Fuel Efficiency
SELECT VIN, SUM(Cost) / SUM(GallonsPurchased) AS Average_Price_Per_Gallon
FROM FuelReceipt
GROUP BY VIN;

