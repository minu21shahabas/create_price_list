
import os
from django.http import JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.text import capfirst
from django.contrib.auth.models import User, auth
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


def index(request):

    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':

        first_name = capfirst(request.POST['fname'])
        last_name = capfirst(request.POST['lname'])
        username = request.POST['uname']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        email = request.POST['email1']
        phone = request.POST['phone']

        if password == cpassword:  # password matching......
            # check Username Already Exists..
            if User.objects.filter(username=username).exists():
                messages.info(request, 'This username already exists!!!!!!')
                return redirect('register')
            else:
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    password=password,
                    email=email)

                user.save()
                u = User.objects.get(id=user.id)

                company_details(contact_number=phone, user=u).save()

        else:
            messages.info(request, 'Password doesnt match!!!!!!!')
            print("Password is not Matching.. ")
            return redirect('register')
        return redirect('register')

    return render(request, 'register.html')


def login(request):

    if request.method == 'POST':

        email_or_username = request.POST['emailorusername']
        password = request.POST['password']

        user = authenticate(
            request, username=email_or_username, password=password)
        print(user)
        if user is not None:
            auth.login(request, user)
            return redirect('base')
        else:
            return redirect('/')

    return render(request, 'register.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required(login_url='login')
def base(request):

    company = company_details.objects.get(user=request.user)
    context = {
        'company': company
    }
    return render(request, 'base.html', context)


@login_required(login_url='login')
def view_profile(request):

    company = company_details.objects.get(user=request.user)
    context = {
        'company': company
    }
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def edit_profile(request, pk):

    company = company_details.objects.get(id=pk)
    user1 = User.objects.get(id=company.user_id)

    if request.method == "POST":

        user1.first_name = capfirst(request.POST.get('f_name'))
        user1.last_name = capfirst(request.POST.get('l_name'))
        user1.username = request.POST.get('uname')
        # pat.age = request.POST.get('age')
        # pat.address = capfirst(request.POST.get('address'))
        # pat.gender = request.POST.get('gender')
        # user1.email = request.POST.get('email')
        # pat.email = request.POST.get('email')
        # pat.contact_num = request.POST.get('cnum')
        # #fkey1= request.POST.get('doc')
        # #pat.doctor = doctor.objects.get(id = fkey1)
        # if len(request.FILES)!=0 :
        #     doc.profile_pic = request.FILES.get('file')

        company.save()
        user1.save()
        return redirect('view_profile')

    context = {
        'company': company,
        'user1': user1,
    }
    context = {
        'company': company,
    }
    return render(request, 'edit_profile.html', context)


def itemview(request):
    viewitem = AddItem.objects.all()
    return render(request, 'item_view.html', {'view': viewitem})


def additem(request):
    unit = Unit.objects.all()
    sale = Sales.objects.all()
    purchase = Purchase.objects.all()
    sal = Sales.objects.filter(Account_type='SALE')
    inc = Sales.objects.filter(Account_type='INCOME')
    cred = Sales.objects.filter(Account_type='CREDIT')
    purch = Purchase.objects.filter(Account_type='COST OF GOODS')
    exp = Purchase.objects.filter(Account_type='EXPENSE')

    return render(request, 'additem.html', {'unit': unit, 'sale': sale, 'purchase': purchase, "sal": sal, "inc": inc, "cred": cred,"purch": purch, "exp": exp,
                                            })


def add_account(request):
    if request.method == 'POST':
        Account_type = request.POST['acc_type']
        Account_name = request.POST['acc_name']
        Acount_code = request.POST['acc_code']
        Account_desc = request.POST['acc_desc']
        if Purchase.objects.filter(Account_type=Account_type).exists():
            acc = Purchase(Account_type=Account_type, Account_name=Account_name,
                           Acount_code=Acount_code, Account_desc=Account_desc)
            acc.save()
            return redirect('additem')
        else:
            messages.info(request, "You cant create new account")
            return redirect("additem")

    return render(request, 'additem.html')


def add(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            type = request.POST.get('type')
            name = request.POST['name']
            unit = request.POST['unit']
            sel_price = request.POST.get('sel_price')
            sel_acc = request.POST.get('sel_acc')
            s_desc = request.POST.get('sel_desc')
            cost_price = request.POST.get('cost_price')
            cost_acc = request.POST.get('cost_acc')
            p_desc = request.POST.get('cost_desc')
            u = request.user.id
            us = request.user
            history = "Created by" + str(us)
            user = User.objects.get(id=u)
            unit = Unit.objects.get(id=unit)
            sel = Sales.objects.get(id=sel_acc)
            cost = Purchase.objects.get(id=cost_acc)
            ad_item = AddItem(type=type, Name=name, p_desc=p_desc, s_desc=s_desc, s_price=sel_price, p_price=cost_price, unit=unit,
                              sales=sel, purchase=cost, user=user, creat=history
                              )
            ad_item.save()

            return redirect("itemview")
    return render(request, 'additem.html')


def edititem(request, id):
    pedit = AddItem.objects.get(id=id)
    p = Purchase.objects.all()
    s = Sales.objects.all()
    u = Unit.objects.all()
    return render(request, 'edititem.html', {'e': pedit, 'p': p, 's': s, 'u': u})


def edit_db(request, id):
    if request.method == 'POST':
        edit = AddItem.objects.get(id=id)
        edit.type = request.POST.get('type')
        edit.Name = request.POST['name']
        unit = request.POST['unit']
        edit.sel_price = request.POST['sel_price']
        sel_acc = request.POST['sel_acc']
        edit.s_desc = request.POST['sel_desc']
        edit.cost_price = request.POST['cost_price']
        cost_acc = request.POST['cost_acc']
        edit.p_desc = request.POST['cost_desc']

        edit.unit = Unit.objects.get(id=unit)
        edit.sel = Sales.objects.get(id=sel_acc)
        edit.cost = Purchase.objects.get(id=cost_acc)
        edit.save()
        return redirect('itemview')

    return render(request, 'edititem.html')


def detail(request, id):
    user_id = request.user
    items = AddItem.objects.all()
    product = AddItem.objects.get(id=id)
    history = History.objects.filter(p_id=product.id)
    print(product.id)

    context = {
        "allproduct": items,
        "product": product,
        "history": history,

    }

    return render(request, 'demo.html', context)


def Action(request, id):
    user = request.user.id
    user = User.objects.get(id=user)
    viewitem = AddItem.objects.all()
    event = AddItem.objects.get(id=id)

    print(user)
    if request.method == 'POST':
        action = request.POST['action']
        event.satus = action
        event.save()
        if action == 'active':
            History(user=user.username,
                    message="Item marked as Active ", p=event).save()
        else:
            History(user=user, message="Item marked as inActive", p=event).save()
    return render(request, 'item_view.html', {'view': viewitem})


def cleer(request, id):
    dl = AddItem.objects.get(id=id)
    dl.delete()
    return redirect('itemview')





def add_sales(request):
    if request.method == 'POST':
        Account_type = request.POST['acc_type']
        Account_name = request.POST['acc_name']
        Acount_code = request.POST['acc_code']
        Account_desc = request.POST['acc_desc']

        if Sales.objects.filter(Account_type=Account_type).exists():
            acc = Sales(Account_type=Account_type, Account_name=Account_name,
                        Acount_code=Acount_code, Account_desc=Account_desc)
            acc.save()
            return redirect('additem')
        else:
            messages.info(request, "You cant create new account")
            return redirect("additem")
    return render(request, 'additem.html')

# --------------------estimates-------------------------------------------------------------------------------------------------------------------


def allestimates(request):
    user = request.user
    estimates = Estimates.objects.filter(user=user).order_by('-id')
    company = company_details.objects.get(user=user)
    context = {
        'estimates': estimates,
        'company': company,
    }
    # for i in estimates:
    #     print(i)

    return render(request, 'all_estimates.html', context)





def newestimate(request):
    user = request.user
    # print(user_id)
    company = company_details.objects.get(user=user)
    items = AddItem.objects.filter(user_id=user.id)
    customers = customer.objects.filter(user_id=user.id)
    estimates_count = Estimates.objects.count()
    next_count = estimates_count+1
    context = {'company': company,
               'items': items,
               'customers': customers,
               'count': next_count,
               }

    return render(request, 'new_estimate.html', context)


def itemdata_est(request):
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)
    company = company_details.objects.get(user=user)
    # print(company.state)
    id = request.GET.get('id')
    cust = request.GET.get('cust')
    # print(id)
    # print(cust)

    item = AddItem.objects.get(Name=id, user=user)
    print(item)
    rate = item.p_price
    place = company.state
    gst = item.intrastate
    igst = item.interstate
    place_of_supply = customer.objects.get(
        customerName=cust, user=user).placeofsupply
    return JsonResponse({"status": " not", 'place': place, 'rate': rate, 'pos': place_of_supply, 'gst': gst, 'igst': igst})
    return redirect('/')
    

def createestimate(request):
    print('hhi1')
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)
    print('hhi2')
    if request.method == "POST":
        print('hhi3')
        cust_name = request.POST['customer_name']
        est_number = request.POST['estimate_number']
        reference = request.POST['reference']
        est_date = request.POST['estimate_date']
        exp_date = request.POST['expiry_date']

        item = request.POST.getlist('item[]')
        quantity = request.POST.getlist('quantity[]')
        rate = request.POST.getlist('rate[]')
        discount = request.POST.getlist('discount[]')
        tax = request.POST.getlist('tax[]')
        amount = request.POST.getlist('amount[]')
        # print(item)
        # print(quantity)
        # print(rate)
        # print(discount)
        # print(tax)
        # print(amount)

        cust_note = request.POST['customer_note']
        sub_total = request.POST['subtotal']
        igst = request.POST['igst']
        sgst = request.POST['sgst']
        cgst = request.POST['cgst']
        tax_amnt = request.POST['total_taxamount']
        shipping = request.POST['shipping_charge']
        adjustment = request.POST['adjustment_charge']
        total = request.POST['total']
        tearms_conditions = request.POST['tearms_conditions']
        attachment = request.FILES.get('file')
        status = 'Draft'

        estimate = Estimates(user=user, customer_name=cust_name, estimate_no=est_number, reference=reference, estimate_date=est_date, 
                             expiry_date=exp_date, sub_total=sub_total,igst=igst,sgst=sgst,cgst=cgst,tax_amount=tax_amnt, shipping_charge=shipping,
                             adjustment=adjustment, total=total, status=status, customer_notes=cust_note, terms_conditions=tearms_conditions, 
                             attachment=attachment)
        estimate.save()

        if len(item) == len(quantity) == len(rate) == len(discount) == len(tax) == len(amount):
            mapped = zip(item, quantity, rate, discount, tax, amount)
            mapped = list(mapped)
            for element in mapped:
                created = EstimateItems.objects.get_or_create(
                    estimate=estimate, item_name=element[0], quantity=element[1], rate=element[2], discount=element[3], tax_percentage=element[4], amount=element[5])
    return redirect('newestimate')

