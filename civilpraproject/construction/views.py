from .forms import *
from .models import *
from django.contrib import messages
from django.http import JsonResponse
import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.utils import timezone
from datetime import datetime
from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm ,AuthenticationForm
from django.contrib.auth import login , logout
from .middlewares import *

def register_views(request):
    if request.method == 'POST':
        form= UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('/land')
    else:
        inital_data={'username':'', 'password':'','password2':''}
        form = UserCreationForm(initial = inital_data)

    return render(request,'auth/register.html',{'form':form})

def login_views(request):
    if request.method=='POST':
        form = AuthenticationForm(request,data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('/land')
    else:
        inital_data = {'username': '', 'password': ''}
        form = AuthenticationForm(initial = inital_data)
    return render(request,'auth/login.html',{'form':form})


def logout_views(request):
    logout(request)
    return redirect('login')

@auth
def dashboard_views(request):
    return render(request,'dashboard.html')

# ********************************************************************************************
@auth
def vendor_registration(request):
    context = {}
    vendor = VendorForm(request.POST or None)
    if vendor.is_valid():
        vendor.save()
        return redirect('/search_vendor-registration')

    else:
        print(request.POST)
        context['form'] = vendor

    return render(request, "vendor_registration.html", context)

@auth

def search_vendor_registration(request):
    records = Vendor.objects.all()
    mydict = {'records': records}
    return render(request, 'searchvendorreg.html', context=mydict)

@auth

def update_vendor_registration(request, id):
    branch = Vendor.objects.get(id=id)
    form = VendorForm(
        initial={'vendor_name': branch.vendor_name, 'contact_person': branch.contact_person,
                 'contact_number': branch.contact_number, 'landline_number': branch.landline_number,
                 'registered_office_address': branch.registered_office_address, 'email': branch.email,
                 'gst_no': branch.gst_no, 'organization_type': branch.organization_type,
                 'nature_of_business': branch.nature_of_business})
    if request.method == "POST":
        form = VendorForm(request.POST, instance=branch)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                return redirect('/search_vendor-registration')
            except Exception as e:
                pass
    return render(request, 'updatevendorreg.html', {'form': form})

@auth

def delete_vendor_registration(request, id):
    data = Vendor.objects.get(id=id)
    try:
        data.delete()
    except:
        pass
    return redirect('/search_vendor-registration')

@auth

def roughdrawing(request):
    context = {}
    rough = roughForm(request.POST or None)
    if rough.is_valid():
        print("HELOO______________________________________________________")
        rough.save()
        return redirect('/search_rough_drawing')


    else:
        print(request.POST)
        context['form'] = rough

    return render(request, "rough_drawing.html", context)

@auth

def search_roughdrawing(request):
    records = RoughDrawing.objects.all()
    mydict = {'records': records}
    return render(request, 'searchroughdrawing.html', context=mydict)

@auth

def update_roughdrawing(request, id):
    branch = RoughDrawing.objects.get(id=id)
    form = roughForm(
        initial={'project_name': branch.project_name, 'client_name': branch.client_name,
                 'executive_engg_name': branch.executive_engg_name, 'date_of_submission': branch.date_of_submission,
                 'drawing_count': branch.drawing_count, 'description': branch.description})
    if request.method == "POST":
        form = roughForm(request.POST, instance=branch)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                return redirect('/search_rough_drawing')
            except Exception as e:
                pass
    return render(request, 'updateroughdrawing.html', {'form': form})

@auth

def delete_roughdrawing(request, id):
    data = RoughDrawing.objects.get(id=id)
    try:
        data.delete()
    except:
        pass
    return redirect('/search_rough_drawing')

@auth

def Add_finaldrawing(request):
    context = {}
    final = finalForm(request.POST or None)
    if final.is_valid():
        print("HELOO______________________________________________________")
        final.save()
        return redirect('/search_final_drawing')


    else:
        print(request.POST)
        context['form'] = final

    return render(request, "final_drawing.html", context)

@auth

def search_finaldrawing(request):
    records = finaldrawing.objects.all()
    mydict = {'records': records}
    return render(request, 'searchfinaldrawing.html', context=mydict)

@auth

def update_finaldrawing(request, id):
    branch = finaldrawing.objects.get(id=id)
    form = finalForm(
        initial={'projectname': branch.projectname, 'clientname': branch.clientname,
                 'executiveenggname': branch.executiveenggname, 'dateofsubmission': branch.dateofsubmission,
                 'drawingcount': branch.drawingcount, 'description': branch.description})
    if request.method == "POST":
        form = finalForm(request.POST, instance=branch)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                return redirect('/search_final_drawing')
            except Exception as e:
                pass
    return render(request, 'updatefinaldrawing.html', {'form': form})

@auth

def delete_finaldrawing(request, id):
    data = finaldrawing.objects.get(id=id)
    try:
        data.delete()
    except:
        pass
    return redirect('/search_final_drawing')

@auth

def constypeview(request):
    context = {}
    cons = constypeForm(request.POST or None)
    if cons.is_valid():
        print("HELOO______________________________________________________")
        cons.save()
        return redirect('/searchconstruction_type')


    else:
        print(request.POST)
        context['form'] = cons

    return render(request, "insertconstruction_type.html", context)

@auth

def search_constypeview(request):
    records = constructiontype.objects.all()
    mydict = {'records': records}
    return render(request, 'searchconstruction_type.html', context=mydict)

@auth

def update_constypeview(request, id):
    branch = constructiontype.objects.get(id=id)
    form = constypeForm(
        initial={'con_type': branch.con_type, 'description': branch.description})
    if request.method == "POST":
        form = constypeForm(request.POST, instance=branch)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                return redirect('/searchconstruction_type')
            except Exception as e:
                pass
    return render(request, 'updateconstruction_type.html', {'form': form})

@auth

def delete_constypeview(request, id):
    records = constructiontype.objects.get(id=id)
    try:
        records.delete()
    except:
        pass
    return redirect('/searchconstruction_type')



@auth
def assign_view(request):
    context = {}
    customer_name = approvedinquiry.objects.all()
    tasks = constructionlevel.objects.all()
    employees = employeeregistration.objects.all()

    if request.method == "POST":
        customer_id = request.POST.get('customer_id')
        site_id = request.POST.get('site_id')
        task_data = request.POST.get('taskData', '[]')
        task_list = json.loads(task_data)

        customer = get_object_or_404(approvedinquiry, id=customer_id)
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
                Status='assign'
            )

        return redirect('/search_tasktransaction')

    context["customer_name"] = customer_name
    context["tasks"] = tasks
    context["employees"] = employees

    return render(request, "task_assignments.html", context)

