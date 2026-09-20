from django.shortcuts import render, redirect
from django.contrib import messages

from .models import (
    CompanyInfo, ServiceCategory, GalleryImage,
    Partner, ContactMessage, HeroSlide, Stat, Brand,
)


def _shared():
    """Context used by more than one page."""
    return {
        'slides': HeroSlide.objects.filter(is_active=True),
        'partners': Partner.objects.all(),
        'featured_services': ServiceCategory.objects.filter(is_featured=True),
    }


def home(request):
    context = _shared()
    context.update({
        'services': ServiceCategory.objects.filter(is_featured=True)[:6],
        'gallery': GalleryImage.objects.all()[:6],
        'stats': Stat.objects.all()[:4],
    })
    return render(request, 'core/home.html', context)


def about(request):
    context = _shared()
    context['stats'] = Stat.objects.all()[:4]
    return render(request, 'core/about.html', context)


def services(request):
    context = _shared()
    context['products'] = ServiceCategory.objects.filter(kind='product')
    context['services_list'] = ServiceCategory.objects.filter(kind='service')
    context['brands'] = Brand.objects.all()
    return render(request, 'core/services.html', context)


def our_work(request):
    context = _shared()
    context['gallery'] = GalleryImage.objects.all()
    return render(request, 'core/our_work.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        message = request.POST.get('message', '').strip()

        if not name or not message:
            messages.error(request, 'Add your name and a short note about the job, then send again.')
        else:
            ContactMessage.objects.create(
                name=name,
                company_name=request.POST.get('company_name', '').strip(),
                phone=request.POST.get('phone', '').strip(),
                email=request.POST.get('email', '').strip(),
                message=message,
            )
            messages.success(request, 'Message received. Our team will come back to you with a quote.')
            return redirect('contact')

    return render(request, 'core/contact.html', _shared())