# def createestimate(request):

#     cur_user = request.user
#     user = User.objects.get(id=cur_user.id)
#     print('hi1')
#     if request.method == 'POST':
#         cust_name = request.POST['customer_name']
#         est_number = request.POST['estimate_number']
#         reference = request.POST['reference']
#         est_date = request.POST['estimate_date']
#         exp_date = request.POST['expiry_date']

#         item = request.POST.getlist('item[]')
#         quantity1 = request.POST.getlist('quantity[]')
#         quantity = [float(x) for x in quantity1]
#         rate1 = request.POST.getlist('rate[]')
#         rate = [float(x) for x in rate1]
#         discount1 = request.POST.getlist('discount[]')
#         discount = [float(x) for x in discount1]
#         tax1 = request.POST.getlist('tax[]')
#         tax = [float(x) for x in tax1]
#         amount1 = request.POST.getlist('amount[]')
#         amount = [float(x) for x in amount1]
#         # print(item)
#         # print(quantity)
#         # print(rate)
#         # print(discount)
#         # print(tax)
#         # print(amount)

#         cust_note = request.POST['customer_note']
#         sub_total = float(request.POST['subtotal'])
#         igst = float(request.POST['igst'])
#         sgst = float(request.POST['sgst'])
#         cgst = float(request.POST['cgst'])
#         tax_amnt = float(request.POST['total_taxamount'])
#         shipping = float(request.POST['shipping_charge'])
#         adjustment = float(request.POST['adjustment_charge'])
#         total = float(request.POST['total'])
#         tearms_conditions = request.POST['tearms_conditions']
#         attachment = request.FILES.get('file')
#         status = 'Draft'

