from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Category, MenuItem, Report, Rating, Suggestion, STALL_CHOICES
from .utils import contains_profanity
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'canteen/home.html')

@login_required
def activity_feed(request):
    if not request.user.is_staff:
        messages.error(request, "Access denied. Admins only.")
        return redirect('home')
        
    activities = []
    reports = list(Report.objects.order_by('-created_at')[:20])
    ratings = list(Rating.objects.order_by('-created_at')[:20])
    suggestions = list(Suggestion.objects.order_by('-created_at')[:20])
    
    for r in reports:
        activities.append({
            'id': r.id,
            'type': 'Concern',
            'user': 'Anonymous' if r.is_anonymous else r.user.username,
            'content': f"For {r.stall}: {r.concern_text[:100]}" + ('...' if len(r.concern_text) > 100 else ''),
            'full_content': f"Concern for {r.stall}:\n\n{r.concern_text}",
            'is_read': r.is_read,
            'created_at': r.created_at,
            'icon': 'alert-circle',
            'meta': f"Reported by: {'Anonymous' if r.is_anonymous else r.user.username} | Section: {r.grade_section or 'N/A'} | Posted on: {r.created_at.strftime('%b %d, %Y %I:%M %p')}"
        })
    for r in ratings:
        activities.append({
            'id': r.id,
            'type': 'Rating',
            'user': 'Anonymous' if r.is_anonymous or not r.user else r.user.username,
            'content': f"{r.rating} stars for {r.stall}: {r.feedback[:100]}...",
            'full_content': f"Rating for {r.stall}:\n\nRating: {r.rating} Stars\nFood: {r.food_name or 'N/A'}\n\nFeedback: {r.feedback}",
            'is_read': r.is_read,
            'created_at': r.created_at,
            'icon': 'star',
            'meta': f"Rated by: {'Anonymous' if r.is_anonymous or not r.user else r.user.username} | Posted on: {r.created_at.strftime('%b %d, %Y %I:%M %p')}"
        })
    for s in suggestions:
        activities.append({
            'id': s.id,
            'type': 'Suggestion',
            'user': s.user.username if s.user else 'Anonymous',
            'content': f"For {s.stall}: {s.suggestion_text[:100]}...",
            'full_content': f"Suggestion for {s.stall}:\n\n{s.suggestion_text}",
            'is_read': s.is_read,
            'created_at': s.created_at,
            'icon': 'lightbulb',
            'meta': f"Suggested by: {s.user.username if s.user else 'Anonymous'} | Posted on: {s.created_at.strftime('%b %d, %Y %I:%M %p')}"
        })
        
    activities.sort(key=lambda x: x['created_at'], reverse=True)
    activities = activities[:50]  # Show more on the dedicated page

    return render(request, 'canteen/activity_feed.html', {'activities': activities})

from django.http import JsonResponse
@login_required
def mark_activity_read(request, activity_type, activity_id):
    if not request.user.is_staff:
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
    
    try:
        if activity_type == 'Concern':
            item = Report.objects.get(id=activity_id)
        elif activity_type == 'Rating':
            item = Rating.objects.get(id=activity_id)
        elif activity_type == 'Suggestion':
            item = Suggestion.objects.get(id=activity_id)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid type'}, status=400)
        
        item.is_read = True
        item.save()
        return JsonResponse({'status': 'success'})
    except (Report.DoesNotExist, Rating.DoesNotExist, Suggestion.DoesNotExist):
        return JsonResponse({'status': 'error', 'message': 'Item not found'}, status=404)

@login_required
def suggestion_view(request):
    if request.method == 'POST':
        stall = request.POST.get('stall')
        suggestion_text = request.POST.get('suggestion_text')
        
        if contains_profanity(suggestion_text):
            messages.error(request, "Your suggestion contains unprofessional language. Please revise it.")
            return render(request, 'canteen/suggestion_box.html', {'stalls': STALL_CHOICES, 'suggestion_text': suggestion_text, 'selected_stall': stall})

        Suggestion.objects.create(
            user=request.user,
            stall=stall,
            suggestion_text=suggestion_text
        )
        messages.success(request, "Your suggestion has been submitted. Thank you!")
        return redirect('home')
        
    return render(request, 'canteen/suggestion_box.html', {'stalls': STALL_CHOICES})

@login_required
def rate_view(request):
    if request.method == 'POST':
        stall = request.POST.get('stall')
        rating_val = request.POST.get('rating')
        food_name = request.POST.get('food_name')
        feedback = request.POST.get('feedback')
        is_anonymous = request.POST.get('is_anonymous') == 'on'
        
        if contains_profanity(food_name) or contains_profanity(feedback):
            messages.error(request, "Your rating contains unprofessional language. Please revise it.")
            return render(request, 'canteen/ratings.html', {
                'stalls': STALL_CHOICES, 
                'food_name': food_name, 
                'feedback': feedback, 
                'selected_stall': stall,
                'rating': rating_val
            })

        Rating.objects.create(
            user=request.user,
            stall=stall,
            rating=rating_val,
            food_name=food_name,
            feedback=feedback,
            is_anonymous=is_anonymous
        )
        messages.success(request, "Your rating has been submitted. Thank you!")
        return redirect('home')
        
    return render(request, 'canteen/ratings.html', {'stalls': STALL_CHOICES})

@login_required
def report_concern(request):
    if request.method == 'POST':
        reporter_name = request.POST.get('reporter_name')
        grade_section = request.POST.get('grade_section')
        stall = request.POST.get('stall')
        gender = request.POST.get('gender')
        is_anonymous = request.POST.get('is_anonymous') == 'on'
        concern_text = request.POST.get('concern_text')
        
        if contains_profanity(concern_text) or (reporter_name and contains_profanity(reporter_name)):
            messages.error(request, "Your concern contains unprofessional language. Please revise it.")
            return render(request, 'canteen/report_form.html', {
                'stalls': STALL_CHOICES,
                'reporter_name': reporter_name,
                'grade_section': grade_section,
                'selected_stall': stall,
                'gender': gender,
                'concern_text': concern_text
            })

        Report.objects.create(
            user=request.user,
            reporter_name=reporter_name,
            grade_section=grade_section,
            stall=stall,
            gender=gender,
            is_anonymous=is_anonymous,
            concern_text=concern_text
        )
        messages.success(request, "Your concern has been submitted successfully.")
        return redirect('report_history')
        
    return render(request, 'canteen/report_form.html', {'stalls': STALL_CHOICES})



@login_required
def report_history(request):
    reports = Report.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'canteen/report_history.html', {'reports': reports})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'canteen/login.html', {'error': 'Invalid username or password'})
            
    return render(request, 'canteen/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            return render(request, 'canteen/register.html', {'error': 'Passwords do not match'})
            
        if User.objects.filter(username=username).exists():
            return render(request, 'canteen/register.html', {'error': 'Username already exists'})
            
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        return redirect('home')
        
    return render(request, 'canteen/register.html')

def logout_view(request):
    logout(request)
    return redirect('login')
