from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Profissional, Contato, Consulta
from .serializers import ProfissionalSerializer, ConsultaSerializer, ContatoSerializer


# Função central para CRUD
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def handle_request(request, model_name):
    if model_name == 'profissionais':
        return profissional_crud(request)
    elif model_name == 'contatos':
        return contato_crud(request)
    elif model_name == 'consultas':
        return consulta_crud(request)
    else:
        return Response({'error': 'Model não encontrado'}, status=status.HTTP_400_BAD_REQUEST)


# CRUD - Profissionais
def profissional_crud(request):
    # Inserir novo Profissional
    if request.method == 'POST':
        profissional = ProfissionalSerializer(data=request.data)
        if not profissional.is_valid():
            return Response(profissional.errors, status=status.HTTP_400_BAD_REQUEST)
        
        profissional.save()
        return Response(profissional.data, status=status.HTTP_201_CREATED)
    
    # Atualizar dados de um Profissional
    elif request.method == 'PUT':
        try:
            id_profissional = request.data.get('id_profissional')
      
            profissional = Profissional.objects.get(id_profissional=id_profissional)
            serializer = ProfissionalSerializer(profissional, data=request.data, partial=True)

            if not serializer.is_valid():
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK) 
        except:
            return Response({'error': 'Profissional não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    # Deletar Profissional 
    elif request.method == 'DELETE':
        try:
            id_profissional = request.data.get('id_profissional')
            profissional = Profissional.objects.get(id_profissional=id_profissional)
            profissional.delete()
            return Response({'message': 'Profissional deletado com sucesso'}, status=status.HTTP_204_NO_CONTENT)
        except Profissional.DoesNotExist:
            return Response({'error': 'Profissional não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    else:
        return Response({'error': 'Método não suportado'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    

# CRUD - Contatos
def contato_crud(request):
    # Inserir novo Contato
    if request.method == 'POST':
        contato = ContatoSerializer(data=request.data)
        
        if not contato.is_valid():
            return Response(contato.errors, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            profissional_id = contato.validated_data['profissional'].id_profissional
            Profissional.objects.get(id_profissional=profissional_id)
        except Profissional.DoesNotExist:
            return Response({'error': 'Não existe profissional vinculado ao id passado'}, status=status.HTTP_404_NOT_FOUND)
        
        contato.save()
        return Response(contato.data, status=status.HTTP_201_CREATED)

    # Atualizar Contato
    elif request.method == 'PUT':

        id_contato = request.data.get('id_contato')
        
        try:
            # Encontre o contato a ser atualizado
            contato = Contato.objects.get(id_contato=id_contato)
            serializer = ContatoSerializer(contato, data=request.data, partial=True)
            
            # Valide os dados
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # Salve as alterações
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Contato.DoesNotExist:
            return Response({'error': 'Profissional não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    # Deletar Contato 
    elif request.method == 'DELETE':
        try:
            id_contato = request.data.get('id_contato')
            contato = Contato.objects.get(id_contato=id_contato)
            contato.delete()
            return Response({'message': 'Contato deletado com sucesso'}, status=status.HTTP_204_NO_CONTENT)
        except Contato.DoesNotExist:
            return Response({'error': 'Contato não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        
    else:
        return Response({'error': 'Método não suportado'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# CRUD - Consultas
def consulta_crud(request):
    # Inserir nova Consulta
    if request.method == 'POST':
        consulta = ConsultaSerializer(data=request.data)

        if not consulta.is_valid():
            return Response(consulta.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            profissional_id = consulta.validated_data['profissional'].id_profissional
            Profissional.objects.get(id_profissional=profissional_id)
        except Profissional.DoesNotExist:
            return Response({'error': 'Não existe profissional vinculado ao id passado'}, status=status.HTTP_404_NOT_FOUND)
        
        consulta.save()
        return Response(consulta.data, status=status.HTTP_201_CREATED)
    
    # Atualizar Consulta
    elif request.method == 'PUT':

        id_consulta = request.data.get('id_consulta')
        
        try:
            # Encontre a consulta a ser atualizado
            consulta =  Consulta.objects.get(id_consulta=id_consulta)
            serializer = ConsultaSerializer(consulta, data=request.data, partial=True)
            
            # Valide os dados
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # Salve as alterações
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Contato.DoesNotExist:
            return Response({'error': 'Profissional não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    # Deletar Consulta 
    elif request.method == 'DELETE':
        try:
            id_consulta = request.data.get('id_consulta')
            consulta = Consulta.objects.get(id_consulta=id_consulta)
            consulta.delete()
            return Response({'message': 'Consulta deletado com sucesso'}, status=status.HTTP_204_NO_CONTENT)
        except Consulta.DoesNotExist:
            return Response({'error': 'Consulta não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    # GET consulta pelo id do profissional
    elif request.method == 'GET':
        id_profissional = request.data.get('id_profissional')
        try:
            consulta = Consulta.objects.filter(profissional=id_profissional)

            if not consulta.exists():
                return Response({'error': 'Consultado não encontrada'}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = ConsultaSerializer(consulta, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK )    
        except Profissional.DoesNotExist:
                return Response({'error': 'Profissional não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    else:
        return Response({'error': 'Método não suportado'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