#         estimate = Estimates(user=user, customer_name=cust_name, estimate_no=est_number, reference=reference, estimate_date=est_date, 
#                              expiry_date=exp_date, sub_total=sub_total,igst=igst,sgst=sgst,cgst=cgst,tax_amount=tax_amnt, shipping_charge=shipping,
#                              adjustment=adjustment, total=total, status=status, customer_notes=cust_note, terms_conditions=tearms_conditions, 
#                              attachment=attachment)
#         estimate.save()

#         if len(item) == len(quantity) == len(rate) == len(discount) == len(tax) == len(amount):
#             mapped = zip(item, quantity, rate, discount, tax, amount)
#             mapped = list(mapped)
#             for element in mapped:
#                 created = EstimateItems.objects.get_or_create(
#                     estimate=estimate, item_name=element[0], quantity=element[1], rate=element[2], discount=element[3], tax_percentage=element[4], amount=element[5])
#     return redirect('newestimate')


def create_and_send_estimate(request):
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)
    print("hello")
    if request.method == 'POST':
        cust_name = request.POST['customer_name']
        est_number = request.POST['estimate_number']
        reference = request.POST['reference']
        est_date = request.POST['estimate_date']
        exp_date = request.POST['expiry_date']

        item = request.POST.getlist('item[]')
        quantity1 = request.POST.getlist('quantity[]')
        quantity = [float(x) for x in quantity1]
        rate1 = request.POST.getlist('rate[]')
        rate = [float(x) for x in rate1]
        discount1 = request.POST.getlist('discount[]')
        discount = [float(x) for x in discount1]
        tax1 = request.POST.getlist('tax[]')
        tax = [float(x) for x in tax1]
        amount1 = request.POST.getlist('amount[]')
        amount = [float(x) for x in amount1]
        # print(item)
        # print(quantity)
        # print(rate)
        # print(discount)
        # print(tax)
        # print(amount)

        cust_note = request.POST['customer_note']
        sub_total = float(request.POST['subtotal'])
        igst = float(request.POST['igst'])
        sgst = float(request.POST['sgst'])
        cgst = float(request.POST['cgst'])
        tax_amnt = float(request.POST['total_taxamount'])
        shipping = float(request.POST['shipping_charge'])
        adjustment = float(request.POST['adjustment_charge'])
        total = float(request.POST['total'])
        tearms_conditions = request.POST['tearms_conditions']
        attachment = request.FILES.get('file')
        status = 'Sent'
        tot_in_string = str(total)

        estimate = Estimates(user=user, customer_name=cust_name, estimate_no=est_number, reference=reference, estimate_date=est_date, 
                             expiry_date=exp_date, sub_total=sub_total,igst=igst,sgst=sgst,cgst=cgst,tax_amount=tax_amnt, shipping_charge=shipping,
                             adjustment=adjustment, total=total, status=status, customer_notes=cust_note, terms_conditions=tearms_conditions, 
                             attachment=attachment)
        estimate.save()

        if len(item) == len(quantity) == len(rate) == len(discount) == len(tax) == len(amount):
            mapped = zip(item, quantity, rate, discount, tax, amount)
            mapped = list(mapped)
            for element in mapped:
                created = EstimateItems.objects.get_or_create(
                    estimate=estimate, item_name=element[0], quantity=element[1], rate=element[2], discount=element[3], tax_percentage=element[4], amount=element[5])

        cust_email = customer.objects.get(
            user=user, customerName=cust_name).customerEmail
        print(cust_email)
        subject = 'Estimate'
        message = 'Dear Customer,\n Your Estimate has been Saved for a total amount of: ' + tot_in_string
        recipient = cust_email
        send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient])

    return redirect('newestimate')

