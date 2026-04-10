-- Core CRUD Operations

-- 1. Insert the Vehicle (The Parent)
INSERT INTO Vehicles (VIN, Make, Model, Year, Color, Mileage) 
VALUES 	('12345ABCDE6789010', 'Toyota',     'Camry',       2024, 'Silver',   500),
		    ('1HGCM82633A123456', 'Honda',      'Civic',       2020, 'Blue',   45230),
		    ('2T1BURHE0JC123457', 'Toyota',     'Corolla',     2019, 'White',  62100),
		    ('3VWFE21C04M123458', 'Volkswagen', 'Jetta',       2021, 'Black',  31450),
		    ('4T1BF1FK5CU123459', 'Toyota',     'Camry',       2022, 'Black', 18900),
		    ('5YJSA1DN5DFP12345', 'Tesla',      'Model S',     2023, 'Red',     8750),
		    ('1FTFW1ET5DFC12346', 'Ford',       'F-150',       2018, 'Gray',   95400),
		    ('2GNFLFEK5G612347',  'Chevrolet',  'Equinox',     2020, 'White',  54300),
		    ('3GCUKREC0EG123480', 'Chevrolet',  'Silverado',   2017, 'Black', 112000);

-- 2. Insert the Driver (The other Parent)
INSERT INTO Drivers (LicenseNumber, Name, PhoneNumber) 
VALUES 	('FL-999999', 'John Doe',        '407-555-0199'),
		    ('FL-001234', 'James Carter',    '407-555-0101'),
        ('FL-003456', 'Robert Thompson', '321-555-0303'),
		    ('FL-004567', 'Angela Davis',    '321-555-0404'),
		    ('FL-005678', 'Kevin Patel',     '407-555-0505'),
		    ('FL-006789', 'Sandra Lee',      '813-555-0606');

-- Insert: adding a new trip
INSERT INTO Trips (Date, Distance_Miles, FromLocation, ToLocation, VIN, LicenseNumber)
VALUES 
-- Toyota Camry (Silver) trips
('2026-04-08', 45.5, 'Orlando', 'Tampa', '12345ABCDE67890', 'FL-999999'),
-- Honda Civic trips
('2024-08-01',  45.2, 'Orlando, FL',    'Kissimmee, FL',   '1HGCM82633A123456', 'FL-002345'),
('2024-08-15', 120.5, 'Orlando, FL',    'Tampa, FL',       '1HGCM82633A123456', 'FL-002345'),
('2024-09-03',  22.8, 'Orlando, FL',    'Sanford, FL',     '1HGCM82633A123456', 'FL-002345'),
('2024-10-10', 210.0, 'Orlando, FL',    'Miami, FL',       '1HGCM82633A123456', 'FL-002345'),
('2024-11-05',  88.4, 'Orlando, FL',    'Daytona Beach,FL','1HGCM82633A123456', 'FL-002345'),
-- Toyota Corolla trips
('2024-07-10',  55.0, 'Jacksonville,FL','St. Augustine,FL', '2T1BURHE0JC123457', 'FL-003456'),
('2024-08-05', 140.3, 'Jacksonville,FL','Orlando, FL',      '2T1BURHE0JC123457', 'FL-003456'),
('2024-09-20',  30.1, 'Jacksonville,FL','Orange Park, FL',  '2T1BURHE0JC123457', 'FL-003456'),
('2024-10-15', 320.7, 'Jacksonville,FL','Miami, FL',        '2T1BURHE0JC123457', 'FL-003456'),
('2024-11-12',  75.5, 'Jacksonville,FL','Gainesville, FL',  '2T1BURHE0JC123457', 'FL-003456'),
-- VW Jetta trips
('2024-09-05',  60.0, 'Tampa, FL',      'Clearwater, FL',  '3VWFE21C04M123458', 'FL-001234'),
('2024-10-12', 180.0, 'Tampa, FL',      'Orlando, FL',     '3VWFE21C04M123458', 'FL-001234'),
('2024-11-08',  42.3, 'Tampa, FL',      'Brandon, FL',     '3VWFE21C04M123458', 'FL-001234'),
-- Toyota Camry (Black) trips
('2024-09-14',  95.0, 'Miami, FL',      'Fort Lauderdale,FL','4T1BF1FK5CU123459','FL-005678'),
('2024-10-22', 265.0, 'Miami, FL',      'Orlando, FL',     '4T1BF1FK5CU123459', 'FL-005678'),
('2024-11-18',  38.5, 'Miami, FL',      'Coral Gables, FL','4T1BF1FK5CU123459', 'FL-005678'),
-- Tesla Model S trips
('2024-09-10', 310.0, 'Tallahassee,FL', 'Orlando, FL',     '5YJSA1DN5DFP12345', 'FL-006789'),
('2024-10-08', 155.0, 'Tallahassee,FL', 'Gainesville, FL', '5YJSA1DN5DFP12345', 'FL-006789'),
('2024-11-02',  85.0, 'Tallahassee,FL', 'Panama City, FL', '5YJSA1DN5DFP12345', 'FL-006789'),
-- Ford F-150 trips
('2024-07-01',  50.0, 'Fort Myers, FL', 'Naples, FL',      '1FTFW1ET5DFC12346', 'FL-004567'),
('2024-08-10', 110.5, 'Fort Myers, FL', 'Sarasota, FL',    '1FTFW1ET5DFC12346', 'FL-004567'),
('2024-09-18', 185.0, 'Fort Myers, FL', 'Tampa, FL',       '1FTFW1ET5DFC12346', 'FL-004567'),
('2024-10-25',  62.4, 'Fort Myers, FL', 'Cape Coral, FL',  '1FTFW1ET5DFC12346', 'FL-004567'),
('2024-11-14', 230.0, 'Fort Myers, FL', 'Orlando, FL',     '1FTFW1ET5DFC12346', 'FL-004567'),
-- Chevy Equinox trips
('2024-08-20',  78.0, 'Gainesville,FL', 'Ocala, FL',       '2GNFLFEK5G612347',  'FL-003456'),
('2024-09-25', 140.0, 'Gainesville,FL', 'Orlando, FL',     '2GNFLFEK5G612347',  'FL-003456'),
('2024-11-10',  55.5, 'Gainesville,FL', 'Lake City, FL',   '2GNFLFEK5G612347',  'FL-003456'),
-- Chevy Silverado trips
('2024-07-08',  95.0, 'Pensacola, FL',  'Mobile, AL',      '3GCUKREC0EG123480', 'FL-005678'),
('2024-08-19', 150.0, 'Pensacola, FL',  'Tallahassee, FL', '3GCUKREC0EG123480', 'FL-005678'),
('2024-09-28',  40.0, 'Pensacola, FL',  'Gulf Breeze, FL', '3GCUKREC0EG123480', 'FL-005678'),
('2024-10-30', 350.0, 'Pensacola, FL',  'Orlando, FL',     '3GCUKREC0EG123480', 'FL-005678'),
('2024-11-22',  80.0, 'Pensacola, FL',  'Destin, FL',      '3GCUKREC0EG123480', 'FL-005678');


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
WHERE LicenseNumber = 'FL-003456' 
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

