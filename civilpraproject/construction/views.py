from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template

# Create your views here.
from .forms import *
from .models import *
from django.contrib import messages
# Create your views here.
# views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json

def vendor_registration(request):
    context = {}
    vendor = VendorForm(request.POST or None)
    if vendor.is_valid():
        vendor.save()

    else:
        print(request.POST)
        context['form'] = vendor

    return render(request, "vendor_registration.html", context)

def roughdrawing(request):
    context = {}
    rough = roughForm(request.POST or None )
    if rough.is_valid():
        print("HELOO______________________________________________________")
        rough.save()

    else:
        print(request.POST)
        context['form'] = rough

    return render(request, "rough_drawing.html", context)

def finaldrawing(request):
    context = {}
    final = finalForm(request.POST or None )
    if final.is_valid():
        print("HELOO______________________________________________________")
        final.save()

    else:
        print(request.POST)
        context['form'] = final

    return render(request, "final_drawing.html", context)



def assign_view(request):
    context = {}
    customer_name = Customer.objects.all()
    tasks = constructionlevel.objects.all()
    employees = employeeregistration.objects.all()

    if request.method == "POST":
        customer_id = request.POST.get('customer_id')
        site_id = request.POST.get('site_id')
        task_data = request.POST.get('taskData', '[]')
        task_list = json.loads(task_data)

        customer = get_object_or_404(Customer, id=customer_id)
        site = get_object_or_404(Site, id=site_id)

        master_data = masterdata.objects.create(customer=customer, site=site)

        for task_item in task_list:
            task_obj = get_object_or_404(constructionlevel, id=task_item['taskId'])
            assignee = get_object_or_404(employeeregistration, id=task_item['assignToId'])

            assign_two = None
            if task_item.get('assignTwoId'):
                assign_two = get_object_or_404(employeeregistration, id=task_item['assignTwoId'])

            assign_three = None
            if task_item.get('assignThreeId'):
                assign_three = get_object_or_404(employeeregistration, id=task_item['assignThreeId'])

            start_date = task_item['startDate']
            end_date = task_item['endDate']

            Taskttransaction.objects.create(
                customersid=master_data,
                task=task_obj,
                assign_to=assignee,
                assign_two=assign_two,
                assign_three=assign_three,
                start_date=start_date,
                end_date=end_date,
                state='assign'
            )

        return redirect('/search_masterdata')

    context["customer_name"] = customer_name
    context["tasks"] = tasks
    context["employees"] = employees

    return render(request, "task_assignments.html", context)

def get_sites(request, customer_id):
    sites = Site.objects.filter(customer_id=customer_id)
    site_list = [{'id': site.id, 'site_name': site.site_name} for site in sites]
    return JsonResponse(site_list, safe=False)
def search_assignmasterdata(request):
    sea = masterdata.objects.all()
    return render(request, "search_masterdata.html", {'data': sea})


def update_masterdata(request, id):
    branch = masterdata.objects.get(id=id)
    form = MasterdataForm(
        initial={'customer': branch.customer, 'site': branch.site, 'created_at': branch.created_at, })
    if request.method == "POST":
        form = MasterdataForm(request.POST, instance=branch)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                return redirect('/search_masterdata')
            except Exception as e:
                pass
    return render(request, 'update_masterdata.html', {'form': form})

def delete_masterdata(request, id):
    data = masterdata.objects.get(id=id)
    try:
        data.delete()
    except:
        pass
    return redirect('/search_masterdata')





def add_work_progress(request):
    if request.method == 'POST':
        form = WorkProgressForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/search_clientinquiry')

    else:
        form = WorkProgressForm()
    return render(request, 'add_work_progress.html', {'form': form})

def work_progress_list(request):
    progress_list = WorkProgress.objects.all()
    return render(request, 'work_progress_list.html', {'progress_list': progress_list})





# *****************************************************************************************************************

