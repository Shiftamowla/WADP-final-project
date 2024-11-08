from django.shortcuts import render, redirect
from myapp.models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash
from django.db import IntegrityError
from django.db.models import Q 

# Public Content
# -----------------------------------------------------------------------------

def base(req):

    return render (req, 'base.html')

def home(req):

    total_jobs = JobModel.objects.count()
    total_applications = ApplyJobModel.objects.count()
    total_users = Custom_user.objects.count()
    
    context = {
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'total_users': total_users,
    }


    return render (req, 'home.html',context)

def jobfeed(req):
    data=JobModel.objects.all()

    context = {
        'data': data
    }
    return render(req,'jobfeed.html',context)



# search and skillmatching
# -----------------------------------------------------------------------------

def searchJob(req):
    
    query = req.GET.get('query')
    
    if query:
        
        data = JobModel.objects.filter(Q(job_title__icontains=query) 
                                       |Q(Job_Description__icontains=query) 
                                       |Q(Category__icontains=query))
    
    else:
        data = JobModel.objects.none()
        
    context={
        'data':data,
        'query':query
    }
    
    return render(req,"search.html",context)

def skillmatching(req):
    user=req.user
    myskill=user.viewersProfile.Skills

    Job=JobModel.objects.filter(Skills=myskill)
    text={
        'Job':Job,
    }
 
    return render(req,'skillmatching.html',text)



# delete and single view
# -----------------------------------------------------------------------------
login_required
def mainprofile(req,id):
    current_user=req.user

    Job=JobModel.objects.filter(id=id)
    text={
        'Job':Job,
    }
 
    return render(req,'mainprofile.html',text)

def deletejob(req,id):
    job=JobModel.objects.filter(id=id)
    job.delete()
    return redirect('Table')



# Table and Apply 
# -----------------------------------------------------------------------------
login_required
def totalTable(req):
    data=AllPost.objects.all()

    context = {
        'data': data
    }
    return render(req,'totalTable.html',context)

def totaluser(req):
    data=Custom_user.objects.all()

    context = {
        'data': data
    }
    return render(req,'alluser.html',context)


login_required
def Table(req):
    current_user = req.user
    data=JobModel.objects.filter(user=current_user)

    context = {
        'data': data
    }
    return render(req,'Table.html',context)

login_required
def appliedJob(request):
    current_user = request.user

    job_applications = ApplyJobModel.objects.filter(user=current_user)


    context = {
        "Job": job_applications,
    }
    return render(request, "applyedJob.html", context)


login_required
def ApplyNow(request,job_title,apply_id):
    jobs=JobModel.objects.get(id=apply_id)
    context={
        'jobs':jobs
    }
    
    
    if request.method=='POST':
        
        skill=request.POST.get("skill")
        Cover=request.POST.get("Cover")
        apply_Image=request.FILES.get("apply_Image")
        resume=request.FILES.get("resume")
        
        apply=ApplyJobModel(
            user=request.user,
            job=jobs,
            Skills=skill,
            Cover=Cover,
            Resume=resume,
            Apply_Image=apply_Image,
        )
        
        apply.save()
        return redirect("jobfeed")
            
    return render(request,"applyjob.html",context)






# Add and Edit
# -----------------------------------------------------------------------------
login_required
def Addjob(req):
    current_user=req.user
    AllPost.objects.create(user=current_user)

    if current_user.user_type == "recruiters":
     if req.method=='POST':
        company_logo=req.FILES.get('company_logo')
        job_title=req.POST.get('job_title')
        Number_of_opening=req.POST.get('Number_of_opening')
        Category=req.POST.get('Category')
        Job_Description=req.POST.get('Job_Description')
        Skills=req.POST.get('Skills')

        books=JobModel(
            user=current_user,
            company_logo=company_logo,
            job_title=job_title,
            Number_of_opening=Number_of_opening,
            Category=Category,
            Job_Description=Job_Description,
            Skills=Skills,
        )
        books.save()
        
        return redirect('jobfeed')
    return render(req,'addjob.html')




