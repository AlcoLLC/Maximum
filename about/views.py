from django.shortcuts import render
from .models import About, AboutContent, AboutSection, GlobalPresence, Sustainability, PartnershipContent
from home.models import CarLogo

def about_view(request):
    about = About.objects.first()
    about_contents = AboutContent.objects.all()
    about_section = AboutSection.objects.first()
    global_presence = GlobalPresence.objects.first()
    sustainability = Sustainability.objects.first()
    partnership_content = PartnershipContent.objects.first()
    car_logos = CarLogo.objects.all()

    context = {
        'about': about,
        'about_contents': about_contents,
        'about_section': about_section,
        'global_presence': global_presence,
        'sustainability': sustainability,
        'partnership_content': partnership_content,
        'car_logos': car_logos,
    }
    return render(request, 'about.html', context)
