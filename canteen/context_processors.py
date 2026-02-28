from .models import Report, Rating, Suggestion

def notification_context(request):
    if request.user.is_authenticated and request.user.is_staff:
        # Fetch the most recent 10 items of each type regardless of read status
        recent_reports = list(Report.objects.all().order_by('-created_at')[:10])
        recent_ratings = list(Rating.objects.all().order_by('-created_at')[:10])
        recent_suggestions = list(Suggestion.objects.all().order_by('-created_at')[:10])
        
        all_activities = []
        for r in recent_reports:
            all_activities.append({
                'id': r.id,
                'type': 'Concern',
                'user': 'Anonymous' if r.is_anonymous else r.user.username,
                'content': r.concern_text[:50] + ('...' if len(r.concern_text) > 50 else ''),
                'created_at': r.created_at,
                'is_read': r.is_read
            })
        for r in recent_ratings:
            all_activities.append({
                'id': r.id,
                'type': 'Rating',
                'user': 'Anonymous' if r.is_anonymous or not r.user else r.user.username,
                'content': f"{r.rating} stars: {r.feedback[:40]}...",
                'created_at': r.created_at,
                'is_read': r.is_read
            })
        for s in recent_suggestions:
            all_activities.append({
                'id': s.id,
                'type': 'Suggestion',
                'user': s.user.username if s.user else 'Anonymous',
                'content': s.suggestion_text[:50] + ('...' if len(s.suggestion_text) > 50 else ''),
                'created_at': s.created_at,
                'is_read': s.is_read
            })
        
        all_activities.sort(key=lambda x: x['created_at'], reverse=True)
        
        # We still need unread counts for badges
        total_unread = (
            Report.objects.filter(is_read=False).count() +
            Rating.objects.filter(is_read=False).count() +
            Suggestion.objects.filter(is_read=False).count()
        )
        
        return {
            'unread_notifications': all_activities[:10], # Keep variable name for template compatibility
            'unread_count': total_unread,
            'unread_concerns_count': Report.objects.filter(is_read=False).count(),
            'unread_ratings_count': Rating.objects.filter(is_read=False).count(),
            'unread_suggestions_count': Suggestion.objects.filter(is_read=False).count(),
        }
    return {
        'unread_notifications': [],
        'unread_count': 0,
        'unread_concerns_count': 0,
        'unread_ratings_count': 0,
        'unread_suggestions_count': 0,
    }
