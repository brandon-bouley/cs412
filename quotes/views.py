from django.shortcuts import render
import random

# Lists of quotes and images
quotes = [
    "Sometimes it is the people no one can imagine anything of who do the things no one can imagine.",
    "We can only see a short distance ahead, but we can see plenty there that needs to be done.",
    "Those who can imagine anything, can create the impossible."
]

images = [
    "https://community.esri.com/legacyfs/online/503181_pastedImage_2.png",
    "https://images.fineartamerica.com/images/artworkimages/mediumlarge/1/1-alan-turing-british-mathematician-bill-sanderson.jpg",
    "https://spectrum.ieee.org/media-library/f1.jpg?id=25583742&width=800&quality=85"
]

def quote(request):
    selected_quote = random.choice(quotes)
    selected_image = random.choice(images)
    context = {
        'quote': selected_quote,
        'image': selected_image
    }
    return render(request, 'quotes/quote.html', context)

def show_all(request):
    context = {
        'quotes': quotes,
        'images': images
    }
    return render(request, 'quotes/showall.html', context)

def about(request):
    context = {
        'biography': "Alan Turing was a pioneering British mathematician and computer scientist,\
            widely regarded as the father of theoretical computer science and artificial \
            intelligence. He developed the concept of the Turing machine, a theoretical \
            framework for understanding computation, and played a crucial role in breaking the \
            German Enigma code during World War II, significantly contributing to the Allied victory.\
            Despite his groundbreaking contributions, The life of Alan Turning \
             was tragically cut short after facing persecution for his homosexuality,\
            highlighting both his genius and the societal challenges he faced.",
        'creator': "Brandon Bouley is a Computer Science senior. Who is gay like Alan Turing was. Please give me an A."
    }
    return render(request, 'quotes/about.html', context)