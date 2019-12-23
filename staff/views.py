from django.shortcuts import render,redirect
from .forms import *
from django.http import HttpResponse
import xlrd
from .models import *
from rest_framework import viewsets
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from staff.serializers import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import mixins
# from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import *
from rest_framework import generics,reverse
from .permissions import *
from django.core.mail import send_mail
from django.contrib.auth import logout,authenticate,login
from .models import *
from .extras import *
from django.contrib.auth.decorators import login_required
# Create your views here.







def upload_excel(request):
 if request.user.is_staff==True:
   if request.method == 'POST':

       userform = user_form(request.POST)
       excelform = excel_form(request.POST,request.FILES)
       if(userform.is_valid()):
           userform.save()

           return redirect('home-page')
       elif(excelform.is_valid()):
           excelform.instance.uploaded_by = request.user
           x = excelform.save()
           path = str(excelform.instance.sheet.path)
           user_profile_from_excel(path)
           return redirect('home-page')

   excelform = excel_form()
   userform = user_form()
   return render(request,'excel.html',{'form':excelform,'user_form':userform})
 return render(request,'error.html')



def get_model(name,model):
    obj = model.objects.get(name = name)
    return obj



def user_profile_from_excel(path):
     book = xlrd.open_workbook(path)
     sheet = book.sheet_by_index(0)
     row = sheet.nrows
     cols = sheet.ncols

     for i in range(1,row):

              adhaar_no= int(sheet.cell_value(i,1))
              name = sheet.cell_value(i,2)
              DOB = sheet.cell_value(i,3)
              gender = sheet.cell_value(i,4)
              city = sheet.cell_value(i,5)
              state = sheet.cell_value(i,6)

              city_model = get_model(city,City)
              state_model = get_model(state,State)
              print(DOB)
              new = str((xlrd.xldate_as_datetime(DOB,book.datemode)))[0:10]
              birth = str(DOB)

              new = user_profile.objects.create(adhaar_no=adhaar_no,name=name,DOB=new,gender= gender,city=city_model, state=state_model)
              new.save()




def load_cities(request):
    State_id = request.GET.get('state')
    # st_obj = State.objects.get(id=State_id)
    cities = City.objects.filter(state_id=State_id).order_by('name')
    # cities = City.objects.filter(state=st_obj).order_by('name')

    for city in cities:
        print(city)

    return render(request, 'city_dropdown_list_options.html', {'cities': cities})




class Dber_list(generics.ListCreateAPIView):
    queryset = user_profile.objects.all()
    serializer_class = user_profile_serializer


class Dber_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = user_profile.objects.all()
    serializer_class = user_profile_serializer
    # permission_classes = ['IsStaffOrAdmin']




@login_required(login_url='dber-logout')
def Dber_mail(request):
 if request.method == 'POST':
    form = email_form(request.POST)
    subject = request.POST.get('subject')
    content = request.POST.get('content')
    send_to = request.POST.get('send_to')
    sent_by = request.user.user_profile.email
    # sent_by = 'sunilkumar.sobha@gmail.com'
    send_mail(subject,content,sent_by,[send_to],fail_silently=False,)
    return redirect('home-page')
 form = email_form()
 return render(request,'dber_mail.html',{'form':form})




@login_required(login_url='dber-logout')
def staff_mail(request):
  if request.user.is_staff==True:
     if request.method == 'POST':
        form = staff_email_form(request.POST)
        subject = request.POST.get('subject')
        content = request.POST.get('content')
        sent_by = request.user.staff.email
        city = request.user.staff.city
        objs = user_profile.objects.filter(city = city,adhaar_linked=True)
        send_to =[]
        for x in objs:
            send_to.append(x.email)
        send_mail(subject,content,sent_by,send_to,fail_silently=False,)
        return redirect('home-page')
     form = staff_email_form()
     return render(request,'staff_mail.html',{'form':form})




def register(request):
    if request.method == 'POST':
            reg_form = register_form(request.POST)
            if reg_form.is_valid:
                adh = request.POST['Adhaar']
                ad_list =[]
                for user in user_profile.objects.all():
                    if int(user.adhaar_no) == int(adh):
                        u_name = request.POST['username']
                        passw = request.POST['password']
                        email = request.POST['email']
                        user.adhaar_linked = True
                        user.username = u_name
                        user.Password = passw
                        user.email = email

                        u_name = request.POST['username']
                        passw = request.POST['password']
                        try:
                            new = User.objects.create(username =u_name,password=passw)
                            new.save()
                            new.set_password(passw)
                            user.user = new
                            new.save()
                            user.save()
                            return redirect('dber-logout')
                        except:
                           pass      
                # print(HttpResponse("adhhar number not matched , please contact administrator"))
            # return HttpResponse("<h3>User Not Found</h3>")
            return render(request,'error.html')

    reg_form = register_form()
    return render(request,'register.html',{'r_form':reg_form})





def login_view(request):
    if request.method == 'POST':
        l_form = login_form(request.POST)
        if l_form.is_valid():
            u_name = request.POST['username']
            passw = request.POST['password']
            user = authenticate(username=u_name,password=passw)
            if user is not None:
                    if user.is_active:
                        login(request, user)
                        return redirect('home-page')
        return redirect('dber-login')
    l_form = login_form()
    return render(request,'login.html',{'l_form':l_form})




def custom_filter(name1,state1,city1,list):
    list1 = getquery_name('name',name1,list)
    list2 = getquery_state('state',state1,list1)
    list3 = getquery_city('city',city1,list2)
    return list3



@login_required(login_url='dber-logout')
def HomePage(request):
    if request.user.is_staff != True:
        klist = User.objects.all()
        list =[]
        for x in klist:
            if x.is_staff != True:
                list.append(x)

        if request.method == 'POST':
            # adhaar = request.POST.get('adhaar')
            name1 = request.POST.get('name')
            state1 = request.POST.get('state')
            city1 = request.POST.get('city')
            # query = request.POST.get('query')
            list4 = custom_filter(name1,state1,city1,list)
            return render(request,'home.html',{'list':list4})

        return render(request,'home.html',{'list':list})
    return redirect('upload_excel')





def logout_view(request):
    logout(request)
    return redirect('dber-login')



@login_required(login_url='dber-logout')
def profile_update(request):
    if request.method == 'POST':

        if request.user.is_staff==True:
            l_form = staffprofileForm(data=request.POST,instance=request.user.staff)
        else:
            l_form = profileForm(data=request.POST, instance=request.user.user_profile)
        if l_form.is_valid():
                update = l_form.save(commit=False)
                l_form.user = request.user
                l_form.save()
                user = request.user
                if user.is_active:
                            user.set_password(l_form.instance.Password)
                            user.save()
                            return redirect('dber-logout')
        return render(request,'error.html')
    print(request.user.staff.city)
    print("")
    if request.user.is_staff==True:
        print(request.user.staff.city)
        print("")
        l_form = staffprofileForm(instance=request.user.staff)
    else:
        l_form = profileForm(instance=request.user.user_profile)
    return render(request,'new_password.html',{'l_form':l_form})
