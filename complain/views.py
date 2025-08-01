from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import ComplaintForm
from .models import Complaint

@login_required
def submit_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()
            return render(request, 'complain/thank_you.html')
    else:
        form = ComplaintForm()
    return render(request, 'complain/submit_complaint.html', {'form': form})

# Only police/staff/superuser can view
@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def view_complaints(request):
    complaints = Complaint.objects.all().order_by('-date_submitted')
    return render(request, 'complain/view_complaints.html', {'complaints': complaints})

@user_passes_test(lambda u: u.is_superuser or u.is_staff)
def take_action(request, complaint_id):
    complaint = Complaint.objects.get(id=complaint_id)
    if request.method == 'POST':
        complaint.action_note = request.POST.get('action_note')
        complaint.action_taken = True
        complaint.save()
        return redirect('view-complaints')
    return render(request, 'complain/take_action.html', {'complaint': complaint})