def customer_site_task_list(request):
    customers = Customer.objects.all()
    selected_customer = request.GET.get('customer')
    selected_site = request.GET.get('site')

    sites = Site.objects.filter(customer_id=selected_customer) if selected_customer else Site.objects.none()
    tasks = Taskttransaction.objects.filter(customersid__customer_id=selected_customer,
                                            customersid__site_id=selected_site) if selected_customer and selected_site else Taskttransaction.objects.none()

    context = {
        'customers': customers,
        'sites': sites,
        'tasks': tasks,
        'selected_customer': selected_customer,
        'selected_site': selected_site,
    }
    return render(request, 'task_search.html', context)



def assignee_task_list(request):
    assignees = employeeregistration.objects.all()
    selected_assignee = request.GET.get('assign_to')
    selected_customer = request.GET.get('customer')
    selected_site = request.GET.get('site')

    customers = Customer.objects.filter(masterdata__taskttransaction__assign_to_id=selected_assignee).distinct() if selected_assignee else Customer.objects.none()
    sites = Site.objects.filter(masterdata__taskttransaction__assign_to_id=selected_assignee, customer_id=selected_customer).distinct() if selected_assignee and selected_customer else Site.objects.none()
    tasks = Taskttransaction.objects.filter(assign_to_id=selected_assignee, customersid__customer_id=selected_customer, customersid__site_id=selected_site) if selected_assignee and selected_customer and selected_site else Taskttransaction.objects.none()

    context = {
        'assignees': assignees,
        'customers': customers,
        'sites': sites,
        'tasks': tasks,
        'selected_assignee': selected_assignee,
        'selected_customer': selected_customer,
        'selected_site': selected_site,
    }
    return render(request, 'assignee_task_list.html', context)

# *********************************************ooooooooo************************************

# Create your views here.



def creatematerial(request):
    context = {}
    if request.method == 'POST':
        print(request.POST)
        materialform = mastermateriallistform(request.POST)
        print(materialform)
        print(materialform.is_valid())
        if materialform.is_valid():
            materialform.save()
            return redirect('/searchmaterial')

        print(materialform.is_valid())
        context['form'] = materialform
    return render(request, "creatematerial.html", context)


def searchmaterial(request):
    materials = mastermateriallist.objects.all()
    return render(request, "searchmaterial.html", {'materials': materials})



def updatematerial(request, materialid):
    materials = mastermateriallist.objects.get(materialid=materialid)
    form = mastermateriallistform(
        initial={'materialname': materials.materialname,})
    if request.method == "POST":
        form = mastermateriallistform(request.POST, instance=materials)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                return redirect('/searchmaterial')
            except Exception as e:
                pass
    return render(request, 'updatematerial.html', {'form': form})



def deletematerial(request, materialid):
    materials = mastermateriallist.objects.get(materialid=materialid)
    try:
        materials.delete()
    except:
        pass
    return redirect('/searchmaterial')





# *******************************************************************************************************************

def createconstructionlevel(request):

    context = {}
    contruct = constructionlevelform(request.POST or None)
    if contruct.is_valid():
        print("HELOO______________________________________________________")
        contruct.save()
        return redirect('/searchconstructionlevel')

    else:
        print("HELOO______________________________________________________111")
        print(request.POST)
        messages.error(request,contruct.errors)
        context['form'] = contruct

    return render(request, "createconstructionlevel.html", context)


def searchconstructionlevel(request):
    levels = constructionlevel.objects.all()
    return render(request, "searchconstructionlevel.html", {'levels': levels})



def updateconstructionlevel(request,id):
    level = constructionlevel.objects.get(id=id)
    form = constructionlevelform(
        initial={'constructionlevelname': level.constructionlevelname, 'description': level.description,})
    if request.method == "POST":
        form = constructionlevelform(request.POST, instance=level)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                return redirect('/searchconstructionlevel')
            except Exception as e:
                pass
    return render(request, 'updateconstructionlevel.html', {'form': form})


def deleteconstructionlevel(request, id):
    level = constructionlevel.objects.get(id=id)
    try:
        level.delete()
    except:
        pass
    return redirect('/searchconstructionlevel')

#******************************************************************************************************************


def createcategory(request):
    context = {}
    if request.method == 'POST':
        print(request.POST)
        catform = categoryform(request.POST)
        print(catform)
        print(catform.is_valid())
        if catform.is_valid():
            catform.save()
            return redirect('/searchcategory')

        print(catform.is_valid())
        context['form'] = catform
    return render(request, "createcategory.html", context)


