from django.db import models
from django.contrib.auth.models import User
from django.template import loader, Context

class Tent(models.Model):
    #The name of the tent
    name = models.CharField(max_length=40)

    #A description of the tent
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    @property
    def assignedDoctors(self):
        return Doctor.objects.filter(tent=self)

    @property
    def assignedPatients(self):
        return len(Patient.objects.filter(tent=self))

    #An html representation of the tent object
    @property
    def html(self):
        itemTemplate = loader.get_template('tent.html')
        context = Context({'tent':self})
        return itemTemplate.render(context).replace('\n', '')

class Doctor(models.Model):
    #The account for the doctor
    user = models.OneToOneField(User)

    #A tent that the doctor works at
    tent = models.ForeignKey(Tent, blank=True, null=True)

    def __unicode__(self):
        return self.user.username

class Patient(models.Model):
    #Name of the patient
    name = models.CharField(blank=True, default="", max_length=40)

    #Conscious or unconscious
    conscious = models.IntegerField(blank=True, default=-1)

    #Needs immediate attention
    emergency = models.IntegerField(blank=True, default=-1)

    #Age of the patient
    age = models.IntegerField(blank=True, default=-1)

    #Sex of the patient
    sex = models.CharField(max_length=10, blank=True, default="Unknown")

    #Determines if the patient is treated already
    treated = models.BooleanField(blank=True, default=False)

    #The tent the patient was assigned to
    tent = models.ForeignKey(Tent, blank=True, null=True)

    #The doctor that treated the patient
    doctor = models.ForeignKey(Doctor, blank=True, null=True)

    #Determines how quickly a patient should be seen
    priority = models.IntegerField(blank=True, default=-1)

    #Determines if the patient is alive or not
    alive = models.BooleanField(blank=True, default=True)

    #Determines if the patient has been identified
    identified = models.BooleanField(blank=True, default=False)

    #Picture of the patients face
    image = models.ImageField(blank=True)

    def __unicode__(self):
        return str(self.pk)

    #An html representation of the patient object
    @property
    def html(self):
        itemTemplate = loader.get_template('patient.html')
        context = Context({'patient':self})
        return itemTemplate.render(context).replace('\n', '')

    @property
    def injury(self):
        try:
            injury = Injury.objects.get(patient=self)
            return injury
        except:
            pass
        #Should never happen


    @property
    def is_conscious(self):
        if self.conscious:
            return "Yes"
        return "No"

    @property
    def is_emergency(self):
        if self.emergency:
            return "Yes"
        return "No"


class Injury(models.Model):
    category = models.CharField(max_length=100)

    patient = models.ForeignKey(Patient)

    image = models.ImageField(blank=True)

    def __unicode__(self):
        return str(self.pk)

class Statistic(models.Model):

    #An html representation of the tent object
    @property
    def html(self):
        itemTemplate = loader.get_template('statistic.html')
        context = Context({'statistic':self})
        return itemTemplate.render(context).replace('\n', '')

    @property
    def numberOfAlivePatients(self):
        patients = Patient.objects.filter(alive=True)
        return len(patients)

    @property
    def numberOfPatients(self):
        patients = Patient.objects.all()
        return len(patients)

    @property
    def numberOfDeaths(self):
        patients = Patient.objects.filter(alive=False)
        return len(patients)

    @property
    def numberOfDoctors(self):
        patients = Doctor.objects.all()
        return len(patients)

    @property
    def ratioOfPatientsDoctors(self):
        doctors = self.numberOfDoctors
        if doctors == 0:
            return 0
        return self.numberOfPatients / doctors

    @property
    def numberTreated(self):
        return len(Patient.objects.filter(treated=True))

    @property
    def numberNotTreated(self):
        return len(Patient.objects.filter(treated=False))

    @property
    def percentageOfMales(self):
        patients = float(self.numberOfPatients)
        if patients == 0:
            return 0
        males = float(len(Patient.objects.filter(sex="Male")))
        return "%.2f" % float((males / patients) * 100.0)

    @property
    def percentageOfFemales(self):
        return "%.2f" % float(100.0 - float(self.percentageOfMales))

    @property
    def percentageNotIdentified(self):
        not_identified = float(len(Patient.objects.filter(identified=False)))
        patients = float(self.numberOfPatients)
        if patients == 0:
            return 0
        return "%.2f" % float((not_identified / patients) * 100)

    @property
    def percentageIdentified(self):
        return "%.2f" % float(100.0 - float(self.percentageNotIdentified))

    def ageDistribution(self):
        patients = list(Patient.objects.all())
        age = [0, 0, 0, 0, 0, 0]
        for patient in patients:
            if patient.age <= 5:
                age[0] += 1
            elif patient.age <= 15:
                age[1] += 1
            elif patient.age <= 25:
                age[2] += 1
            elif patient.age <= 40:
                age[3] += 1
            elif patient.age <= 60:
                age[4] += 1
            else:
                age[5] += 1
        return age

    @property
    def between0And5(self):
        age = self.ageDistribution()
        group = float(age[0])
        patients = float(self.numberOfPatients)
        if patients == 0:
            return 0
        return "%.2f" % float((group / patients) * 100.0)

    @property
    def between6And15(self):
        age = self.ageDistribution()
        group = float(age[1])
        patients = float(self.numberOfPatients)
        if patients == 0:
            return 0
        return "%.2f" % float((group / patients) * 100.0)

    @property
    def between16And25(self):
        age = self.ageDistribution()
        group = float(age[2])
        patients = float(self.numberOfPatients)
        if patients == 0:
            return 0
        return "%.2f" % float((group / patients) * 100.0)

    @property
    def between26And40(self):
        age = self.ageDistribution()
        group = float(age[3])
        patients = float(self.numberOfPatients)
        if patients == 0:
            return 0
        return "%.2f" % float((group / patients) * 100.0)

    @property
    def between41And60(self):
        age = self.ageDistribution()
        group = float(age[4])
        patients = float(self.numberOfPatients)
        if patients == 0:
            return 0
        return "%.2f" % (float((group / patients) * 100.0))

    @property
    def above61(self):
        sum = float(self.between0And5) + float(self.between6And15) + float(self.between16And25) + float(self.between26And40) + float(self.between41And60)
        if self.numberOfPatients == 0:
            return 0
        return "%.2f" % float(100.0 - sum)