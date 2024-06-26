from django.urls import path
from .views import getRoutes, postOccurrence, handleOccurrence, postCitizen, postCity, login, getAllOccurrences, getMostRepeatedReports, filterOccurrences, returnImage, concludeReport, searchOccurrences
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [  #Route list
    path('', getRoutes, name="RoutesList"),  # Add one route
    path('occurrence/', postOccurrence,
         name='Post Occurrence'),  # Add one route
    path(
        'occurrence/<int:id>/<int:citizenAccount>/<str:userEmail>/<str:userPassword>',
        handleOccurrence,
        name='Handle Occurrence'),
    path('postCitizen/', postCitizen, name='Post Citizen'),  # Add one route
    path('postCity/', postCity, name="Post City"),  # Add one route
    path('login/<str:accountType>', login, name="Login"),  #Add one route
    path(
        'getAllOccurrences/<int:cep>/<int:citizenAccount>/<str:accountEmail>/<str:accountPassword>',
        getAllOccurrences,
        name="Get All Occurrences"),  #Add one route
    path('getMostRepeatedReports/<int:cep>',
         getMostRepeatedReports,
         name="Get Most Repeated Reports"),  #Add one route
    path(
        'filterReports/<int:cep>/<str:specificOccurrence>/<int:citizenAccount>/<str:accountEmail>/<str:accountPassword>',
        filterOccurrences,
        name="Filter Reports"),  #Add one route
    path('returnImage/<int:occurrence_id>', returnImage,
         name="Return Image"),  #Add one route
    path('concludeReport/<int:controlVar>/<int:occurrence_id>',
         concludeReport,
         name="Conclude Report"),  #Add one route
    path(
        'searchOccurrences/<int:cep>/<str:startDate>/<str:endDate>/<str:specificOccurrence>/<int:citizenAccount>/<str:accountEmail>/<str:accountPassword>',
        searchOccurrences,
        name="Search Reports"),  #Add one route
]

# Add the following lines at the end of your urls.py file for serving media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