def estimateslip(request, est_id):
    user = request.user
    company = company_details.objects.get(user=user)
    all_estimates = Estimates.objects.filter(user=user)
    estimate = Estimates.objects.get(id=est_id)
    items = EstimateItems.objects.filter(estimate=estimate)
    context = {
        'company': company,
        'all_estimates':all_estimates,
        'estimate': estimate,
        'items': items,
    }
    return render(request, 'estimate_slip.html', context)




def editestimate(request,est_id):
    user = request.user
    company = company_details.objects.get(user=user)
    customers = customer.objects.filter(user_id=user.id)
    items = AddItem.objects.filter(user_id=user.id)
    estimate = Estimates.objects.get(id=est_id)
    est_items = EstimateItems.objects.filter(estimate=estimate)
    context = {
        'company': company,
        'estimate': estimate,
        'customers': customers,
        'items': items,
        'est_items': est_items,
    }
    return render(request, 'edit_estimate.html', context)

def updateestimate(request,pk):
    cur_user = request.user
    user = User.objects.get(id=cur_user.id)

    if request.method == 'POST':
        estimate = Estimates.objects.get(id=pk)
        estimate.user = user
        estimate.customer_name = request.POST['customer_name']
        estimate.estimate_no = request.POST['estimate_number']
        estimate.reference = request.POST['reference']
        estimate.estimate_date = request.POST['estimate_date']
        estimate.expiry_date = request.POST['expiry_date']

        estimate.customer_notes = request.POST['customer_note']
        estimate.sub_total = float(request.POST['subtotal'])
        estimate.tax_amount = float(request.POST['total_taxamount'])
        estimate.shipping_charge = float(request.POST['shipping_charge'])
        estimate.adjustment = float(request.POST['adjustment_charge'])
        estimate.total = float(request.POST['total'])
        estimate.terms_conditions = request.POST['tearms_conditions']
        estimate.status = 'Draft'

        old=estimate.attachment
        new=request.FILES.get('file')
        if old != None and new == None:
            estimate.attachment = old
        else:
            estimate.attachment = new

        estimate.save()

        item = request.POST.getlist('item[]')
        quantity1 = request.POST.getlist('quantity[]')
        quantity = [float(x) for x in quantity1]
        rate1 = request.POST.getlist('rate[]')
        rate = [float(x) for x in rate1]
        discount1 = request.POST.getlist('discount[]')
        discount = [float(x) for x in discount1]
        tax1 = request.POST.getlist('tax[]')
        tax = [float(x) for x in tax1]
        amount1 = request.POST.getlist('amount[]')
        amount = [float(x) for x in amount1]
        # print(item)
        # print(quantity)
        # print(rate)
        # print(discount)
        # print(tax)
        # print(amount)

        objects_to_delete = EstimateItems.objects.filter(estimate_id=estimate.id)
        objects_to_delete.delete()

        
        if len(item) == len(quantity) == len(rate) == len(discount) == len(tax) == len(amount):
            mapped = zip(item, quantity, rate, discount, tax, amount)
            mapped = list(mapped)
            for element in mapped:
                created = EstimateItems.objects.get_or_create(
                    estimate=estimate, item_name=element[0], quantity=element[1], rate=element[2], discount=element[3], tax_percentage=element[4], amount=element[5])
    return redirect('allestimates')

