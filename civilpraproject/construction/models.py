from django.db import models, transaction
from datetime import timezone

from django.db import models
from django.utils import timezone
import datetime
from django.core.validators import EmailValidator, RegexValidator
# Create your models here.

# master tables


class EmployeeIDCounter(models.Model):
    letter = models.CharField(max_length=1, unique=True)
    last_number = models.PositiveIntegerField(default=0)

class employeeregistration(models.Model):
    employee_name = models.CharField(max_length=50)
    employeeid = models.CharField(max_length=5, unique=True, blank=True)
    emailid = models.EmailField()
    phonenum = models.BigIntegerField()
    dateofbirth = models.DateField()
    permanentaddress = models.TextField()
    presentaddress = models.TextField()
    gender = models.CharField(max_length=15)
    bloodgroup = models.CharField(max_length=15)
    status = models.CharField(max_length=15)
    bankacnum = models.BigIntegerField()
    qualification = models.CharField(max_length=50)
    aadharcard = models.BigIntegerField()
    pancard = models.CharField(max_length=10)
    pfnum = models.CharField(max_length=22)
    pfeligibledate = models.DateField()
    licencenum = models.CharField(max_length=16)

    def save(self, *args, **kwargs):
        if not self.employeeid:
            self.employeeid = self.generate_employeeid()
        super().save(*args, **kwargs)

    def generate_employeeid(self):
        first_letter = self.employee_name[0].upper()

        with transaction.atomic():
            counter, created = EmployeeIDCounter.objects.select_for_update().get_or_create(letter=first_letter)
            counter.last_number += 1
            counter.save()
            employeeid = f"{first_letter}{counter.last_number:04d}"

        return employeeid

    def __str__(self):
        return self.employee_name

class constructiontype(models.Model):
    con_type = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.con_type

class Client_registration(models.Model):
    client_name = models.CharField(max_length=100)
    representative_name = models.ForeignKey(employeeregistration, on_delete=models.CASCADE)
    phone_no = models.IntegerField()
    email = models.EmailField()
    site_address = models.TextField()
    inquiry_date = models.DateField()

    def __str__(self):
        return self.client_name


class ClientInquiry(models.Model):
    client_name = models.ForeignKey(Client_registration, on_delete=models.CASCADE)
    representative_name = models.ForeignKey(employeeregistration, on_delete=models.CASCADE)
    address = models.TextField()
    date = models.DateField()
    follow_off_date = models.DateField()
    construction_type = models.ForeignKey(constructiontype, on_delete=models.CASCADE)
    remark = models.TextField()


class approvedinquiry(models.Model):
    customer_name = models.ForeignKey(Client_registration, on_delete=models.CASCADE)
    employee = models.ForeignKey(employeeregistration, on_delete=models.CASCADE)
    plotarea = models.IntegerField()
    constructionarea = models.IntegerField()
    constructioncost = models.IntegerField()
    totalcost = models.IntegerField()
    worktype = models.ForeignKey(constructiontype, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.customer_name)

class Site (models.Model):
    site_name = models.CharField(max_length=50)
    customer = models.ForeignKey(approvedinquiry, on_delete=models.CASCADE)
    pincode = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    houseno = models.CharField(max_length=50)
    roadname = models.CharField(max_length=50)
    address = models.CharField(max_length=350)

    def __str__(self):
        return str(self.site_name)

class constructionlevel (models.Model):
    constructionlevelname  = models.CharField(max_length=50)
    description = models.TextField()
    def __str__(self):
        return str(self.constructionlevelname)


class mastermateriallist (models.Model):
    materialid = models.AutoField(primary_key=True)
    materialname = models.CharField(max_length=50)
    def __str__(self):
        return str(self.materialname)



class Category (models.Model):
    categoryid = models.AutoField(primary_key=True)
    categoryname = models.CharField(max_length=50)
    def __str__(self):
        return str(self.categoryname)



class unitmeasurement (models.Model):
    unitmeasurementid = models.AutoField(primary_key=True)
    unitmeasurementname = models.CharField(max_length=50)
    def __str__(self):
        return str(self.unitmeasurementname)

class brandlist (models.Model):
    brandname = models.CharField(max_length=25)
    materialnames = models.ForeignKey(mastermateriallist, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.brandname)