def searchcategory(request):
    categorys = Category.objects.all()
    return render(request, "searchcategory.html", {'categorys': categorys})



def updatecategory(request, categoryid):
    categorys = Category.objects.get(categoryid=categoryid)
    form = categoryform(
        initial={'categoryname': categorys.categoryname})
    if request.method == "POST":
        form = categoryform(request.POST, instance=categorys)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                return redirect('/searchcategory')
            except Exception as e:
                pass
    return render(request, 'updatecategory.html', {'form': form})



def deletecategory(request, categoryid):
    categorys = Category.objects.get(categoryid=categoryid)
    try:
        categorys.delete()
    except:
        pass
    return redirect('/searchcategory')


# *****************************************************************************************************************



def createunitmeasurement(request):
    context = {}
    if request.method == 'POST':
        print(request.POST)
        unitform = unitmeasurementform(request.POST)
        print(unitform)
        print(unitform.is_valid())
        if unitform.is_valid():
            unitform.save()
            return redirect('/searchunit')

        print(unitform.is_valid())
        context['form'] = unitform
    return render(request, "createunit.html", context)


def searchunitmeasurement(request):
    units = unitmeasurement.objects.all()
    return render(request, "searchunit.html", {'units': units})



def updateunitmeasurement(request, unitmeasurementid):
    units = unitmeasurement.objects.get(unitmeasurementid=unitmeasurementid)
    form = unitmeasurementform(
        initial={'unitmeasurementname': units.unitmeasurementname})
    if request.method == "POST":
        form = unitmeasurementform(request.POST, instance=units)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                return redirect('/searchunit')
            except Exception as e:
                pass
    return render(request, 'updateunit.html', {'form': form})



def deleteunitmeasurement(request, unitmeasurementid):
    units = unitmeasurement.objects.get(unitmeasurementid=unitmeasurementid)
    try:
        units.delete()
    except:
        pass
    return redirect('/searchunit')

# *****************************************************************************************************************

def createbrand(request):
    context = {}

    materialname = mastermateriallist.objects.all()
    brd = brandform(request.POST or None)
    if brd.is_valid():
        print("HELOO______________________________________________________")
        brd.save()
        return redirect('/searchbrand')

    else:
        print("HELOO______________________________________________________111")
        print(request.POST)
        messages.error(request, brd.errors)
        context['form'] = brd

    context["materialname"] = materialname
    return render(request, "createbrand.html", context)


def searchbrand(request):
    brands = brandlist.objects.all()
    return render(request, "searchbrand.html", {'brands': brands})


def updatebrand(request,id):
    brands = brandlist.objects.get(id=id)
    form = brandform(
        initial={'brandname': brands.brandname, 'materialnames': brands.materialnames, })
    if request.method == "POST":
        form = brandform(request.POST, instance=brands)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                return redirect('/searchbrand')
            except Exception as e:
                pass
    return render(request, 'updatebrand.html', {'form': form})



def deletebrand(request, id):
    brands = brandlist.objects.get(id=id)
    try:
        brands.delete()
    except:
        pass
    return redirect('/searchbrand')


# ************************************************************************************************************************


def createworktype(request):
    context = {}
    if request.method == 'POST':
        print(request.POST)
        workform = worktypesform(request.POST)
        print(workform)
        print(workform.is_valid())
        if workform.is_valid():
            workform.save()
            return redirect('/searchworktype')

        print(workform.is_valid())
        context['form'] = workform
    return render(request, "createworktype.html", context)


def searchworktype(request):
    works = worktypes.objects.all()
    return render(request, "searchworktype.html", {'works': works})


def updateworktype(request, worktypeid):
    works = worktypes.objects.get(worktypeid=worktypeid)
    form = worktypesform(
        initial={'worktypename': works.worktypename,'workdescription': works.workdescription})
    if request.method == "POST":
        form = worktypesform(request.POST, instance=works)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                return redirect('/searchworktype')
            except Exception as e:
                pass
    return render(request, 'updateworktype.html', {'form': form})



def deleteworktype(request, worktypeid):
    works = worktypes.objects.get(worktypeid=worktypeid)
    try:
        works.delete()
    except:
        pass
    return redirect('/searchworktype')

