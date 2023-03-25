
from django.core.mail import send_mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,HttpResponse,redirect,reverse
from .models import Lead,Agent
from .forms import LeadForm,LeadModelForm,CustomUserCreationForm
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView


# Create your views here.
#CRUD -create,retrieve,update,and Delete


class SignupView(LoginRequiredMixin,CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self) -> str:
        return reverse("login")
class LandingPageView(TemplateView):
    template_name = "landing.html"

class LeadListView(LoginRequiredMixin,ListView):
    template_name = "leads/lead_list.html"
    queryset = Lead.objects.all()
    context_object_name = "leads"
class LeadDetailView(LoginRequiredMixin,DetailView):
    template_name = 'leads/lead_details.html'
    queryset  = Lead.objects.all()
    context_object_name = 'lead'


class LeadCreateView(LoginRequiredMixin,CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm
    def get_success_url(self) -> str:
        return reverse("leads:lead-list")

    def form_valid(self,form):
        #todo send emails
        send_mail(
            subject="A lead has been created",
                message="Go to the site to see the new lead",
                from_email="test@test.com",
                recipient_list=["test2@test.com"]

        )

        return super(LeadCreateView,self).form_valid(form)
        
class LeadUpdateView(LoginRequiredMixin,UpdateView):
    template_name = 'leads/lead_update.html'
    queryset = Lead.objects.all()
    form_class = LeadModelForm
    def get_success_url(self) -> str:
        return reverse("leads:lead-list")    

class LeadDeleteView(LoginRequiredMixin,DeleteView):
    template_name = 'leads/lead_delete.html'
    queryset = Lead.objects.all()
    def get_success_url(self) -> str:
        return reverse('leads:lead-list')

def landing(request):
    return render(request,'landing.html')
def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads":leads
    }
    # return HttpResponse("this is a home!!")
    return render(request,'leads/lead_list.html',context)

def lead_detail(request,pk):
    lead = Lead.objects.get(id = pk)
    context = {
        "lead":lead
    }
    return render(request,'leads/lead_details.html',context)

def lead_create(request):
    form = LeadModelForm()
    if request.method == "POST":
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/leads')


    context = {
        "form":LeadModelForm()
    }
    return render(request,'leads/lead_create.html',context)

def lead_update(request,pk):
    lead = Lead.objects.get(id = pk)
    form = LeadModelForm(instance=lead)
    if request.method == "POST":
        form = LeadModelForm(request.POST ,instance=lead)
        if form.is_valid():
            form.save()
            return redirect('/leads')
    context = {

        'form' : form,
        'lead': lead
    }
    return render(request,'leads/lead_update.html',context)
def lead_delete(request,pk):
    lead = Lead.objects.get(id = pk)
    lead.delete()
    return redirect('/leads')


# def lead_update(request,pk):
#     form = LeadForm()
#     lead = Lead.objects.get(id = pk)
#     if request.method == "POST":
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data)
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             lead.first_name = first_name
#             lead.last_name = last_name
#             lead.age = age
#             lead.save()
#             return redirect('/leads')


#     context = {
#         "form": form,
#         'lead': lead
#     }
#     return render(request,'leads/lead_update.html',context)

# def lead_create(request):
#     form = LeadModelForm()
#     if request.method == "POST":
#         form = LeadModelForm(request.POST)
#         if form.is_valid():
#             print(form.cleaned_data)
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             agent = form.cleaned_data['agent']
#             Lead.objects.create(
#                 first_name = first_name,
#                 last_name = last_name,
#                 age = age,
#                 agent = agent
#             )
#             return redirect('/leads')


#     context = {
#         "form":LeadModelForm()
#     }
#     return render(request,'leads/lead_create.html',context)