class addmaterial (models.Model):
    customers = models.ForeignKey(approvedinquiry, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    currentdate = models.DateTimeField(default=datetime.datetime.now)
    transferdate = models.DateField()
    materials = models.ForeignKey(mastermateriallist, on_delete=models.CASCADE)
    categorys = models.ForeignKey(Category, on_delete=models.CASCADE)
    specifications = models.TextField()
    units = models.ForeignKey(unitmeasurement, on_delete=models.CASCADE)
    quantitys = models.IntegerField(blank=True, null=True)
    requirementby = models.CharField(max_length = 200)
    requirementto = models.CharField(max_length = 200)






# ********************************************************************************************************





# main form

class internaltransfer (models.Model):
    executiveengineer = models.CharField(max_length=50)
    executiveengineernum = models.BigIntegerField()
    sourceclientname = models.CharField(max_length=50)
    sourceaddress = models.TextField()
    destinationclientname = models.CharField(max_length=50)
    destinationaddress = models.TextField()
    vehiclename = models.CharField(max_length=50)
    vehiclenum = models.CharField(max_length=15)
    drivername = models.CharField(max_length=50)
    drivernum = models.BigIntegerField()
    date = models.DateField()
    material = models.ForeignKey(mastermateriallist, on_delete=models.CASCADE)
    brand = models.ForeignKey(brandlist, on_delete=models.CASCADE)
    unit = models.ForeignKey(unitmeasurement, on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=True, null=True)
    transferdate = models.DateTimeField()





class Vendor(models.Model):
    COMPANY_TYPES = (
        ('Sole Proprietorship', 'Sole Proprietorship'),
        ('Partnership', 'Partnership'),
        ('Limited Liability Partnership', 'Limited Liability Partnership'),
        ('Private Limited Company', 'Private Limited Company'),
        ('Public Limited Company', 'Public Limited Company'),
        ('Others', 'Others'),
    )

    vendor_name = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=50)
    contact_number = models.IntegerField()
    landline_number = models.IntegerField()
    registered_office_address = models.TextField()
    email = models.EmailField(validators=[EmailValidator()])
    gst_no = models.CharField(max_length=15, validators=[RegexValidator(regex=r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[0-9]{1}[Z]{1}[0-9]{1}$', message="Enter a valid GST number")])
    organization_type = models.CharField(max_length=50, choices=COMPANY_TYPES)
    nature_of_business = models.TextField()




class RoughDrawing(models.Model):
    project_name = models.CharField(max_length=100)
    client_name = models.CharField(max_length=100)
    executive_engg_name = models.CharField(max_length=100)
    date_of_submission = models.DateField()
    drawing_count = models.IntegerField()
    description = models.TextField()

class finaldrawing(models.Model):
    projectname = models.CharField(max_length=100)
    clientname = models.CharField(max_length=100)
    executiveenggname = models.CharField(max_length=100)
    dateofsubmission = models.DateField()
    drawingcount = models.IntegerField()
    description = models.TextField()




class masterdata(models.Model):
    customer = models.ForeignKey(approvedinquiry, on_delete=models.CASCADE)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    def __str__(self):
        return str(self.customer)





class Taskttransaction(models.Model):
    progresstatus = (
        ('To Do', 'To Do'),
        ('In Progress', 'In Progress'),
        ('Done', 'Done'),

    )
    customersid = models.ForeignKey(masterdata, on_delete=models.CASCADE)
    task = models.ForeignKey(constructionlevel, on_delete=models.CASCADE)
    assign_to = models.ForeignKey(employeeregistration, on_delete=models.CASCADE)
    assign_two = models.ForeignKey(employeeregistration, on_delete=models.CASCADE, related_name='assigned_two',blank=True,null=True)
    assign_three = models.ForeignKey(employeeregistration, on_delete=models.CASCADE, related_name='assigned_three',blank=True,null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    Status = models.CharField(max_length=50, choices=progresstatus, default='assign')


class WorkProgress(models.Model):
    photo = models.ImageField(upload_to='photos/')
    progress = models.IntegerField(default=0)
    worker_count = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Progress: {self.progress}%"

