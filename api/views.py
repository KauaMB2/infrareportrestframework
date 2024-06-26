import os
from .models import Occurrence, Citizen, City
from .serializers import OccurrenceSerializer, CitizenSerializer, CitySerializer
from rest_framework import status
import requests
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from collections import Counter
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from datetime import datetime
from PIL import Image
from io import BytesIO
from django.utils import timezone
from django.db.models import Q
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


@api_view([
    'GET'
])  #It defines the method the user is allowed to do in this route of API
def getRoutes(request):
    routes = [
        '(GET) /', '(POST) /occurrence/',
        '(PUT, DELETE) /occurrence/:id/:citizenAccount/:userEmail/:userPassword',
        '(POST) /postCitizen/', '(POST) /postCity/',
        '(POST) /login/:accountType',
        '(GET) /getAllOccurrences/:cep/:citizenAccount/:accountEmail/:accountPassword',
        '(GET) /getMostRepeatedReports/:cep',
        '(GET) /filterReports/:cep/:specificOccurrence',
        '(GET) /returnImage/:occurrence_id',
        '(PUT) /concludeReport/:controlVar/:occurrence_id',
        '(GET) /searchOccurrences/:cep/:startDate/:endDate/:specificOccurrence'
    ]
    return Response(routes, status=200)  #It returns the routes of the API