def get_sites(request, customer_id):
    sites = Site.objects.filter(customer_id=customer_id)
    site_list = [{'id': site.id, 'site_name': site.site_name} for site in sites]
    return JsonResponse(site_list, safe=False)

def update_task(request, task_id):
    task = get_object_or_404(Taskttransaction, id=task_id)
    employees = employeeregistration.objects.all()
    tasks = constructionlevel.objects.all()

    if request.method == 'POST':
        task.assign_to_id = request.POST.get('assign_to_id')
        assign_two_id = request.POST.get('assign_two_id', None)
        task.assign_two_id = assign_two_id if assign_two_id else None

        assign_three_id = request.POST.get('assign_three_id', None)
        task.assign_three_id = assign_three_id if assign_three_id else None

        start_date = request.POST.get('start_date')
        task.start_date = start_date if start_date else None

        end_date = request.POST.get('end_date')
        task.end_date = end_date if end_date else None

        status = request.POST.get('Status')
        if status:
            task.Status = status

        task.save()
        return HttpResponseRedirect('/search_tasktransaction')

    return render(request, 'update_task.html', {
        'task': task,
        'employees': employees,
        'tasks': tasks,
        'status_upto': calculate_status_upto(task),
        'error_message': None
    })
def calculate_status_upto(task):
    today = datetime.now().date()
    if task.start_date and task.end_date:
        if task.start_date <= today <= task.end_date:
            total_days = (task.end_date - task.start_date).days
            completed_days = (today - task.start_date).days
            return (completed_days / total_days) * 100
        elif today > task.end_date:
            return 100
    return 0

