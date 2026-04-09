-- Create the Database
CREATE DATABASE FleetMaintenance;
USE FleetMaintenance;

-- 1. Parent Tables (No Foreign Keys)
CREATE TABLE Vehicles (
    VIN VARCHAR(17) PRIMARY KEY,
    Make VARCHAR(50),
    Model VARCHAR(50),
    Year INT,
    Color VARCHAR(20),
    Mileage INT
);

CREATE TABLE Drivers (
    LicenseNumber VARCHAR(20) PRIMARY KEY,
    Name VARCHAR(100),
    PhoneNumber VARCHAR(15)
);

-- 2. Child Tables (Reference the Parents)
CREATE TABLE FuelReceipt (
    ReceiptID INT AUTO_INCREMENT PRIMARY KEY,
    Date DATE,
    Cost DECIMAL(10, 2),
    GallonsPurchased DECIMAL(7, 2),
    VIN VARCHAR(17),
    FOREIGN KEY (VIN) REFERENCES Vehicles(VIN)
);

CREATE TABLE ServiceEvents (
    ServiceID INT AUTO_INCREMENT PRIMARY KEY,
    Date DATE,
    Type VARCHAR(100),
    Cost DECIMAL(10, 2),
    VIN VARCHAR(17),
    FOREIGN KEY (VIN) REFERENCES Vehicles(VIN)
);

CREATE TABLE Trips (
    TripID INT AUTO_INCREMENT PRIMARY KEY,
    Date DATE,
    Distance_Miles DECIMAL(7, 2),
    FromLocation VARCHAR(100),
    ToLocation VARCHAR(100),
    VIN VARCHAR(17),
    LicenseNumber VARCHAR(20),
    FOREIGN KEY (VIN) REFERENCES Vehicles(VIN),
    FOREIGN KEY (LicenseNumber) REFERENCES Drivers(LicenseNumber)
);

CREATE TABLE DriverVehicleAssignment (
    AssignmentID INT AUTO_INCREMENT PRIMARY KEY,
    StartDate DATE,
    EndDate DATE,
    VIN VARCHAR(17),
    LicenseNumber VARCHAR(20),
    FOREIGN KEY (VIN) REFERENCES Vehicles(VIN),
    FOREIGN KEY (LicenseNumber) REFERENCES Drivers(LicenseNumber)
);