@api_view([
    'POST', 'GET'
])  #It defines the method the user is allowed to do in this route of API
def postCity(request):
    if request.method == "GET":  #If the method is GET
        routes = {
            "cep": "string",
            "city_name": "string",
            "state_name": "string",
            "email": "string",
            "password": "string"
        }
        return Response(routes, status=200)  #It returns the routes of the API
    try:  #Try get the JSON data...
        cep, city_name, state_name, email, password = request.data[
            'cep'], request.data["city_name"], request.data[
                'state_name'], request.data['email'], request.data[
                    'password']  #get the request data
        if (cep == "" or city_name == "" or state_name == "" or email == ""
                or password == ""):
            return Response(
                {
                    "Erro":
                    "Há parâmetros vazios que são necessários para a inserção no banco de dados. Certifique-se de que digitou todos os parâmetros de forma correta."
                },
                status=400)  #Return 400
        try:
            response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
            response.raise_for_status()  # Check for HTTP errors
            cityData = response.json()
            # Check if the "erro" key exists in the JSON response
            if not response.ok or "erro" in cityData:
                return Response(
                    {
                        "Erro":
                        "CEP inválido! Certifique-se de que você digitou o CEP corretamente. Observação: O CEP deve ser preenchido somente com números, sem caracteres especiais."
                    },
                    status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(
                {
                    "Erro":
                    "CEP inválido! Certifique-se de que você digitou o CEP corretamente. Observação: O CEP deve ser preenchido somente com números, sem caracteres especiais."
                },
                status=status.HTTP_400_BAD_REQUEST)
    except:  #If the format isnt the correct
        return Response({"Erro": "O formato da requisição não está correto."},
                        status=400)  #Return 400
    cityObject1 = City.objects.filter(email=email).first()
    cityObject2 = City.objects.filter(cep=cep).first()
    citizenObject = Citizen.objects.filter(email=email).first()
    if ((citizenObject != None) or (cityObject1 != None)
            or (cityObject2 != None)):  #Try find a register with this email..
        return Response(
            {'Erro': "Já existe um município com este email ou com este CEP."},
            status=409)
    else:  #If the email doesnt exist in the DB...
        try:  #try insert data
            cityObject = City.objects.create(
                cep=cep,
                city_name=city_name,
                state_name=state_name,
                email=email,
                password=make_password(
                    password))  #Create the new register in DB
        except Exception as e:  #If it was wrong
            print(e)
            return Response(
                {
                    "Erro":
                    "Ocorreu um erro interno no servidor ao criar a conta. Por favor, tente novamente mais tarde.",
                    "Texto": e
                },
                status=500)  #Return 400
    citySerialized = CitySerializer(
        cityObject, many=False
    )  #Object serialized(JSON) | many=False =>Just serialized one object
    return Response(citySerialized.data, status=201)  #Return 200


@api_view([
    'POST', 'GET'
])  #It defines the method the user is allowed to do in this route of API
def postCitizen(request):
    if request.method == "GET":  #If the method is GET
        routes = {
            "cep": "string",
            "city_name": "string",
            "state_name": "string",
            "email": "string",
            "password": "string",
            "neighborhood": "string",
            "street": "string",
            "residential_number": "string",
            "citizen_name": "citizen_name",
        }
        return Response(routes, status=200)  #It returns the routes of the API
    try:  #Try get the JSON data...
        citizen_name, cep, state_name, city_name, neighborhood, street, residential_number, email, password = request.data[
            "citizen_name"], request.data['cep'], request.data[
                'state_name'], request.data['city_name'], request.data[
                    'neighborhood'], request.data['street'], request.data[
                        'residential_number'], request.data[
                            'email'], request.data[
                                'password']  #get the request data
        if (citizen_name == "" or cep == "" or state_name == ""
                or city_name == "" or neighborhood == "" or street == ""
                or residential_number == "" or email == "" or password == ""):
            return Response(
                {
                    "Erro":
                    "Há parâmetros vazios que são necessários para a inserção no banco de dados. Certifique-se de que digitou todos os parâmetros de forma correta."
                },
                status=400)  #Return 400
        try:
            response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
            response.raise_for_status()  # Check for HTTP errors
            cityData = response.json()
            # Check if the "erro" key exists in the JSON response
            if not response.ok or "erro" in cityData:
                return Response(
                    {
                        "Erro":
                        "CEP inválido! Certifique-se de que você digitou o CEP corretamente. Observação: O CEP deve ser preenchido somente com números, sem caracteres especiais."
                    },
                    status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(
                {
                    "Erro":
                    "CEP inválido! Certifique-se de que você digitou o CEP corretamente. Observação: O CEP deve ser preenchido somente com números, sem caracteres especiais."
                },
                status=status.HTTP_400_BAD_REQUEST)
    except:  #If the format isnt the correct
        return Response(
            {"Erro": "O formato do corpo da requisição não está correto."},
            status=400)  #Return 400
    cityObject = City.objects.filter(email=email).first()
    citizenObject = Citizen.objects.filter(email=email).first()
    if citizenObject or cityObject:
        return Response({"Erro": "Já existe um usuário com este email."},
                        status=409)
    else:  #If the email doesnt exist in the DB...
        try:  #try insert data
            citizenObject = Citizen.objects.create(
                citizen_name=citizen_name,
                cep=cep,
                state_name=state_name,
                city_name=city_name,
                neighborhood=neighborhood,
                street=street,
                residential_number=residential_number,
                email=email,
                password=make_password(
                    password))  #Create the new register in DB
        except Exception as e:  #If it was wrong
            print('errrr')
            print(e)
            return Response(
                {
                    "Erro":
                    "Ocorreu um erro interno no servidor ao criar a conta. Por favor, tente novamente mais tarde.",
                    "Texto": e
                },
                status=500)  #Return 500
    citizenSerialized = CitizenSerializer(
        citizenObject, many=False
    )  #Object serialized(JSON) | many=False =>Just serialized one object
    return Response(citizenSerialized.data, status=200)  #Return 200


@api_view([
    'PUT', 'GET', 'DELETE'
])  #It defines the method the user is allowed to do in this route of API
def handleOccurrence(request, id, citizenAccount, userEmail, userPassword):
    try:  #Try find the data
        occurrenceObject = Occurrence.objects.get(
            id=id)  #It returns all the rooms of DB
        occurrenceSerialized = OccurrenceSerializer(
            occurrenceObject, many=False
        )  #Object serialized(JSON) | many=False =>Just serialized one object
    except:  #if it is not registered...
        return Response({"Erro": "Ocorrência selecionada não existe!"},
                        status=404)  #Return 404
    accountObject = None
    if (citizenAccount == 1):
        try:
            accountObject = Citizen.objects.get(email=userEmail)
        except:
            return Response({"Erro": "Cidadão não encontrado."}, status=404)
        if (accountObject.email != occurrenceObject.citizen_email):
            return Response(
                {
                    "Erro":
                    "A conta selecionada não tem permissão para manusear esta ocorrência."
                },
                status=401)
    elif (citizenAccount == 0):
        try:
            accountObject = City.objects.get(email=userEmail)
        except:
            return Response({"Erro": "Cidade não encontrada."}, status=404)
        if (accountObject.cep != occurrenceObject.cep):
            return Response(
                {
                    "Erro":
                    "A conta selecionada não tem permissão para manusear esta ocorrência."
                },
                status=401)
    else:
        return Response(
            {"Erro": "Os parâmetros passados na URL não estão corretos."},
            status=404)
    if request.method == "GET":  #If the method is GET
        try:
            if (check_password(userPassword, accountObject.password)):
                originalCreatedDatatime = occurrenceSerialized.data[
                    "created_at"]
                originalUpdatedDatatime = occurrenceSerialized.data[
                    "updated_at"]
                originalCreatedDatatime_without_ms = originalCreatedDatatime.split(
                    "."
                )[0]  # Remove the milliseconds portion from the original datetime string
                originalUpdatedDatatime_without_ms = originalCreatedDatatime.split(
                    "."
                )[0]  # Remove the milliseconds portion from the original datetime string
                createdDatatime = datetime.fromisoformat(
                    originalCreatedDatatime_without_ms.replace("Z", "+00:00"))
                updatedDatatime = datetime.fromisoformat(
                    originalUpdatedDatatime_without_ms.replace("Z", "+00:00"))
                formattedCreatedDatatime = createdDatatime.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )  # Convert the datetime object to the desired format (e.g., "YYYY-MM-DD HH:mm:ss")
                formattedUpdatedDatatime = createdDatatime.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )  # Convert the datetime object to the desired format (e.g., "YYYY-MM-DD HH:mm:ss")
                updatedData = dict(occurrenceSerialized.data)
                updatedData["created_at"] = formattedCreatedDatatime
                updatedData["updated_at"] = formattedUpdatedDatatime
                if (citizenAccount == 0):
                    citizenObject = Citizen.objects.get(
                        email=occurrenceSerialized.data["citizen_email"])
                    updatedData["userName"] = citizenObject.citizen_name
                    updatedData["userEmail"] = citizenObject.email
                return Response(updatedData, status=200)  #Return 200
            else:
                return Response({"Erro": "Sem autorização! Senha errada."},
                                status=401)
        except Exception as e:  #If the format isnt the correct
            print(e)
            return Response(
                {
                    "Erro":
                    "Ocorreu um erro interno no servidor ao criar a conta. Por favor, tente novamente mais tarde.",
                    "Texto": e
                },
                status=500)  #Return 400
    elif (request.method == "PUT"):  #If the method is PUT
        try:  #Try get the JSON data...
            occurrence_type, neighborhood, street, user_comment, image = request.data[
                "occurrence_type"], request.data['neighborhood'], request.data[
                    'street'], request.data['user_comment'], request.data[
                        'image']  #get the request data
            #print(image)
        except:  #If the format isnt the correct
            return Response(
                {"Erro": "O formato do corpo da requisição não está correto."},
                status=400)  #Return 400
        try:
            citizenObject = Citizen.objects.get(email=userEmail)
        except:
            return Response({"Erro": "Cidadão não encontrado."}, status=404)
        try:
            if (check_password(userPassword, citizenObject.password)):
                occurrenceObject.occurrence_type = occurrence_type  #Modify the data...
                occurrenceObject.neighborhood = neighborhood  #Modify the data...
                occurrenceObject.street = street  #Modify the data...
                occurrenceObject.user_comment = user_comment  #Modify the data...
                if image != None:
                    try:
                        if (occurrenceObject.image.name !=
                                "occurrences/occurrenceVoid.png"):
                            os.remove(
                                os.path.join(settings.MEDIA_ROOT,
                                             occurrenceObject.image.name)
                            )  #Try delete the image if it exist in the folder
                    except:
                        pass
                    occurrenceObject.image = image  #Modify the data...
                occurrenceObject.save()  #Save the modified line in DB
                occurrenceSerialized = OccurrenceSerializer(
                    occurrenceObject, many=False
                )  #Object serialized(JSON) | many=False =>Just serialized one object
                return Response(occurrenceSerialized.data,
                                status=200)  #Return 200
            else:
                return Response({"Erro": "Sem autorização! Senha errada."},
                                status=401)  #Return 400
        except Exception as e:  #If the format isnt the correct
            print(e)
            return Response(
                {
                    "Erro":
                    "Ocorreu um erro interno no servidor ao criar a conta. Por favor, tente novamente mais tarde.",
                    "Texto": e
                },
                status=500)
    elif (request.method == "DELETE"):  #If the method is delete
        try:
            citizenObject = Citizen.objects.get(email=userEmail)
        except:
            return Response({"Erro": "Cidadão não encontrado."}, status=404)
        try:
            if check_password(userPassword, citizenObject.password):
                try:
                    if (occurrenceObject.image.name !=
                            "occurrences/occurrenceVoid.png"):
                        os.remove(
                            os.path.join(settings.MEDIA_ROOT,
                                         occurrenceObject.image.name)
                        )  #Try delete the image if it exist in the folder
                except:
                    pass
                updatedData = dict(occurrenceSerialized.data)
                updatedData["id"] = occurrenceSerialized.data["id"]
                occurrenceObject.delete()  # Delete the Occurrence object
                return Response(
                    {
                        "Mensagem": "A ocorrência foi deletada.",
                        "data": updatedData
                    },
                    status=200)
            else:
                return Response({"Erro": "Sem autorização! Senha errada."},
                                status=401)
        except Exception as e:
            print(e)
            return Response(
                {
                    "Erro":
                    "Ocorreu um erro interno no servidor ao criar a conta. Por favor, tente novamente mais tarde.",
                    "Texto": e
                },
                status=500)