def converttoinvoice(request,est_id):
    user = request.user
    company = company_details.objects.get(user=user)
    estimate = Estimates.objects.get(id=est_id)
    items = EstimateItems.objects.filter(estimate=estimate)
    cust = customer.objects.get(customerName=estimate.customer_name,user=user)
    invoice_count = invoice.objects.count()
    next_no = invoice_count+1 
    inv = invoice(customer=cust,invoice_no=next_no,terms=1,order_no=estimate.estimate_no,
                      inv_date=estimate.estimate_date,due_date=estimate.expiry_date,igst=estimate.igst,cgst=estimate.cgst,
                      sgst=estimate.sgst,t_tax=estimate.tax_amount,subtotal=estimate.sub_total,grandtotal=estimate.total,
                      cxnote=estimate.customer_notes,file=estimate.attachment,terms_condition=estimate.terms_conditions,
                      status=estimate.status)
    inv.save()
    inv = invoice.objects.get(invoice_no=next_no,customer=cust)
    for item in items:
        items = invoice_item(product=item.item_name,quantity=item.quantity,hsn='null',tax=item.tax_percentage,
                             total=item.amount,desc=item.discount,rate=item.rate,inv=inv)
        items.save()
    return redirect('allestimates')




from django.core.mail import EmailMessage
from django.views import View
from django.conf import settings
from .forms import EmailForm

