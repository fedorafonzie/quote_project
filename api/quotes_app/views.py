# quote_api/quotes_app/views.py
from rest_framework import generics, filters, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from .models import Quote, Source, Author, Category # Zorg dat alles geïmporteerd is
from .serializers import QuoteSerializer, SourceSerializer # Zorg dat beide serializers geïmporteerd zijn
import random
import requests
from django.conf import settings
from django.shortcuts import get_object_or_404
from .pagination import StandardResultsSetPagination # Importeer
from .filters import QuoteFilter
from django.core.mail import send_mail 


# View voor de volledige lijst + zoeken + filteren
#class QuoteListView(generics.ListAPIView):
 #   queryset = Quote.objects.all().order_by('id')
 #   serializer_class = QuoteSerializer
    # DE FIX: Voeg de filter backend en de juiste veld-configuratie toe
 #   filter_backends = [DjangoFilterBackend, filters.SearchFilter]
 #   filterset_fields = ['source'] # Dit filtert op de ID van de source
 #   search_fields = ['text', 'author__name']
    
class QuoteListView(generics.ListCreateAPIView):
    serializer_class = QuoteSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['source']
    search_fields = ['text', 'author__name']

    def get_queryset(self):
        """
        Deze functie zorgt ervoor dat ALLEEN goedgekeurde quotes
        worden teruggegeven door deze publieke view.
        """
        return Quote.objects.filter(status=Quote.STATUS_APPROVED).order_by('id')  

# View voor de lijst met alle bronnen/categorieën
class SourceListView(generics.ListAPIView):
    queryset = Source.objects.all().order_by('name')
    serializer_class = SourceSerializer

# View voor een willekeurige quote
class RandomQuoteView(generics.RetrieveAPIView):
    serializer_class = QuoteSerializer

    def get_object(self):
        all_quote_ids = Quote.objects.values_list('id', flat=True)
        if not all_quote_ids:
            return None
        random_id = random.choice(list(all_quote_ids))
        return get_object_or_404(Quote, pk=random_id)
        
class QuoteDetailView(generics.RetrieveAPIView):
    """
    Deze view toont één specifieke quote op basis van zijn ID.
    """
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer

# --- VIEW VOOR INZENDINGEN ---
class QuoteSubmitView(generics.CreateAPIView):
    serializer_class = QuoteSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # reCAPTCHA validation
        recaptcha_response = request.data.get('g-recaptcha-response')
        # ... (your reCAPTCHA validation logic) ...

        # Let the serializer handle saving the instance
        self.perform_create(serializer)

        instance = serializer.instance
        try:
            # Gebruik de setting om de URL op te bouwen
            admin_url = f"{settings.FRONTEND_URL}/admin"
            
            send_mail(
                'Nieuwe Quote Wacht op Goedkeuring',
                f'Er is een nieuwe quote ingediend:\n\n"{instance.text}"\n- {instance.author.name if instance.author else "Onbekend"}\n\n'
                f'Ga naar {admin_url} om te beoordelen.', # <-- GEBRUIK DE VARIABELE
                'noreply@jouwwebsite.com',
                ['jouw-email@adres.com'],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Kon e-mail niet versturen: {e}")


        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
# --- NIEUWE VIEW VOOR BEHEER ---
class ModerationViewSet(viewsets.ModelViewSet):
    """
    ViewSet voor het beheren van quotes.
    """
    serializer_class = QuoteSerializer
    permission_classes = [IsAdminUser]

    # We definiëren de queryset nu direct. Dit is de meest robuuste manier.
    queryset = Quote.objects.filter(status=Quote.STATUS_PENDING)

    @action(detail=True, methods=['post'], url_path='approve')
    def approve_quote(self, request, pk=None):
        quote = self.get_object()
        quote.status = Quote.STATUS_APPROVED
        quote.save()
        return Response({'status': 'quote goedgekeurd'})