# *********************************************************************************************************************************



def createcustomer(request):
    context = {}
    if request.method == 'POST':
        print(request.POST)
        custform = customersform(request.POST)
        print(custform)
        print(custform.is_valid())
        if custform.is_valid():
            custform.save()
            return redirect('/searchcustomer')

        print(custform.is_valid())
        context['form'] = custform
    return render(request, "createcustomer.html", context)


def searchcustomer(request):
    custs = Customer.objects.all()
    return render(request, "searchcustomer.html", {'custs': custs})




def updatecustomer(request, id):
    custs = Customer.objects.get(id=id)
    form = customersform(
        initial={'customer_name': custs.customer_name,'emailids': custs.emailids,'phoneno': custs.phoneno,'address': custs.address})
    if request.method == "POST":
        form = customersform(request.POST, instance=custs)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                return redirect('/searchcustomer')
            except Exception as e:
                pass
    return render(request, 'updatecustomer.html', {'form': form})



def deletecustomer(request,id):
    custs = Customer.objects.get(id=id)
    try:
        custs.delete()
    except:
        pass
    return redirect('/searchcustomer')


# **************************************************************************************************************************

def createsite(request):
    context = {}

    customer_name = Customer.objects.all()
    sitess = siteform(request.POST or None)
    if sitess.is_valid():
        print("HELOO______________________________________________________")
        sitess.save()
        return redirect('/searchsite')

    else:
        print("HELOO______________________________________________________111")
        print(request.POST)
        messages.error(request, sitess.errors)
        context['form'] = sitess

    context["customer_name"] = customer_name
    return render(request, "createsite.html", context)


def searchsite(request):
    sitess = Site.objects.all()
    return render(request, "searchsite.html", {'sitess': sitess})


def updatesite(request,id):
    sitess = Site.objects.get(id=id)
    form = siteform(
        initial={'site_name': sitess.site_name, 'ownername': sitess.ownername,'pincode': sitess.pincode,
                 'state': sitess.state,'city': sitess.city,
                 'houseno': sitess.houseno,'roadname': sitess.roadname,'address': sitess.address,})
    if request.method == "POST":
        form = siteform(request.POST, instance=sitess)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                return redirect('/searchsite')
            except Exception as e:
                pass
    return render(request, 'updatesite.html', {'form': form})



def deletesite(request, id):
    sitess = Site.objects.get(id=id)
    try:
        sitess.delete()
    except:
        pass
    return redirect('/searchsite')

# **********************************************************************************************************************

# from django.shortcuts import render, get_object_or_404, redirect
# from django.http import JsonResponse
# from .models import Customer, MasterMaterialList, Category, UnitMeasurement, AddMaterial, Site
import json
import datetime

def material_management(request):
    customers = Customer.objects.all()
    material_names = mastermateriallist.objects.all()
    category_names = Category.objects.all()
    unit_measurement_names = unitmeasurement.objects.all()

    if request.method == "POST":
        material_data = request.POST.get('materialData')
        customer_id = request.POST.get('customers')
        site_id = request.POST.get('site')
        current_date = request.POST.get('currentdate')
        transfer_date = request.POST.get('transferdate')
        requirement_by = request.POST.get('requirementby')
        requirement_to = request.POST.get('requirementto')

        if material_data:
            material_list = json.loads(material_data)
            customer = Customer.objects.get(id=customer_id)
            site = Site.objects.get(id=site_id)

            for material_item in material_list:
                material = mastermateriallist.objects.get(materialid=material_item['materialId'])
                category = Category.objects.get(categoryid=material_item['categoryId'])
                unit = unitmeasurement.objects.get(unitmeasurementid=material_item['unitId'])
                quantity = material_item['quantity']
                specifications = material_item['specifications']

                addmaterial.objects.create(
                    customers=customer,
                    site=site,
                    currentdate=current_date,
                    transferdate=transfer_date,
                    materials=material,
                    categorys=category,
                    specifications=specifications,
                    units=unit,
                    quantitys=quantity,
                    requirementby=requirement_by,
                    requirementto=requirement_to,
                )

            return redirect('/searchaddmaterial')  # Redirect to a success page

    return render(request, 'createaddmaterial.html', {
        'customers': customers,
        'material_names': material_names,
        'category_names': category_names,
        'unit_measurement_names': unit_measurement_names,
    })


