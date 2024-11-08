from django.db import models
from django.contrib.auth.models import AbstractUser

class Custom_user(AbstractUser):
    USER=[
        ('recruiters','Recruiters'),
        ('jobseeker','Jobseeker')
    ]

    user_type=models.CharField(choices=USER,max_length=100,null=True)
    Display_name=models.CharField(max_length=100,null=True)

    def  __str__(self):
        return f"{self.username}-{self.Display_name}-{self.user_type}"
    
class jobseekerProfileModel(models.Model):
    skills=[
        ('programing', 'Programing'),
        ('graphics_design', 'Graphics Design'),
        ('resarch', 'Resarch'),
    ]
    user=models.OneToOneField(Custom_user,on_delete=models.CASCADE,related_name='viewersProfile', null=True)
    Skills = models.CharField(choices=skills,max_length=255, null=True)
    Image=models.ImageField(upload_to='Media/Blog_Pic',null=True)
    
    def __str__(self):
        return f"{self.user.username}"   
    
class CreatorProfileModel(models.Model):
    user = models.OneToOneField(Custom_user, on_delete=models.CASCADE,related_name='creatorProfile')
    Image=models.ImageField(upload_to='Media/Blog_Pic',null=True)
    
    def __str__(self):
        return f"{self.user.username}"
    
class JobModel(models.Model):
    JOB_TYPE_CHOICES = [
        ('fulltime', 'Full-time'),
        ('parttime', 'Part-time'),
    ]
    skills=[
        ('programing', 'Programing'),
        ('graphics_design', 'Graphics Design'),
        ('resarch', 'Resarch'),
    ]


    user = models.ForeignKey(Custom_user, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255, null=True)
    Number_of_opening = models.PositiveIntegerField(null=True)
    Category = models.CharField(choices=JOB_TYPE_CHOICES,max_length=255, null=True)
    Job_Description = models.TextField(max_length=255, null=True)
    Skills = models.CharField(choices=skills,max_length=255, null=True)
    company_logo=models.ImageField(upload_to='Media/Blog_Pic',null=True)

    def __str__(self):
        return f"{self.user} at {self.job_title}"
    
class ApplyJobModel(models.Model):
    skills=[
        ('programing', 'Programing'),
        ('graphics_design', 'Graphics Design'),
        ('resarch', 'Resarch'),
    ]

    user=models.ForeignKey(Custom_user,on_delete=models.CASCADE,null=True)
    job=models.ForeignKey(JobModel,on_delete=models.CASCADE,null=True)
    Resume = models.FileField(upload_to="Media/Resume",max_length=200, null=True, blank=True) 
    Cover = models.TextField(null=True, blank=True) 
    Skills = models.CharField(choices=skills,max_length=255, null=True) 
    Apply_Image=models.ImageField(upload_to='Media/Job_Image',null=True)
 
    def __str__(self):
        return f"{self.user} at {self.job.job_title}"
    


class AllPost(models.Model):
    user = models.ForeignKey(Custom_user, on_delete=models.CASCADE,null=True)
    job=models.ForeignKey(JobModel,on_delete=models.CASCADE,null=True)


    def __str__(self):
        return  f"{self.user} at {self.job}"