@auth
def search_assigntransaction(request):
    sea = Taskttransaction.objects.all()
    return render(request, "search_Taskttransaction.html", {'task': sea})

@auth
def delete_assigntransaction(request, id):
    task = Taskttransaction.objects.get(id=id)
    try:
        task.delete()
    except:
        pass
    return redirect('/search_tasktransaction')


@auth
def search_assignmasterdata(request):
    sea = masterdata.objects.all()
    return render(request, "search_masterdata.html", {'data': sea})

@auth
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

@auth
def delete_masterdata(request, id):
    data = masterdata.objects.get(id=id)
    try:
        data.delete()
    except:
        pass
    return redirect('/search_masterdata')





@auth
def add_work_progress(request):
    if request.method == 'POST':
        form = WorkProgressForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/search_clientinquiry')

    else:
        form = WorkProgressForm()
    return render(request, 'add_work_progress.html', {'form': form})

@auth
def work_progress_list(request):
    progress_list = WorkProgress.objects.all()
    return render(request, 'work_progress_list.html', {'progress_list': progress_list})





# *****************************************************************************************************************

@auth
def customer_site_task_list(request):
    customers = approvedinquiry.objects.all()
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



@auth
def assignee_task_list(request):
    assignees = employeeregistration.objects.all()
    selected_assignee = request.GET.get('assign_to')
    selected_customer = request.GET.get('customer')
    selected_site = request.GET.get('site')

    customers = approvedinquiry.objects.filter(masterdata__taskttransaction__assign_to_id=selected_assignee).distinct() if selected_assignee else approvedinquiry.objects.none()
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


@auth
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

@auth
def searchmaterial(request):
    materials = mastermateriallist.objects.all()
    return render(request, "searchmaterial.html", {'materials': materials})


@auth
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


@auth
def deletematerial(request, materialid):
    materials = mastermateriallist.objects.get(materialid=materialid)
    try:
        materials.delete()
    except:
        pass
    return redirect('/searchmaterial')





# *******************************************************************************************************************
@auth
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

@auth
def searchconstructionlevel(request):
    levels = constructionlevel.objects.all()
    return render(request, "searchconstructionlevel.html", {'levels': levels})


@auth
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

@auth
def deleteconstructionlevel(request, id):
    level = constructionlevel.objects.get(id=id)
    try:
        level.delete()
    except:
        pass
    return redirect('/searchconstructionlevel')

#******************************************************************************************************************

@auth
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

@auth
def searchcategory(request):
    categorys = Category.objects.all()
    return render(request, "searchcategory.html", {'categorys': categorys})


@auth
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


@auth
def deletecategory(request, categoryid):
    categorys = Category.objects.get(categoryid=categoryid)
    try:
        categorys.delete()
    except:
        pass
    return redirect('/searchcategory')


# *****************************************************************************************************************


@auth
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

@auth
def searchunitmeasurement(request):
    units = unitmeasurement.objects.all()
    return render(request, "searchunit.html", {'units': units})


@auth
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


@auth
def deleteunitmeasurement(request, unitmeasurementid):
    units = unitmeasurement.objects.get(unitmeasurementid=unitmeasurementid)
    try:
        units.delete()
    except:
        pass
    return redirect('/searchunit')

# *****************************************************************************************************************
@auth
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

@auth
def searchbrand(request):
    brands = brandlist.objects.all()
    return render(request, "searchbrand.html", {'brands': brands})

@auth
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


@auth
def deletebrand(request, id):
    brands = brandlist.objects.get(id=id)
    try:
        brands.delete()
    except:
        pass
    return redirect('/searchbrand')


# ************************************************************************************************************************
@auth
def createsite(request):
    context = {}

    customer_name = approvedinquiry.objects.all()
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

@auth
def searchsite(request):
    sitess = Site.objects.all()
    return render(request, "searchsite.html", {'sitess': sitess})

