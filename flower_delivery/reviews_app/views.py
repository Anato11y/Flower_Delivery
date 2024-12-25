from django.shortcuts import render
from .models import Review

def reviews(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        rating = request.POST.get('rating')
        review_text = request.POST.get('review')
        Review.objects.create(user=request.user, product_id=product_id, rating=rating, review=review_text)
    reviews = Review.objects.all()
    return render(request, 'reviews_app/reviews.html', {'reviews': reviews})