@api_view(['GET'])
def getAllOccurrences(request, cep, citizenAccount, accountEmail,
                      accountPassword):
    try:
        accountObject = None
        if (citizenAccount == 1):
            try:
                accountObject = Citizen.objects.get(email=accountEmail)
            except:
                return Response({"Erro": "Cidadão não encontrado."},
                                status=404)
        elif (citizenAccount == 0):
            try:
                accountObject = City.objects.get(email=accountEmail)
            except:
                return Response({"Erro": "Cidade não encontrada."}, status=404)
        else:
            return Response(
                {"Erro": "Os parâmetros passados na URL não estão corretos."},
                status=404)
        if not (check_password(accountPassword, accountObject.password)):
            return Response({"Erro": "Sem autorização! Senha errada."},
                            status=401)
        allOccurrencesObject = None
        if (citizenAccount == 1):
            allOccurrencesObject = Occurrence.objects.filter(
                cep=cep, citizen_email=accountEmail)
            serializedData = OccurrenceSerializer(allOccurrencesObject,
                                                  many=True)
            return Response(serializedData.data, status=200)  #Return 200
        elif (citizenAccount == 0):
            openedOccurrences = Occurrence.objects.filter(
                cep=cep, concluded="Em aberto")
            oneMonthAgo = timezone.now() - timezone.timedelta(
                days=30
            )  #Get the format of DJANGO DATA TIME of one month ago!!!
            condludedOccurrences = Occurrence.objects.filter(
                Q(concluded="Concluído") & Q(cep=cep)
                & Q(created_at__gte=oneMonthAgo))
            # Combine the lists of occurrences into a single list
            allOccurrences = list(openedOccurrences) + list(
                condludedOccurrences)
            # Serialize the occurrences into a JSON serializable format
            serializedData = OccurrenceSerializer(allOccurrences, many=True)
            return Response(serializedData.data, status=200)  #Return 200
        else:
            return Response(
                {
                    "Erro":
                    "Você somente pode passar '1' ou '0' como parâmetro na URL."
                },
                status=404)
    except Exception as e:  #if it is not registered...
        print(e)
        return Response(
            {
                "Erro":
                "Ainda não existe nenhum registro no banco de dados para esta cidade ou usuário.",
                "Texto": e
            },
            status=404)  #Return 400