@auth
def updatesite(request,id):
    sitess = Site.objects.get(id=id)
    form = siteform(
        initial={'site_name': sitess.site_name, 'customer': sitess.customer,'pincode': sitess.pincode,
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


@auth
def deletesite(request, id):
    sitess = Site.objects.get(id=id)
    try:
        sitess.delete()
    except:
        pass
    return redirect('/searchsite')


# **********************************************************************************************************************

@auth
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

@auth
def get_brands_by_material(request):
    material_id = request.GET.get('material_id')
    brands = brandlist.objects.filter(materialnames_id=material_id)
    brand_list = list(brands.values('id', 'brandname'))
    return JsonResponse(brand_list, safe=False)


@auth
def searchinternaltransfer(request):
    internals = internaltransfer.objects.all()
    return render(request, "searchinternaltransfer.html", {'internals': internals})


@auth
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


@auth
def deleteinternaltransfer(request, id):
    internals = internaltransfer.objects.get(id=id)
    try:
        internals.delete()
    except:
        pass
    return redirect('/searchinternaltransfer')

# **************************************************************************************************************************

@auth
def material_management(request):
    customers = approvedinquiry.objects.all()
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
            customer = approvedinquiry.objects.get(id=customer_id)
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

@auth
def get_site(request, customer_id):
    customer = get_object_or_404(approvedinquiry, id=customer_id)
    sites = Site.objects.filter(customer=customer)
    site_list = [{'id': site.id, 'name': site.site_name} for site in sites]
    return JsonResponse(site_list, safe=False)

@auth
def searchaddmaterial(request):
    addmates = addmaterial.objects.all()
    return render(request, "searchaddmaterial.html", {'addmates': addmates})

@auth
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


@auth
def deleteaddmaterial(request, id):
    addmates = addmaterial.objects.get(id=id)
    try:
        addmates.delete()
    except:
        pass
    return redirect('/searchaddmaterial')



# *******************************************************************************************************************

@auth
def createempregistration(request):
    if request.method == 'POST':
        form = employeeregistrationform(request.POST)
        employee_name = request.POST.get('employee_name')

        if employeeregistration.objects.filter(employee_name=employee_name).exists():
            return JsonResponse({'error': 'Employee already exists'})

        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
    else:
        form = employeeregistrationform()

    return render(request, 'createempregistration.html', {'form': form})

@auth
def generate_employeeid(request):
    name = request.GET.get('name')
    if name:
        temp_employee = employeeregistration(employee_name=name)
        employeeid = temp_employee.generate_employeeid()
        return JsonResponse({'employeeid': employeeid})
    return JsonResponse({'error': 'Invalid name'}, status=400)

@auth
def searchempregistration(request):
    emplos = employeeregistration.objects.all()
    return render(request, "searchempregistration.html", {'emplos': emplos})

@auth
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


@auth
def deleteempregistration(request, id):
    emplos = employeeregistration.objects.get(id=id)
    try:
        emplos.delete()
    except:
        pass
    return redirect('/searchempregistration')


# **************************************************************************************************************************************

# def approvedinquiry_view(request):
#     context = {}
#     form = approvedinquiryform(request.POST or None)
#     clients = Client_registration.objects.all()
#     employees = employeeregistration.objects.all()
#     work_types = constructiontype.objects.all()
#
#     if request.method == 'POST':
#         customer_id = request.POST.get('customer_name')
#         if approvedinquiry.objects.filter(customer_name_id=customer_id).exists():
#             context["duplicate_error"] = True
#         else:
#             if form.is_valid():
#                 form.save()
#                 return redirect('/search_approvedinquiry')
#
#     context["form"] = form
#     context["clients"] = clients
#     context["employees"] = employees
#     context["work_types"] = work_types
#
#     return render(request, "approvedinquiry.html", context)
#
# def get_representatives(request):
#     client_id = request.GET.get('client_id')
#     representatives = employeeregistration.objects.filter(client_registration__id=client_id)
#     client = Client_registration.objects.get(id=client_id)
#     data = {
#         "representatives": [{"id": rep.id, "name": rep.employee_name} for rep in representatives],
#         "client_details": {
#             "name": client.client_name,
#             "phone_no": client.phone_no,
#             "email": client.email,
#             "site_address": client.site_address,
#             "inquiry_date": client.inquiry_date
#         }
#     }
#     return JsonResponse(data, safe=False)

@auth
def approvedinquiry_view(request):
    context = {}
    form = approvedinquiryform(request.POST or None)

    saved_customer_ids = approvedinquiry.objects.values_list('customer_name_id', flat=True)
    clients = Client_registration.objects.exclude(id__in=saved_customer_ids)
    employees = employeeregistration.objects.all()
    work_types = constructiontype.objects.all()

    if request.method == 'POST':
        customer_id = request.POST.get('customer_name')
        if approvedinquiry.objects.filter(customer_name_id=customer_id).exists():
            context["duplicate_error"] = True
        else:
            if form.is_valid():
                form.save()
                return redirect('/search_approvedinquiry')

    context["form"] = form
    context["clients"] = clients
    context["employees"] = employees
    context["work_types"] = work_types

    return render(request, "approvedinquiry.html", context)

@auth
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

@auth
def search_approvedinquiry(request):
    inquiries = approvedinquiry.objects.all()
    return render(request, "searchapprovedinquiry.html", {'inquiries': inquiries})

@auth
def update_approvedinquiry(request, id):
    approveds = approvedinquiry.objects.get(id=id)
    form = approvedinquiryform(
        initial={'customer_name': approveds.customer_name, 'employee': approveds.employee,'plotarea': approveds.plotarea,
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


@auth
def delete_approvedinquiry(request, id):
    approveds = approvedinquiry.objects.get(id=id)
    try:
        approveds.delete()
    except:
        pass
    return redirect('/search_approvedinquiry')

# *********************************************************************************************************************************

@auth
def clientregview(request):
    context = {}
    client = clientregForm(request.POST or None)
    employee_name = employeeregistration.objects.all()

    if request.method == 'POST':
        client_name = request.POST.get('client_name')

        if Client_registration.objects.filter(client_name=client_name).exists():
            return JsonResponse({'error': 'Client already exists'})

        if client.is_valid():
            client.save()
            return JsonResponse({'success': True})
        else:
            context['form'] = client

    context["employee_name"] = employee_name
    return render(request, "client_registration.html", context)

@auth
def search_clientregs(request):
    reg = Client_registration.objects.all()
    return render(request, "search_clientreg.html", {'regs': reg})

@auth
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

@auth
def delete_clientreg(request, id):
    citys = Client_registration.objects.get(id=id)
    try:
        citys.delete()
    except:
        pass
    return redirect('/search_clientreg')

# **********************************************************************************************************************

@auth
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

@auth
def get_representativess(request):
    client_id = request.GET.get('client_id')
    representatives = employeeregistration.objects.filter(client_registration__id=client_id)
    data = [{"id": rep.id, "name": rep.employee_name} for rep in representatives]
    return JsonResponse(data, safe=False)

@auth
def search_clientinq(request):
    client = ClientInquiry.objects.all()
    return render(request, "search_clientinquiry.html", {'inq': client})

@auth
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

@auth
def delete_clientinq(request, id):
    client = ClientInquiry.objects.get(id=id)
    try:
        client.delete()
    except:
        pass
    return redirect('/search_clientinquiry')

# *********************************************************************************************************************


@auth
def labour_management_view(request):
    context = {}
    customer_name = approvedinquiry.objects.all()
    construction_types = constructiontype.objects.all()
    cemployee = employeeregistration.objects.all()

    if request.method == "POST":
        customer_id = request.POST.get('customer_id')
        site_id = request.POST.get('site_id')
        transfer_date = request.POST.get('transfer_date')
        requirement_by = request.POST.get('requirement_by')
        requirement_to_id = request.POST.get('requirement_to_id')  # Ensure we get the correct field name
        construction_data = request.POST.get('constructionData', '[]')
        construction_list = json.loads(construction_data)

        customer = get_object_or_404(approvedinquiry, id=customer_id)
        site = get_object_or_404(Site, id=site_id)
        requirement_to = get_object_or_404(employeeregistration, id=requirement_to_id)  # Fetch the employee instance

        master_data = masterlabour.objects.create(
            customer=customer,
            sites=site,
            transfer_date=transfer_date,
            requirement_by=requirement_by,
            requirement_to=requirement_to
        )

        for construction_item in construction_list:
            construction_type = get_object_or_404(constructiontype, id=construction_item['constructionTypeId'])
            quantity = construction_item['quantity']

            labourtransaction.objects.create(
                customerid=master_data,
                constructiontypes=construction_type,
                quantity=quantity
            )

        return redirect('/search_labourtransaction')

    context["customer_name"] = customer_name
    context["construction_types"] = construction_types
    context["employees"] = cemployee

    return render(request, "createlabour.html", context)
@auth
def get_sites_by_customer(request, customer_id):
    sites = Site.objects.filter(customer_id=customer_id)
    sites_data = [{"id": site.id, "name": site.site_name} for site in sites]
    return JsonResponse(sites_data, safe=False)

@auth
def search_masterlabour(request):
    client = masterlabour.objects.all()
    return render(request, "search_masterlabour.html", {'labour': client})

@auth
def search_labourtransaction(request):
    client = labourtransaction.objects.all()
    return render(request, "search_labourtransaction.html", {'labour': client})

@auth
def update_masterlabour(request, id):
    client = masterlabour.objects.get(id=id)
    form = labourmasterform(
        initial={'customer': client.customer, 'sites': client.sites, 'current_date': client.current_date, 'transfer_date': client.transfer_date, 'requirement_by': client.requirement_by, 'requirement_to': client.requirement_to})
    if request.method == "POST":
        form = labourmasterform(request.POST, instance=client)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                return redirect('/search_masterlabour')
            except Exception as e:
                pass
    return render(request, 'update_masterlabour.html', {'form': form})

@auth
def update_labourtransaction(request, id):
    client = labourtransaction.objects.get(id=id)
    form = labourtransform(
        initial={'customerid': client.customerid, 'constructiontypes': client.constructiontypes, 'quantity': client.quantity })
    if request.method == "POST":
        form = labourtransform(request.POST, instance=client)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                return redirect('/search_labourtransaction')
            except Exception as e:
                pass
    return render(request, 'update_labourtransaction.html', {'form': form})

@auth
def delete_masterlabour(request, id):
    client = masterlabour.objects.get(id=id)
    try:
        client.delete()
    except:
        pass
    return redirect('/search_masterlabour')

@auth
def delete_labourtransaction(request, id):
    client = labourtransaction.objects.get(id=id)
    try:
        client.delete()
    except:
        pass
    return redirect('/search_labourtransaction')

import json
from django.shortcuts import render
from django.contrib import messages
from .models import mastermateriallist, brandlist, unitmeasurement, subcategory


def createsubcategory(request):
    context = {}

    # Fetch data for the dropdowns
    materialname = mastermateriallist.objects.all()
    brandname = brandlist.objects.all()
    unitmeasurementname = unitmeasurement.objects.all()

    if request.method == "POST":
        # Get the JSON data from the form
        subcategory_data = request.POST.get('subcategoryData', '[]')

        try:
            # Load the JSON data
            subcategory_list = json.loads(subcategory_data)

            # Iterate over each item in the list
            for subcategory_item in subcategory_list:
                # Extract data from each item
                material_id = subcategory_item.get('materialId')
                brand_id = subcategory_item.get('brandId')
                unit_id = subcategory_item.get('unitId')
                subcategory_name = subcategory_item.get('subcategoryName')
                unit_per = subcategory_item.get('unitPer')

                # Fetch the corresponding objects from the database
                material = mastermateriallist.objects.get(materialid=material_id)
                brand = brandlist.objects.get(id=brand_id)
                unit = unitmeasurement.objects.get(unitmeasurementid=unit_id)

                # Create a new subcategory object
                subcategory.objects.create(
                    subcategorys=subcategory_name,
                    categorys=material,
                    brands=brand,
                    units=unit,
                    unitper=unit_per
                )

                return redirect('/searchsubcategory')


        except json.JSONDecodeError:
            messages.error(request, 'Failed to decode JSON data.')
        except mastermateriallist.DoesNotExist:
            messages.error(request, 'Material not found.')
        except brandlist.DoesNotExist:
            messages.error(request, 'Brand not found.')
        except unitmeasurement.DoesNotExist:
            messages.error(request, 'Unit not found.')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')

    # Add context data for rendering the form
    context["materialname"] = materialname
    context["brandname"] = brandname
    context["unitmeasurementname"] = unitmeasurementname

    return render(request, "createsubcategory.html", context)


def searchsubcategory(request):
    sub = subcategory.objects.all()
    return render(request, "searchsubcategory.html", {'sub': sub})

def updatesubcategory(request, id):
    sub = subcategory.objects.get(id=id)
    form = subcategoryform(
        initial={'subcategorys': sub.subcategorys, 'categorys': sub.categorys, 'brands': sub.brands, 'units': sub.units, 'unitper': sub.unitper })
    if request.method == "POST":
        form = subcategoryform(request.POST, instance=sub)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                return redirect('/searchsubcategory')
            except Exception as e:
                pass
    return render(request, 'updatesubcategory.html', {'form': form})


def deletesubcategory(request, id):
    sub = subcategory.objects.get(id=id)
    try:
        sub.delete()
    except:
        pass
    return redirect('/searchsubcategory')


#*****************************************************************************************************************************
@auth
def create_selectproduct(request):
    context = {}

    customers_list = approvedinquiry.objects.all()
    sites_list = Site.objects.all()
    brands_list = brandlist.objects.all()

    if request.method == "POST":
        form = selectproductform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product selection has been saved successfully!')
            return redirect('/searchselectproduct')
        else:
            print(request.POST)
            messages.error(request, 'Please correct the error below.')
    else:
        form = selectproductform()

    context["form"] = form
    context["customers_list"] = customers_list
    context["sites_list"] = sites_list
    context["brands_list"] = brands_list

    return render(request, "addproduct.html", context)

@auth
def load_sites(request):
    customer_id = request.GET.get('customer')
    sites_list = Site.objects.filter(customer_id=customer_id).distinct()
    return JsonResponse(list(sites_list.values('id', 'site_name')), safe=False)

@auth
def load_categories(request):
    brand_id = request.GET.get('brand')
    subcategories = subcategory.objects.filter(brands_id=brand_id).distinct()
    category_ids = subcategories.values_list('categorys_id', flat=True).distinct()
    categories = mastermateriallist.objects.filter(materialid__in=category_ids).distinct()
    return JsonResponse(list(categories.values('materialid', 'materialname')), safe=False)
@auth
def load_subcategories(request):
    category_id = request.GET.get('category')
    subcategories = subcategory.objects.filter(categorys_id=category_id).distinct()
    return JsonResponse(list(subcategories.values('id', 'subcategorys')), safe=False)

@auth

def load_units_and_price(request):
    subcategory_id = request.GET.get('subcategory')
    subcategory_obj = subcategory.objects.get(id=subcategory_id)
    unit = subcategory_obj.units
    print("Unit object:", unit)
    print("Unit ID:", unit.pk)  # Debugging line
    unitprice = subcategory_obj.unitper
    data = {
        'unit_id': unit.pk,
        'unit_name': unit.unitmeasurementname,
        'unitprice': unitprice
    }
    return JsonResponse(data)


@auth

def searchselectproduct(request):
    product = selectproduct.objects.all()
    return render(request, "searchselectproduct.html", {'product': product})


@auth

def updateselectproduct(request, id):
    product = selectproduct.objects.get(id=id)
    form = selectproductform(
        initial={'customer': product.customer, 'site': product.site,
                 'brand': product.brand,'category': product.category,
                 'subcategorys': product.subcategorys,'unit': product.unit,
                 'unitprice': product.unitprice,'quantity': product.quantity,
                 'totalprice': product.totalprice})
    if request.method == "POST":
        form = selectproductform(request.POST, instance=product)
        if form.is_valid():
            try:
                form.save()
                model = form.instance
                return redirect('/searchselectproduct')
            except Exception as e:
                pass
    return render(request, 'updateselectproduct.html', {'form': form})


@auth

def deleteselectproduct(request, id):
    product = selectproduct.objects.get(id=id)
    try:
        product.delete()
    except:
        pass
    return redirect('/searchselectproduct')