login_required
def editjob(req,id):
    current_user=req.user
    job=JobModel.objects.filter(id=id)

    if current_user.user_type == "recruiters":
     if req.method=='POST':
        company_logo=req.FILES.get('company_logo')
        job_title=req.POST.get('job_title')
        Number_of_opening=req.POST.get('Number_of_opening')
        Category=req.POST.get('Category')
        Job_Description=req.POST.get('Job_Description')
        Skills=req.POST.get('Skills')
        company_logo_old=req.POST.get('company_logo_old')

        user_object=Custom_user.objects.get(id=id)


        add=JobModel(
            id=id,
            user=user_object,
            job_title=job_title,
            Number_of_opening=Number_of_opening,
            Category=Category,
            Job_Description=Job_Description,
            Skills=Skills,
            )
        if company_logo:
          add.company_logo=company_logo
          add.save()
        else:
         add.company_logo=company_logo_old
         add.save()
        return redirect ('Table')

    return render (req,'editjob.html',{'job':job})


# Profile
# -----------------------------------------------------------------------------

login_required
def Profile(req):
    current_user=req.user

    cre=CreatorProfileModel.objects.filter(user=current_user)
    seekar=jobseekerProfileModel.objects.filter(user=current_user)
    text={
        'cre':cre,
        'seekar':seekar,
    }
 
    return render(req,'profile.html',text)


login_required
def updateprofile(request,id):
    user = request.user
    profile = None

    # Determine which profile to edit based on user type
    if user.user_type == 'jobseeker':
        profile = jobseekerProfileModel.objects.get(user=user)
    elif user.user_type == 'recruiters':
        profile = CreatorProfileModel.objects.get(user=user)

    if request.method == 'POST':
        # Update user details
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()

        # Update profile picture only if a new one is uploaded
        profile.Skills = request.POST.get('Skills')

        if request.FILES.get('Image'):
            profile.Image = request.FILES['Image']

        profile.save()  
        return redirect("Profile")
            


    return render (request,'updateprofile.html', {'user': user, 'profile': profile})




# Authentication
# -----------------------------------------------------------------------------


def password_change(req):
    current_user=req.user
    if req.method == 'POST':
        currentpassword = req.POST.get("currentpassword")
        newpassword = req.POST.get("newpassword")
        confirmpassword = req.POST.get("confirmpassword")

        if check_password(currentpassword,req.user.password):
            if newpassword==confirmpassword:
                current_user.set_password(newpassword)
                current_user.save()
                update_session_auth_hash(req,current_user)
                return redirect("loginpage")
            
            
            if newpassword != confirmpassword:
                return redirect('password_change')
            else:
                return render(req, "password.html")
            
    return render(req, 'password.html')


def loginpage(req):
    if req.method == 'POST':
        username = req.POST.get("username")
        password = req.POST.get("password")

        # Check if both username and password are provided
        if not username or not password:
            return render(req, "login.html")

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is not None:
            login(req, user)
            return redirect("base")
        else:
            return render(req, "login.html")

    return render(req, "login.html")


def registerpage(req):
    if req.method == 'POST':
        username = req.POST.get("username")
        email = req.POST.get("email")
        user_type = req.POST.get("usertype")
        password = req.POST.get("password")
        confirm_password = req.POST.get("confirm_password")

        # Check if passwords match
        if password != confirm_password:
            return render(req, "signupPage.html")

        # Create user
        try:
            user = Custom_user.objects.create_user(
                username=username,
                email=email,
                user_type=user_type,
                password=password,
            )
            # Create the appropriate user profile based on user_type
            if user_type == 'jobseeker':
                jobseekerProfileModel.objects.create(user=user)
            elif user_type == 'recruiters':
                CreatorProfileModel.objects.create(user=user)

            return redirect("loginpage")
        except IntegrityError:
            return render(req, "signupPage.html")

    return render(req, "signupPage.html")

def logoutpage(req):
    logout(req)
    return redirect('loginpage')