@api_view([
    'POST', 'GET'
])  #It defines the method the user is allowed to do in this route of API
def postOccurrence(request):
    if request.method == "GET":  #If the method is GET...
        routes = {
            "citizen_email": "string",
            "cep": "int",
            "occurrence_type": "string",
            "neighborhood": "string",
            "street": "string",
            "user_comment": "string",
            "latitude": "float",
            "longitude": "float",
            "imagem": "file"
        }
        return Response(routes, status=200)  #It returns the routes of the API
    try:  #Try get the JSON data...
        citizen_email, cep, occurrence_type, neighborhood, street, user_comment, latitude, longitude, image = request.data[
            "citizen_email"], request.data["cep"], request.data[
                "occurrence_type"], request.data['neighborhood'], request.data[
                    'street'], request.data['user_comment'], request.data[
                        'latitude'], request.data[
                            'longitude'], request.FILES.get(
                                "image")  #get the request data
        print(request.FILES.get("image"))
        print(request.data['image'])
    except:  #If the format isnt the correct
        return Response(
            {"Erro": "O formato do corpo da requisição não está correto."},
            status=400)  #Return 400
    try:  #Try insert...
        if (image == None):
            occurrenceObject = Occurrence.objects.create(
                citizen_email=citizen_email,
                cep=cep,
                occurrence_type=occurrence_type,
                neighborhood=neighborhood,
                street=street,
                user_comment=user_comment,
                latitude=latitude,
                longitude=longitude)  #Create the new register in DB
        else:
            occurrenceObject = Occurrence.objects.create(
                citizen_email=citizen_email,
                cep=cep,
                occurrence_type=occurrence_type,
                neighborhood=neighborhood,
                street=street,
                user_comment=user_comment,
                latitude=latitude,
                longitude=longitude,
                image=image)  #Create the new register in DB
        occurrenceSerialized = OccurrenceSerializer(
            occurrenceObject, many=False
        )  #Object serialized(JSON) | many=False =>Just serialized one object
        return Response(occurrenceSerialized.data, status=200)  #Return 200
    except Exception as e:  #If it wasnt inserted
        print(e)
        return Response(
            {
                "Erro":
                "Ainda não existe nenhum registro no banco de dados para esta cidade ou usuário.",
                "Texto": e
            },
            status=500)  #Return 500