def get_sites(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    sites = Site.objects.filter(customer=customer)
    site_list = [{'id': site.id, 'name': site.site_name} for site in sites]
    return JsonResponse(site_list, safe=False)

def searchaddmaterial(request):
    addmates = addmaterial.objects.all()
    return render(request, "searchaddmaterial.html", {'addmates': addmates})

def updateaddmaterial(request,id):
    addmates = addmaterial.objects.get(id=id)
    form = addmaterialform(
        initial={'customers': addmates.customers, 'site': addmates.site,'currentdate': addmates.currentdate,
                 'transferdate': addmates.transferdate, 'materials': addmates.materials,'categorys': addmates.categorys,
                 'specifications': addmates.specifications, 'units': addmates.units,'quantitys': addmates.quantitys,
                 'requirementby': addmates.requirementby, 'requirementto': addmates.requirementto,})
    if request.method == "POST":
        form = addmaterialform(request.POST, instance=addmates)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                return redirect('/searchaddmaterial')
            except Exception as e:
                pass
    return render(request, 'updateaddmaterial.html', {'form': form})


def deleteaddmaterial(request, id):
    addmates = addmaterial.objects.get(id=id)
    try:
        addmates.delete()
    except:
        pass
    return redirect('/searchaddmaterial')


# **********************************************************************************************************************


from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import mastermateriallist, brandlist, unitmeasurement, internaltransfer
import json

def createinternaltransfer(request):
    context = {}

    material_list = mastermateriallist.objects.all()
    unit_list = unitmeasurement.objects.all()

    if request.method == "POST":
        transfer_data = request.POST.get('transferData', '[]')
        transfer_list = json.loads(transfer_data)

        for transfer_item in transfer_list:
            executive_engineer = transfer_item['executiveEngineer']
            executive_engineer_num = transfer_item['executiveEngineerNum']
            source_client_name = transfer_item['sourceClientName']
            source_address = transfer_item['sourceAddress']
            destination_client_name = transfer_item['destinationClientName']
            destination_address = transfer_item['destinationAddress']
            vehicle_name = transfer_item['vehicleName']
            vehicle_num = transfer_item['vehicleNum']
            driver_name = transfer_item['driverName']
            driver_num = transfer_item['driverNum']
            date = transfer_item['date']
            material = mastermateriallist.objects.get(materialid=transfer_item['materialId'])
            brand = brandlist.objects.get(brandname=transfer_item['brandName'])
            unit = unitmeasurement.objects.get(unitmeasurementid=transfer_item['unitId'])
            quantity = transfer_item['quantity']
            transfer_date = transfer_item['transferDate']

            internaltransfer.objects.create(
                executiveengineer=executive_engineer,
                executiveengineernum=executive_engineer_num,
                sourceclientname=source_client_name,
                sourceaddress=source_address,
                destinationclientname=destination_client_name,
                destinationaddress=destination_address,
                vehiclename=vehicle_name,
                vehiclenum=vehicle_num,
                drivername=driver_name,
                drivernum=driver_num,
                date=date,
                material=material,
                brand=brand,
                unit=unit,
                quantity=quantity,
                transferdate=transfer_date
            )

        messages.success(request, 'Internal transfers have been saved successfully!')
        return redirect('/searchinternaltransfer')  # Adjust this to your URL name

    context["material_list"] = material_list
    context["unit_list"] = unit_list
    return render(request, "createinternaltransfer.html", context)

def get_brands_by_material(request):
    material_id = request.GET.get('material_id')
    brands = brandlist.objects.filter(materialnames_id=material_id)
    brand_list = list(brands.values('id', 'brandname'))
    return JsonResponse(brand_list, safe=False)


def searchinternaltransfer(request):
    internals = internaltransfer.objects.all()
    return render(request, "searchinternaltransfer.html", {'internals': internals})


def updateinternaltransfer(request,id):
    internals = internaltransfer.objects.get(id=id)
    form = internaltransferform(
        initial={'executiveengineer': internals.executiveengineer, 'executiveengineernum': internals.executiveengineernum,'sourceclientname': internals.sourceclientname,
                 'sourceaddress': internals.sourceaddress, 'destinationclientname': internals.destinationclientname,'destinationaddress': internals.destinationaddress,
                 'vehiclename': internals.vehiclename, 'vehiclenum': internals.vehiclenum,'drivername': internals.drivername,
                 'drivernum': internals.drivernum, 'date': internals.date,'material': internals.material,
                 'brand': internals.brand, 'unit': internals.unit,'quantity': internals.quantity,'transferdate': internals.transferdate,})
    if request.method == "POST":
        form = internaltransferform(request.POST, instance=internals)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                return redirect('/searchinternaltransfer')
            except Exception as e:
                pass
    return render(request, 'updateinternaltransfer.html', {'form': form})



def deleteinternaltransfer(request, id):
    internals = internaltransfer.objects.get(id=id)
    try:
        internals.delete()
    except:
        pass
    return redirect('/searchinternaltransfer')

#***************************************************************************************************************************


from django.shortcuts import render, redirect
from .forms import employeeregistrationform

def createempregistration(request):
    if request.method == 'POST':
        form = employeeregistrationform(request.POST)
        if form.is_valid():
            form.save()
            return redirect('createempregistration')  # Redirect to a list view or any other page
    else:
        form = employeeregistrationform()
    return render(request, 'createempregistration.html', {'form': form})



def generate_employeeid(request):
    name = request.GET.get('name')
    if name:
        temp_employee = employeeregistration(employee_name=name)
        employeeid = temp_employee.generate_employeeid()
        return JsonResponse({'employeeid': employeeid})
    return JsonResponse({'error': 'Invalid name'}, status=400)


def searchempregistration(request):
    emplos = employeeregistration.objects.all()
    return render(request, "searchempregistration.html", {'emplos': emplos})


def updateempregistration(request,id):
    emplos = employeeregistration.objects.get(id=id)
    form = employeeregistrationform(
        initial={'employee_name': emplos.employee_name, 'employeeid': emplos.employeeid,'emailid': emplos.emailid,
                 'phonenum': emplos.phonenum,'dateofbirth': emplos.dateofbirth,'permanentaddress': emplos.permanentaddress,'presentaddress': emplos.presentaddress,
                 'gender': emplos.gender,'bloodgroup': emplos.bloodgroup,'status': emplos.status,
                 'bankacnum': emplos.bankacnum,'qualification': emplos.qualification,'aadharcard': emplos.aadharcard,'pancard': emplos.pancard,
                 'pfnum': emplos.pfnum,'pfeligibledate': emplos.pfeligibledate,'licencenum': emplos.licencenum,})
    if request.method == "POST":
        form = employeeregistrationform(request.POST, instance=emplos)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                return redirect('/searchempregistration')
            except Exception as e:
                pass
    return render(request, 'updateempregistration.html', {'form': form})



def deleteempregistration(request, id):
    emplos = employeeregistration.objects.get(id=id)
    try:
        emplos.delete()
    except:
        pass
    return redirect('/searchempregistration')


#***************************************************************************************************************************



def clientregview(request):
    context = {}
    client = clientregForm(request.POST or None )
    employee_name = employeeregistration.objects.all()
    if client.is_valid():
        print("HELOO______________________________________________________")
        client.save()
        return redirect('/search_clientreg')

    else:
        print(request.POST)
        context['form'] = client
    context["employee_name"] = employee_name

    return render(request, "client_registration.html", context)


def search_clientregs(request):
    reg = Client_registration.objects.all()
    return render(request, "search_clientreg.html", {'regs': reg})

def update_clientreg(request, id):
    branch = Client_registration.objects.get(id=id)
    form = clientregForm(
        initial={'client_name': branch.client_name, 'representative_name': branch.representative_name, 'phone_no': branch.phone_no, 'email': branch.email, 'site_address': branch.site_address, 'inquiry_date': branch.inquiry_date, })
    if request.method == "POST":
        form = clientregForm(request.POST, instance=branch)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                return redirect('/search_clientreg')
            except Exception as e:
                pass
    return render(request, 'update_clientreg.html', {'form': form})


def delete_clientreg(request, id):
    citys = Client_registration.objects.get(id=id)
    try:
        citys.delete()
    except:
        pass
    return redirect('/search_clientreg')

# **********************************************************************************************************************

def clientinquirygview(request):
    context = {}
    form = clientinquiryForm(request.POST or None)
    clients = Client_registration.objects.all()
    employees = employeeregistration.objects.all()
    con_type = constructiontype.objects.all()

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/search_clientinquiry')  # Redirect to a success page after saving

    context["form"] = form
    context["clients"] = clients
    context["employees"] = employees
    context["con_type"] = con_type

    return render(request, "client_inquiry_form.html", context)

def get_representatives(request):
    client_id = request.GET.get('client_id')
    representatives = employeeregistration.objects.filter(client_registration__id=client_id)
    data = [{"id": rep.id, "name": rep.employee_name} for rep in representatives]
    return JsonResponse(data, safe=False)

def search_clientinq(request):
    client = ClientInquiry.objects.all()
    return render(request, "search_clientinquiry.html", {'inq': client})


def update_clientinq(request, id):
    client = ClientInquiry.objects.get(id=id)
    form = clientinquiryForm(
        initial={'client_name': client.client_name, 'representative_name': client.representative_name, 'address': client.address, 'date': client.date, 'follow_off_date': client.follow_off_date, 'construction_type': client.construction_type,'remark': client.remark })
    if request.method == "POST":
        form = clientinquiryForm(request.POST, instance=client)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                return redirect('/search_clientinquiry')
            except Exception as e:
                pass
    return render(request, 'update_clientinquiry.html', {'form': form})


def delete_clientinq(request, id):
    client = ClientInquiry.objects.get(id=id)
    try:
        client.delete()
    except:
        pass
    return redirect('/search_clientinquiry')

# *********************************************************************************************************************

def constypeview(request):
    context = {}
    cons = constypeForm(request.POST or None )
    if cons.is_valid():
        print("HELOO______________________________________________________")
        cons.save()

    else:
        print(request.POST)
        context['form'] = cons

    return render(request, "insertconstruction_type.html", context)



#**********************************************************************************************************************************


def approvedinquiry_view(request):
    context = {}
    form = approvedinquiryform(request.POST or None)
    clients = Client_registration.objects.all()
    employees = employeeregistration.objects.all()
    work_types = worktypes.objects.all()

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('/search_approvedinquiry')  # Redirect to a success page after saving

    context["form"] = form
    context["clients"] = clients
    context["employees"] = employees
    context["work_types"] = work_types

    return render(request, "approvedinquiry.html", context)

def get_representatives(request):
    client_id = request.GET.get('client_id')
    representatives = employeeregistration.objects.filter(client_registration__id=client_id)
    client = Client_registration.objects.get(id=client_id)
    data = {
        "representatives": [{"id": rep.id, "name": rep.employee_name} for rep in representatives],
        "client_details": {
            "name": client.client_name,
            "phone_no": client.phone_no,
            "email": client.email,
            "site_address": client.site_address,
            "inquiry_date": client.inquiry_date
        }
    }
    return JsonResponse(data, safe=False)


def search_approvedinquiry(request):
    inquiries = approvedinquiry.objects.all()
    return render(request, "searchapprovedinquiry.html", {'inquiries': inquiries})


def update_approvedinquiry(request, id):
    approveds = approvedinquiry.objects.get(id=id)
    form = approvedinquiryform(
        initial={'client': approveds.client, 'employee': approveds.employee,'plotarea': approveds.plotarea,
                 'constructionarea': approveds.constructionarea, 'constructioncost': approveds.constructioncost,
                 'totalcost': approveds.totalcost, 'worktype': approveds.worktype, })
    if request.method == "POST":
        form = approvedinquiryform(request.POST, instance=approveds)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                return redirect('/search_approvedinquiry')
            except Exception as e:
                pass
    return render(request, 'updateapprovedinquiry.html', {'form': form})



def delete_approvedinquiry(request, id):
    approveds = approvedinquiry.objects.get(id=id)
    try:
        approveds.delete()
    except:
        pass
    return redirect('/search_approvedinquiry')
