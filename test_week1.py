import unittest
import os

from sql_connection_manager import SqlConnectionManager
from COVID19_vaccine import FillingVaccines, VaccinePatients, Appointments
from enums import *
from utils import *

class TestFillingVaccines(unittest.TestCase):
    def test_init(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)
                    # create a new Vaccineobject
                    self.add_vaccine = FillingVaccines("Johnson&Johnson", 1, 500, cursor)
                    # check if the vaccine is correctly inserted into the database
                    sqlQuery = '''
                               SELECT *
                               FROM Vaccines
                               WHERE VaccineName = 'Johnson&Johnson'
                               '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    if len(rows) < 1:
                        self.fail("Creating vaccine failed")
                    # clear the tables after testing, just in-case
                    # clear_tables(sqlClient)
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Creating vaccine failed")
    
    def test_add_doses(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)
                    # create a new Vaccine object
                    initial_doses = 500
                    self.add_vaccine = FillingVaccines("Johnson&Johnson", 1, initial_doses, cursor)
                    self.add_vaccine.AddDoses('Johnson&Johnson', 300, cursor)
                    # check if doses are added
                    sqlQuery = '''
                               SELECT DosesLeft
                               FROM Vaccines
                               WHERE VaccineName = 'Johnson&Johnson'
                               '''
                    cursor.execute(sqlQuery)
                    doses = cursor.fetchone()
                    if doses['DosesLeft'] != initial_doses + 300:
                        self.fail("Adding doses failed")
                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Adding doses failed")

    def test_reserve_doses(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)
                    # create a new Vaccine and Patient object
                    initial_doses = 500
                    self.add_vaccine = FillingVaccines("Johnson&Johnson", 1, initial_doses, cursor)
                    self.add_patient = VaccinePatients("Christie", "Gan", "clgan@uw.edu", 98115, cursor)
                    self.add_appointment = Appointments("Christie", "Gan", "clgan@uw.edu", "Johnson&Johnson", cursor)
                    cursor.execute("SELECT PatientId FROM Patients WHERE FirstName = 'Christie' AND LastName = 'Gan' AND Email = 'clgan@uw.edu'")
                    patient = cursor.fetchone()
                    self.add_vaccine.ReserveDoses(patient['PatientId'], "Johnson&Johnson", cursor)
                    # check if doses are reserved
                    sqlQuery = '''
                               SELECT DosesLeft
                               FROM Vaccines
                               WHERE VaccineName = 'Johnson&Johnson'
                               '''
                    cursor.execute(sqlQuery)
                    doses = cursor.fetchone()
                    if doses['DosesLeft'] != initial_doses - 1:
                        self.fail("Reserving doses failed")
                    # clear the tables after testing, just in-case
                    clear_tables(sqlClient)
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Reserving doses failed")


class TestAppointments(unittest.TestCase):
    def test_init(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)
                    # create a new objects for Appointments
                    initial_doses = 500
                    self.add_vaccine = FillingVaccines("Johnson&Johnson", 1, initial_doses, cursor)
                    self.add_patient = VaccinePatients("Christie", "Gan", "clgan@uw.edu", 98115, cursor)
                    self.add_appointment = Appointments("Christie", "Gan", "clgan@uw.edu", "Johnson&Johnson", cursor)
                    sqlQuery = '''
                               SELECT *
                               FROM VaccineAppointment
                               WHERE PatientId = (SELECT PatientId 
                                    FROM Patients
                                    WHERE FirstName = 'Christie'
                                    AND LastName = 'Gan'
                                    AND Email = 'clgan@uw.edu')
                                AND VaccineId = (SELECT VaccineId
                                    FROM Vaccines
                                    WHERE VaccineName = 'Johnson&Johnson')
                               '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    if len(rows) < 1:
                        self.fail("Creating appointment failed")
                    # clear the tables after testing, just in-case
                    # clear_tables(sqlClient)
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Creating appointment failed")
                    

class TestVaccinePatients(unittest.TestCase):
    def test_init(self):
        with SqlConnectionManager(Server=os.getenv("Server"),
                                  DBname=os.getenv("DBName"),
                                  UserId=os.getenv("UserID"),
                                  Password=os.getenv("Password")) as sqlClient:
            with sqlClient.cursor(as_dict=True) as cursor:
                try:
                    # clear the tables before testing
                    clear_tables(sqlClient)
                    # create a new Patient object
                    self.add_vaccine = VaccinePatients("Christie", "Gan", "clgan@uw.edu", 98115, cursor)
                    # check if the patient is correctly inserted into the database
                    sqlQuery = '''
                               SELECT *
                               FROM Patients
                               WHERE FirstName = 'Christie'
                               AND LastName = 'Gan'
                               AND Email = 'clgan@uw.edu'
                               '''
                    cursor.execute(sqlQuery)
                    rows = cursor.fetchall()
                    if len(rows) < 1:
                        self.fail("Creating patient failed")
                    # clear the tables after testing, just in-case
                    # clear_tables(sqlClient)
                except Exception:
                    # clear the tables if an exception occurred
                    clear_tables(sqlClient)
                    self.fail("Creating patient failed")

if __name__ == '__main__':
    unittest.main()