@api_view([
    'POST', 'GET'
])  #It defines the method the user is allowed to do in this route of API
def login(request, accountType):
    if request.method == "GET":  #If the method is GET
        text = {"email": "string", "password": "string"}
        return Response(text, status=200)  #It returns the routes of the API
    try:
        email, password = request.data["email"], request.data["password"]
        if (email == "" or password == ""):
            return Response(
                {
                    "Erro":
                    "Há parâmetros vazios que são necessários para a inserção no banco de dados. Certifique-se de que digitou todos os parâmetros de forma correta."
                },
                status=400)  #Return 400
    except:  #If the format isnt the correct
        return Response(
            {"Erro": "O formato do corpo da requisição não está correto."},
            status=400)  #Return 400
    accountObject = None
    try:
        if (accountType == "citizen"):
            accountObject = Citizen.objects.get(email=email)
            if (check_password(password, accountObject.password)):
                accountSerialized = CitizenSerializer(
                    accountObject, many=False
                )  #Object serialized(JSON) | many=False =>Just serialized one object
            else:
                return Response({"Erro": "Sem autorização! Senha errada."},
                                status=401)
        elif (accountType == "city"):
            accountObject = City.objects.get(email=email)
            if (check_password(password, accountObject.password)):
                accountSerialized = CitySerializer(
                    accountObject, many=False
                )  #Object serialized(JSON) | many=False =>Just serialized one object
            else:
                return Response({"Erro": "Sem autorização! Senha errada."},
                                status=401)
        else:
            return Response(
                {
                    "Erro":
                    "A conta selecionada não é válida(somente 'city' or 'citizen')."
                },
                status=400)
        return Response(accountSerialized.data, status=200)  #Return 200
    except:
        return Response(
            {"Erro": "A conta selecionada não existe no banco de dados."},
            status=404)


@api_view(["GET"])
def getMostRepeatedReports(request, cep):
    streetValues = Occurrence.objects.filter(cep=cep).values_list(
        'street', flat=True
    )  #flat=True -> Return the response without tuple | flat=False -> Return the response with tuple
    typeValues = Occurrence.objects.filter(cep=cep).values_list(
        'occurrence_type', flat=True
    )  #flat=True -> Return the response without tuple | flat=False -> Return the response with tuple
    streetCounter = Counter(
        streetValues)  # Storage the register of each streets column
    typeCounter = Counter(
        typeValues)  # Storage the register of each streets column
    # Get the most repeated streets and occurrence and their counts
    mostRepeatedReports = streetCounter.most_common(5)
    typeReports = typeCounter.most_common(5)
    # Convert the list of tuples to a list of dictionaries
    reportsList = []
    typeList = []
    for i in range(0, len(mostRepeatedReports), 1):
        street, count1 = mostRepeatedReports[i]
        reportsList.append({'street': street[0:12] + "...", 'count': count1})
    for i in range(0, len(typeReports), 1):
        Type, count2 = typeReports[i]
        typeList.append({'type': Type[0:12] + "...", 'count': count2})
    return Response({"street": reportsList, "type": typeList}, status=200)