class EmailAttachementView(View):
    form_class = EmailForm
    template_name = 'newmail.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'email_form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            files = request.FILES.getlist('attach')

            try:
                mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])
                for f in files:
                    mail.attach(f.name, f.read(), f.content_type)
                mail.send()
                return render(request, self.template_name, {'email_form': form, 'error_message': 'Sent email to %s'%email})
            except:
                return render(request, self.template_name, {'email_form': form, 'error_message': 'Either the attachment is too big or corrupt'})

        return render(request, self.template_name, {'email_form': form, 'error_message': 'Unable to send email. Please try again later'})

def add_customer_for_estimate(request):
    sb=payment_terms.objects.all()
    return render(request,'customer_est.html',{'sb':sb})
def entr_custmr_for_estimate(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            type=request.POST.get('type')
            txtFullName=request.POST['txtFullName']
            cpname=request.POST['cpname']
           
            email=request.POST.get('myEmail')
            wphone=request.POST.get('wphone')
            mobile=request.POST.get('mobile')
            skname=request.POST.get('skname')
            desg=request.POST.get('desg')      
            dept=request.POST.get('dept')
            wbsite=request.POST.get('wbsite')

            gstt=request.POST.get('gstt')
            posply=request.POST.get('posply')
            tax1=request.POST.get('tax1')
            crncy=request.POST.get('crncy')
            obal=request.POST.get('obal')

            select=request.POST.get('pterms')
            pterms=payment_terms.objects.get(id=select)
            pterms=request.POST.get('pterms')

            plst=request.POST.get('plst')
            plang=request.POST.get('plang')
            fbk=request.POST.get('fbk')
            twtr=request.POST.get('twtr')
        
            atn=request.POST.get('atn')
            ctry=request.POST.get('ctry')
            
            addrs=request.POST.get('addrs')
            addrs1=request.POST.get('addrs1')
            bct=request.POST.get('bct')
            bst=request.POST.get('bst')
            bzip=request.POST.get('bzip')
            bpon=request.POST.get('bpon')
            bfx=request.POST.get('bfx')

            sal=request.POST.get('sal')
            ftname=request.POST.get('ftname')
            ltname=request.POST.get('ltname')
            mail=request.POST.get('mail')
            bworkpn=request.POST.get('bworkpn')
            bmobile=request.POST.get('bmobile')

            bskype=request.POST.get('bskype')
            bdesg=request.POST.get('bdesg')
            bdept=request.POST.get('bdept')
            u = User.objects.get(id = request.user.id)

          
            ctmr=customer(customerName=txtFullName,customerType=type,
                        companyName=cpname,customerEmail=email,customerWorkPhone=wphone,
                         customerMobile=mobile,skype=skname,designation=desg,department=dept,
                           website=wbsite,GSTTreatment=gstt,placeofsupply=posply, Taxpreference=tax1,
                             currency=crncy,OpeningBalance=obal,PaymentTerms=pterms,
                                PriceList=plst,PortalLanguage=plang,Facebook=fbk,Twitter=twtr,
                                 Attention=atn,country=ctry,Address1=addrs,Address2=addrs1,
                                  city=bct,state=bst,zipcode=bzip,phone1=bpon,
                                   fax=bfx,CPsalutation=sal,Firstname=ftname,
                                    Lastname=ltname,CPemail=mail,CPphone=bworkpn,
                                    CPmobile= bmobile,CPskype=bskype,CPdesignation=bdesg,
                                     CPdepartment=bdept,user=u )
            ctmr.save()  
            
            return redirect("newestimate")
        return redirect("newestimate")
    
def payment_term_for_estimate(request):
    if request.method=='POST':
        term=request.POST.get('term')
        day=request.POST.get('day')
        ptr=payment_terms(Terms=term,Days=day)
        ptr.save()
        return redirect("add_customer_for_estimate")
    
def deleteestimate(request,est_id):
    user = request.user
    company = company_details.objects.get(user=user)
    estimate = Estimates.objects.get(id=est_id)
    items = EstimateItems.objects.filter(estimate=estimate)
    items.delete()
    estimate.delete()
    return redirect('allestimates')

def minu(request):
     return render(request, 'new_estimate1.html')
def action1(request):
    print('hi')
    return redirect('minu')

@login_required(login_url='login')
def additem_page_est(request):
    unit=Unit.objects.all()
    sale=Sales.objects.all()
    purchase=Purchase.objects.all()
    accounts = Purchase.objects.all()
    account_types = set(Purchase.objects.values_list('Account_type', flat=True))

    
    account = Sales.objects.all()
    account_type = set(Sales.objects.values_list('Account_type', flat=True))
    
    

    return render(request,'additem_est.html',{'unit':unit,'sale':sale,'purchase':purchase,
               
                            "account":account,"account_type":account_type,"accounts":accounts,"account_types":account_types,
                            
                            })

def additem_est(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            radio=request.POST.get('radio')
            if radio=='tax':
    
                
                inter=request.POST['inter']
                intra=request.POST['intra']
                type=request.POST.get('type')
                name=request.POST['name']
                unit=request.POST['unit']
                sel_price=request.POST.get('sel_price')
                sel_acc=request.POST.get('sel_acc')
                s_desc=request.POST.get('sel_desc')
                cost_price=request.POST.get('cost_price')
                cost_acc=request.POST.get('cost_acc')      
                p_desc=request.POST.get('cost_desc')
                u=request.user.id
                us=request.user
                history="Created by" + str(us)
                user=User.objects.get(id=u)
                unit=Unit.objects.get(id=unit)
                sel=Sales.objects.get(id=sel_acc)
                cost=Purchase.objects.get(id=cost_acc)
                ad_item=AddItem(type=type,Name=name,p_desc=p_desc,s_desc=s_desc,s_price=sel_price,p_price=cost_price,unit=unit,
                            sales=sel,purchase=cost,user=user,creat=history,interstate=inter,intrastate=intra
                                )
                
            else:
                                                  
                type=request.POST.get('type')
                name=request.POST['name']
                unit=request.POST['unit']
                sel_price=request.POST.get('sel_price')
                sel_acc=request.POST.get('sel_acc')
                s_desc=request.POST.get('sel_desc')
                cost_price=request.POST.get('cost_price')
                cost_acc=request.POST.get('cost_acc')      
                p_desc=request.POST.get('cost_desc')
                u=request.user.id
                us=request.user
                history="Created by" + str(us)
                user=User.objects.get(id=u)
                unit=Unit.objects.get(id=unit)
                sel=Sales.objects.get(id=sel_acc)
                cost=Purchase.objects.get(id=cost_acc)
                ad_item=AddItem(type=type,Name=name,p_desc=p_desc,s_desc=s_desc,s_price=sel_price,p_price=cost_price,unit=unit,
                            sales=sel,purchase=cost,user=user,creat=history,interstate='none',intrastate='none'
                                )
                ad_item.save()
            ad_item.save()
           
            return redirect("newestimate")
    return render(request,'additem_est.html')

@login_required(login_url='login')
def add_unit_est(request):
    if request.method=='POST':
        unit_name=request.POST['unit_name']
        Unit(unit=unit_name).save()
        return redirect('additem_est')
    return redirect("additem_est")


@login_required(login_url='login')
def add_sales_est(request):
    if request.method=='POST':
        Account_type  =request.POST['acc_type']
        Account_name =request.POST['acc_name']
        Acount_code =request.POST['acc_code']
        Account_desc =request.POST['acc_desc']        
        acc=Sales(Account_type=Account_type,Account_name=Account_name,Acount_code=Acount_code,Account_desc=Account_desc)
        acc.save()
        return redirect('additem_est')
    return redirect("additem_est")

@login_required(login_url='login')
def add_account_est(request):
    if request.method=='POST':
        Account_type  =request.POST['acc_type']
        Account_name =request.POST['acc_name']
        Acount_code =request.POST['acc_code']
        Account_desc =request.POST['acc_desc']
       
        acc=Purchase(Account_type=Account_type,Account_name=Account_name,Acount_code=Acount_code,Account_desc=Account_desc)
        acc.save()                 
        return redirect("additem_est")
        
    return redirect("additem_est")



def addprice(request):
    add=AddItem.objects.all()
    return render(request,'addprice_list.html',{'add':add})
def addpl(request):
    print('hi')
    if request.method == "POST":
        radio = request.POST.get('rate', None)
        print(radio)

        
        name = request.POST.get('name')
        print(name)
        types = request.POST.get('type')
        print(types)
        desc = request.POST.get('desc')
        cur = request.POST.get('currency')
        print(cur)
        mark = request.POST.get('mark')
        print(mark)
        perc = request.POST.get('per')
        print(perc)
        rounds = request.POST.get('round')
        print(rounds)
        u = request.user.id
        user = User.objects.get(id=u)
            
        ad_item = Pricelist(
                name=name,
                types=types,
                currency=cur,
                description=desc,
                mark=mark,
                percentage=perc,
                roundoff=rounds,
                user=user,
            )
            
        ad_item.save()
        item_name = request.POST.getlist('iname[]') 
        print(item_name)
        price = request.POST.getlist('iprice[]')
        rate = request.POST.getlist('custom[]') 
        if len(item_name) == len(price) == len(rate):
            mapped2 = zip(item_name, price, rate)
            mapped2 = list(mapped2)
         
            for ele in mapped2:
                created = Sample_table.objects.get_or_create(item_name=ele[0], price=ele[1], cust_rate=ele[2], pl=ad_item)

        return redirect("viewpricelist")
    else:
        # Handle the case when the request method is not POST
        return render(request, 'addprice_list.html')
    # return render(request, 'addprice_list.html')
def createpl(request):
    return render(request,'addprice_list.html')
def active_status(request, id):
    user = request.user.id
    user = User.objects.get(id=user)
    viewitem = Pricelist.objects.all()
    event = Pricelist.objects.get(id=id)
    
    if request.method == 'POST':
        action = request.POST['action']
        event.status = action  # Updated field name to 'status'
        event.save()
    
    return render(request, 'view_price_list.html', {'view': viewitem})

def viewpricelist(request):
    view=Pricelist.objects.all()                                                                                                                                                                                                                                                                                                                        
    return render(request,'view_price_list.html',{'view':view})
def viewlist(request,id):
    user_id=request.user
    items=Pricelist.objects.all()
    product=Pricelist.objects.get(id=id)
    print(product.id)
    
    
    context={
       "allproduct":items,
       "product":product,
      
    }
    
    return render(request,'list.html',context)

def editlist(request,id):
    editpl=Pricelist.objects.get(id=id)
    return render(request,'edit_pricelist.html',{'editpl':editpl})
def editpage(request,id):
    if request.method=='POST':
        edit=Pricelist.objects.get(id=id)
        edit.name=request.POST['name']
        edit.description=request.POST['desc']
        edit.mark=request.POST['mark']
        edit.percentage=request.POST['per']
        edit.roundoff=request.POST['round']
        edit.save()
        return redirect('viewpricelist')
def delete_item(request,id):
    dl=Pricelist.objects.get(id=id)
    dl.delete()
    return redirect('viewpricelist')








    



