import pymssql


class FillingVaccines:
    ''' Adds the Vaccines to the DB and adds inventory '''
    def __init__(self, vaccine, shotsNeeded, dosesLeft, cursor):
        # passing in parameters into database and assuming the inventory starts out at 500 doses per vaccine type
        self.sqltext = "INSERT INTO Vaccines (VaccineName, ShotsNeeded, DosesLeft) VALUES ('" + vaccine + "', " + str(shotsNeeded) + "," + str(dosesLeft) + ")"
        print(self.sqltext)
        self.vaccineId = 0
        try: 
            cursor.execute(self.sqltext)
            cursor.connection.commit()
            cursor.execute("SELECT @@IDENTITY AS 'Identity'; ")
            _identityRow = cursor.fetchone()
            self.vaccineId = _identityRow['Identity']
            # cursor.connection.commit()
            print('Query executed successfully. Vaccine : ' + vaccine 
            +  ' added to the database using Vaccine ID = ' + str(self.vaccineId))
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for Vaccines! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1])
            print("SQL text that resulted in an Error: " + self.sqltext)

    def AddDoses(self, vaccineName, doseAmount, cursor):
        cursor.execute("SELECT DosesLeft FROM Vaccines WHERE VaccineName = '" + vaccineName + "'")
        currentDoses = cursor.fetchone()
        self.sqltext = "UPDATE Vaccines SET DosesLeft = " + str(doseAmount + currentDoses['DosesLeft']) + " WHERE VaccineName = '" + vaccineName + "'"
        try: 
            cursor.execute(self.sqltext)
            cursor.connection.commit()
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for adding vaccines! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1])
            print("SQL text that resulted in an Error: " + self.sqltext)

    def ReserveDoses(self, personId, vaccineName, cursor):
        cursor.execute("SELECT ShotsNeeded FROM Vaccines, VaccineAppointment WHERE Vaccines.VaccineId = VaccineAppointment.VaccineId AND PatientId = " + str(personId))
        reservedShots = cursor.fetchone()
        cursor.execute("SELECT DosesLeft FROM Vaccines WHERE VaccineName = '" + vaccineName + "'")
        doses = cursor.fetchone()
        self.sqltext = "UPDATE Vaccines SET DosesLeft = " + str(doses['DosesLeft'] - reservedShots['ShotsNeeded']) + " WHERE VaccineName = '" + vaccineName + "'"
        
        try: 
            cursor.execute(self.sqltext)
            cursor.connection.commit()
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for reserving vaccines! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1])
            print("SQL text that resulted in an Error: " + self.sqltext)

class VaccinePatients:
    ''' Adds Patients to DB '''
    def __init__(self, fname, lname, email, zipcode, cursor):
        self.sqltext = "INSERT INTO Patients (FirstName, LastName, Email, ZipCode) VALUES ('" + fname + "', '" + lname + "', '" + email + "', " + str(zipcode) + ")"
        self.patientId = 0
        try: 
            cursor.execute(self.sqltext)
            cursor.connection.commit()
            cursor.execute("SELECT @@IDENTITY AS 'Identity'; ")
            _identityRow = cursor.fetchone()
            self.patientId = _identityRow['Identity']
            # cursor.connection.commit()
            print('Query executed successfully. Patient contact : ' + email 
            +  ' added to the database using Patient ID = ' + str(self.patientId))
        except pymssql.Error as db_err:
            print("Database Programming Error in SQL Query processing for Patient! ")
            print("Exception code: " + str(db_err.args[0]))
            if len(db_err.args) > 1:
                print("Exception message: " + db_err.args[1])
            print("SQL text that resulted in an Error: " + self.sqltext)

class Appointments:
    ''' Adds Appointments to DB '''
    def __init__(self, fname, lname, email, vaccine, cursor):
        cursor.execute("SELECT PatientId FROM Patients WHERE FirstName =  '" + fname + "' AND LastName = '" + lname + "' AND Email = '" + email + "'")
        patient = cursor.fetchone()
        cursor.execute("SELECT VaccineId FROM Vaccines WHERE VaccineName = '" + vaccine + "'")
        vaccineType = cursor.fetchone()
        cursor.execute("SELECT COUNT(*) AS num FROM Patients WHERE PatientId = " + str(patient['PatientId']))
        rowcount = cursor.rowcount
        patientCount = cursor.fetchone()
        cursor.execute("SELECT ShotsNeeded FROM Vaccines WHERE VaccineName = '" + vaccine + "'")
        shotsNeeded = cursor.fetchone()
        
        if rowcount == 0 or rowcount < shotsNeeded['ShotsNeeded']:
            self.sqltext = "INSERT INTO VaccineAppointment (PatientId, VaccineId, ShotNumber) VALUES (" + str(patient['PatientId']) + ", " + str(vaccineType['VaccineId']) + ", " + str(patientCount['num'] + 1) + ")"
            self.appointmentId = 0
            try: 
                cursor.execute(self.sqltext)
                cursor.connection.commit()
                cursor.execute("SELECT @@IDENTITY AS 'Identity'; ")
                _identityRow = cursor.fetchone()
                self.appointmentId = _identityRow['Identity']
                # cursor.connection.commit()
                print('Query executed successfully. Appointment for : ' + fname 
                +  ' added to the database using Appointment ID = ' + str(self.appointmentId))
            except pymssql.Error as db_err:
                print("Database Programming Error in SQL Query processing for Appointment! ")
                print("Exception code: " + str(db_err.args[0]))
                if len(db_err.args) > 1:
                    print("Exception message: " + db_err.args[1])
                print("SQL text that resulted in an Error: " + self.sqltext)