@api_view(["GET"])
def filterOccurrences(request, cep, specificOccurrence, citizenAccount,
                      accountEmail, accountPassword):
    try:
        accountObject = None
        if (citizenAccount == 1):
            try:
                accountObject = Citizen.objects.get(email=accountEmail)
            except:
                return Response({"Erro": "Cidadão não encontrado."},
                                status=404)
        elif (citizenAccount == 0):
            try:
                accountObject = City.objects.get(email=accountEmail)
            except:
                return Response({"Erro": "Cidade não encontrada."}, status=404)
        else:
            return Response(
                {"Erro": "Os parâmetros passados na URL não estão corretos."},
                status=404)
        if not (check_password(accountPassword, accountObject.password)):
            return Response({"Erro": "Sem autorização! Senha errada."},
                            status=401)
        specificOccurrences = None
        if (citizenAccount == 1):
            specificOccurrences = Occurrence.objects.filter(
                cep=cep,
                occurrence_type=specificOccurrence,
                citizen_email=accountEmail)
            occurrenceSerialized = OccurrenceSerializer(specificOccurrences,
                                                        many=True)
        elif (citizenAccount == 0):
            specificOccurrences = Occurrence.objects.filter(
                cep=cep, occurrence_type=specificOccurrence)
            occurrenceSerialized = OccurrenceSerializer(specificOccurrences,
                                                        many=True)
        else:
            return Response(
                {
                    "Erro":
                    "Você somente pode passar '1' ou '0' como parâmetro na URL."
                },
                status=404)
            return Response(occurrenceSerialized.data, status=200)
    except Exception as e:
        print(e)
        return Response(
            {
                "Erro":
                "Ainda não existe nenhum registro no banco de dados para esta cidade ou usuário.",
                "Texto": e
            },
            status=404)  #Return 400
    return Response(occurrenceSerialized.data, status=200)


@api_view(["GET"])
def searchOccurrences(request, cep, startDate, endDate, specificOccurrence,
                      citizenAccount, accountEmail, accountPassword):
    try:
        accountObject = None
        if citizenAccount == 1:
            try:
                accountObject = Citizen.objects.get(email=accountEmail)
            except:
                return Response({"Erro": "Cidadão não encontrado."},
                                status=404)
        elif citizenAccount == 0:
            try:
                accountObject = City.objects.get(email=accountEmail)
            except:
                return Response({"Erro": "Cidade não encontrada."}, status=404)
        else:
            return Response(
                {"Erro": "Os parâmetros passados na URL não estão corretos."},
                status=404)
        if not check_password(accountPassword, accountObject.password):
            return Response({"Erro": "Sem autorização! Senha errada."},
                            status=401)

        # Convert start and end date strings to datetime objects
        start_date = datetime.strptime(startDate, '%Y-%m-%d').date()
        end_date = datetime.strptime(endDate, '%Y-%m-%d').date()
        specificOccurrences = None
        if citizenAccount == 1:
            specificOccurrences = Occurrence.objects.filter(
                cep=cep,
                occurrence_type=specificOccurrence,
                citizen_email=accountEmail,
                updated_at__date__range=(start_date, end_date))
            occurrenceSerialized = OccurrenceSerializer(specificOccurrences,
                                                        many=True)
        elif citizenAccount == 0:
            specificOccurrences = Occurrence.objects.filter(
                cep=cep,
                occurrence_type=specificOccurrence,
                updated_at__date__range=(start_date, end_date))
            occurrenceSerialized = OccurrenceSerializer(specificOccurrences,
                                                        many=True)
        else:
            return Response(
                {
                    "Erro":
                    "Você somente pode passar '1' ou '0' como parâmetro na URL."
                },
                status=404)

        return Response(occurrenceSerialized.data, status=200)

    except Exception as e:
        print(e)
        return Response(
            {
                "Erro":
                "Ainda não existe nenhum registro no banco de dados para esta cidade ou usuário.",
                "Texto": str(e)  # Cast the exception to a string
            },
            status=404)


