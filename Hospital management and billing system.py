from abc import ABC, abstractmethod

# ==========================================
# 1. DATA ABSTRACTION & ENCAPSULATION
# ==========================================
class BillableService(ABC):
    @abstractmethod
    def calculate_charges(self):
        pass


# ==========================================
# 2. INHERITANCE (Base Person Class)
# ==========================================
class Person:
    def __init__(self, name, age, contact_number):
        self._name = name  # Protected attribute (Encapsulation)
        self._age = age
        self._contact_number = contact_number

    def get_details(self):
        return f"Name: {self._name}, Age: {self._age}, Contact: {self._contact_number}"


# ==========================================
# 3. MULTILEVEL & MULTIPLE INHERITANCE (Staff)
# ==========================================
class Staff(Person):
    def __init__(self, name, age, contact_number, staff_id, salary):
        super().__init__(name, age, contact_number)
        self.__staff_id = staff_id  # Private attribute (Encapsulation)
        self._salary = salary

    def get_staff_id(self):
        return self.__staff_id


class AdministrativeRole:
    def __init__(self, admin_level):
        self._admin_level = admin_level

    def get_admin_duties(self):
        return f"Administrative Level: {self._admin_level}"


class Doctor(Staff, AdministrativeRole):
    def __init__(self, name, age, contact_number, staff_id, salary, specialization, admin_level):
        Staff.__init__(self, name, age, contact_number, staff_id, salary)
        AdministrativeRole.__init__(self, admin_level)
        self._specialization = specialization

    def get_details(self):
        return f"Dr. {self._name} ({self._specialization}) - ID: {self.get_staff_id()}"


class Nurse(Staff):
    def __init__(self, name, age, contact_number, staff_id, salary, shift):
        super().__init__(name, age, contact_number, staff_id, salary)
        self._shift = shift

    def get_details(self):
        return f"Nurse {self._name} ({self._shift} Shift) - ID: {self.get_staff_id()}"


# ==========================================
# 4. COMPOSITION (Appointment & Department)
# ==========================================
class Appointment:
    def __init__(self, appointment_id, date, doctor, patient):
        self._appointment_id = appointment_id
        self._date = date
        self._doctor = doctor
        self._patient = patient

    def get_appointment_info(self):
        return f"Appointment ID: {self._appointment_id} on {self._date} with {self._doctor.get_details()}"


class Department:
    def __init__(self, dept_name):
        self._dept_name = dept_name
        self._staff_members = []  # Composition: Department contains staff members

    def add_staff(self, staff):
        self._staff_members.append(staff)

    def list_staff(self):
        return [staff.get_details() for staff in self._staff_members]


# ==========================================
# 5. INHERITANCE, METHOD OVERRIDING & POLYMORPHISM (Patient)
# ==========================================
class Patient(Person, BillableService):
    def __init__(self, name, age, contact_number, patient_id):
        Person.__init__(self, name, age, contact_number)
        self._patient_id = patient_id
        self.__medical_records = []  # Encapsulated sensitive data
        self._appointments = []      # Composition: Patient has appointments

    def add_medical_record(self, record):
        self.__medical_records.append(record)

    def view_medical_records(self):
        return self.__medical_records

    def book_appointment(self, appointment):
        self._appointments.append(appointment)

    def calculate_charges(self):
        return 100.0  # Base consultation fee


class RegularPatient(Patient):
    def __init__(self, name, age, contact_number, patient_id, base_treatment_cost):
        super().__init__(name, age, contact_number, patient_id)
        self._base_treatment_cost = base_treatment_cost

    def calculate_charges(self):
        return self._base_treatment_cost + 50.0


class EmergencyPatient(Patient):
    def __init__(self, name, age, contact_number, patient_id, emergency_fee):
        super().__init__(name, age, contact_number, patient_id)
        self._emergency_fee = emergency_fee

    def calculate_charges(self):
        return self._emergency_fee + 200.0


class InsuredPatient(Patient):
    def __init__(self, name, age, contact_number, patient_id, treatment_cost, insurance_coverage_percent):
        super().__init__(name, age, contact_number, patient_id)
        self._treatment_cost = treatment_cost
        self.__insurance_coverage = insurance_coverage_percent

    def calculate_charges(self):
        discounted_amount = self._treatment_cost * (1 - (self.__insurance_coverage / 100))
        return max(0.0, discounted_amount)


# ==========================================
# 6. DEMONSTRATION & WORKFLOW
# ==========================================
if __name__ == "__main__":
    print("=== SMART HOSPITAL MANAGEMENT & BILLING SYSTEM ===")
    
    cardiology_dept = Department("Cardiology")
    
    doc1 = Doctor("Kamal Perera", 45, "0771234567", "DOC101", 150000.0, "Cardiologist", "Senior Consultant")
    nurse1 = Nurse("Nimali Silva", 30, "0719876543", "NUR202", 75000.0, "Morning")
    
    cardiology_dept.add_staff(doc1)
    cardiology_dept.add_staff(nurse1)
    
    print(f"\n[Department: Cardiology Staff]")
    for staff_info in cardiology_dept.list_staff():
        print(f" - {staff_info}")

    pat1 = RegularPatient("Sunil Fernando", 50, "0701112233", "P001", 300.0)
    pat2 = EmergencyPatient("Amara Jayasinghe", 28, "0754445566", "P002", 500.0)
    pat3 = InsuredPatient("Priyal Perera", 42, "0789998877", "P003", 1000.0, 40.0)

    apt1 = Appointment("APT-001", "2026-10-15", doc1, pat1)
    pat1.book_appointment(apt1)
    pat1.add_medical_record("Diagnosed with mild hypertension.")

    print("\n[Processing Patient Bills using Polymorphism]")
    patients_list = [pat1, pat2, pat3]
    
    for patient in patients_list:
        total_bill = patient.calculate_charges()
        print(f"Patient ID: {patient._patient_id} ({patient._name}) -> Total Treatment Charge: ${total_bill:.2f}")

    print("\n[Encapsulation Check]")
    print(f"Viewing Medical Records for Sunil: {pat1.view_medical_records()}")