@api_view(["GET"])
def returnImage(request, occurrence_id):
    try:
        occurrence = Occurrence.objects.get(id=occurrence_id)
        image = Image.open(occurrence.image.path)
        image_format = image.format.lower(
        )  # Get the image format (jpeg, jpg, png, etc.)
        # Check if the format is supported (jpeg, jpg, or png)
        if image_format not in ['jpeg', 'jpg', 'png']:
            return Response(
                {
                    "Erro":
                    "Formato de imagem não suportado(somente .jpeg, .jpg ou .png)."
                },
                status=415)
        #Create a BytesIO object to store the image in memory
        image_buffer = BytesIO()
        image.save(image_buffer, format=image_format.upper())
        image_buffer.seek(0)
        #Set the appropriate content type based on the image format
        content_type = f"image/{image_format}"
        #Create the FileResponse with the image data
        image_response = FileResponse(image_buffer, content_type=content_type)
        return image_response
    except FileNotFoundError:
        default_image_path = "media/occurrences/occurrenceVoid.png"
        default_image = Image.open(default_image_path)
        default_image_format = default_image.format.lower()
        image_buffer = BytesIO()
        default_image.save(image_buffer, format=default_image_format.upper())
        image_buffer.seek(0)
        content_type = f"media/{default_image_format}"
        image_response = FileResponse(image_buffer, content_type=content_type)
        return image_response


@api_view(["GET", "PUT"])
def concludeReport(request, controlVar, occurrence_id):
    if request.method == "GET":  #If the method is GET...
        routes = {
            "email": "string",
            "password": "string",
            "user_comment": "string"
        }
        return Response(routes, status=200)  #It returns the routes of the API
    if request.method == "PUT":  #If the method is PUT...
        if (controlVar == 0):
            try:
                cityEmail, cityPassword, cityComment = request.data[
                    "email"], request.data["password"], request.data[
                        "cityComment"]
                if (not cityComment or cityComment == ""
                        or cityComment == "undefined"):
                    return Response(
                        {
                            "Erro":
                            "O comentário da cidade precisa ser válido! Verifique se está vazio!"
                        },
                        status=422)  #Return 400
            except:
                return Response(
                    {"Erro": "O formato da requisição não está correto."},
                    status=400)  #Return 400
            occurrenceObject = get_object_or_404(Occurrence, id=occurrence_id)
            if (occurrenceObject.concluded == "Concluído"):
                return Response({"Erro": "A ocorrência já está concluída!"},
                                status=409)  #Return 400
            cityObject = get_object_or_404(City, email=cityEmail)
            citySerialized = CitySerializer(
                cityObject, many=False
            )  #Object serialized(JSON) | many=False =>Just serialized one object
            if (check_password(cityPassword, citySerialized.data["password"])):
                occurrenceObject.concluded = "Concluído"
                occurrenceObject.city_comment = cityComment
                occurrenceObject.save()
                occurrenceSerialized = OccurrenceSerializer(
                    occurrenceObject, many=False
                )  #Object serialized(JSON) | many=False =>Just serialized one object
                return Response(occurrenceSerialized.data,
                                status=200)  #Return 400
            else:
                return Response({"Erro": "Sem autorização! Senha errada."},
                                status=401)  #Return 400
        if (controlVar == 1):
            try:
                cityEmail, cityPassword = request.data["email"], request.data[
                    "password"]
            except:
                return Response(
                    {"Erro": "O formato da requisição não está correto."},
                    status=400)  #Return 400
            occurrenceObject = get_object_or_404(Occurrence, id=occurrence_id)
            if (occurrenceObject.concluded == "Em aberto"):
                return Response({"Erro": "A ocorrência já está aberta!"},
                                status=409)  #Return 400
            cityObject = get_object_or_404(City, email=cityEmail)
            citySerialized = CitySerializer(
                cityObject, many=False
            )  #Object serialized(JSON) | many=False =>Just serialized one object
            if (check_password(cityPassword, citySerialized.data["password"])):
                occurrenceObject.concluded = "Em aberto"
                occurrenceObject.save()
                occurrenceSerialized = OccurrenceSerializer(
                    occurrenceObject, many=False
                )  #Object serialized(JSON) | many=False =>Just serialized one object
                return Response(occurrenceSerialized.data,
                                status=200)  #Return 400
            else:
                return Response({"Erro": "Sem autorização! Senha errada."},
                                status=401)  #Return 400
