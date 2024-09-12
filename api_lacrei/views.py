from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from django.utils.html import escape
from django.core.exceptions import ValidationError

from .models import Profissional, Contato, Consulta
from .serializers import ProfissionalSerializer, ConsultaSerializer, ContatoSerializer



# Função central para manipular diferentes modelos (Profissionais, Contatos, Consultas) com base na URL
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def handle_request(request, model_name):
    # Verifica qual modelo foi passado como argumento para direcionar à função correta
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
    # Inserir novo Profissional (POST)
    if request.method == 'POST':
        # Sanitizar campos vulneráveis
        data_sanitized = {
            key: escape(value) if key in ['nome_completo', 'endereco', 'nome_social', 'profissao'] and isinstance(value, str) else value 
            for key, value in request.data.items()
        }
        try:
            profissional = ProfissionalSerializer(data=data_sanitized)
            if not profissional.is_valid():
                return Response(profissional.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # Salva o novo profissional no banco de dados
            profissional.save()
            return Response(profissional.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Atualizar dados de um Profissional (PUT)
    elif request.method == 'PUT':
        try:
            # Busca o profissional a ser atualizado com base no ID fornecido
            id_profissional = request.data.get('id_profissional')

            if not id_profissional:
                return Response({'error': 'ID do profissional é necessário'}, status=status.HTTP_400_BAD_REQUEST)
            
            profissional = Profissional.objects.get(id_profissional=id_profissional)
            
            # Sanitizar campos vulneráveis
            data_sanitized = {
                key: escape(value) if key in ['nome_completo', 'endereco', 'nome_social', 'profissao'] and isinstance(value, str) else value
                for key, value in request.data.items()
            }

            # Serializa os novos dados (parcialmente, apenas os fornecidos)
            serializer = ProfissionalSerializer(profissional, data=data_sanitized, partial=True)

            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # Salva as alterações no banco de dados
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Profissional.DoesNotExist:
            return Response({'error': 'Profissional não encontrado'}, status=status.HTTP_404_NOT_FOUND)

        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': 'Erro ao processar a requisição'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Deletar Profissional (DELETE)
    elif request.method == 'DELETE':
        try:
            id_profissional = request.data.get('id_profissional')
            profissional = Profissional.objects.get(id_profissional=id_profissional)
            
            # Deleta o profissional do banco de dados
            profissional.delete()
            return Response({'message': 'Profissional deletado com sucesso'}, status=status.HTTP_204_NO_CONTENT)
        except Profissional.DoesNotExist:
            return Response({'error': 'Profissional não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    else:
        return Response({'error': 'Método não suportado'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# CRUD - Contatos
def contato_crud(request):
    # Inserir novo Contato (POST)
    if request.method == 'POST':
        # Sanitizar campos vulneráveis
        data_sanitized = {
            key: escape(value) if key in ['tipo', 'contato'] and isinstance(value, str) else value 
            for key, value in request.data.items()
        }

        contato = ContatoSerializer(data=data_sanitized)
        
        if not contato.is_valid():
            return Response(contato.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Verifica se o profissional associado ao contato existe
        try:
            profissional_id = contato.validated_data['profissional'].id_profissional
            Profissional.objects.get(id_profissional=profissional_id)
        except Profissional.DoesNotExist:
            return Response({'error': 'Não existe profissional vinculado ao id passado'}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Salva o contato no banco de dados
            contato.save()
            return Response(contato.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    # Atualizar Contato (PUT)
    elif request.method == 'PUT':
        id_contato = request.data.get('id_contato')
        
        if not id_contato:
            return Response({'error': 'ID do contato é necessário'}, status=status.HTTP_400_BAD_REQUEST)
        
        data_sanitized = {
            key: escape(value) if key in ['tipo', 'contato'] and isinstance(value, str) else value 
            for key, value in request.data.items()
        }

        try:
            # Busca o contato a ser atualizado
            contato = Contato.objects.get(id_contato=id_contato)
            serializer = ContatoSerializer(contato, data=data_sanitized, partial=True)
            
            # Valida os novos dados
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # Salva as alterações
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Contato.DoesNotExist:
            return Response({'error': 'Contato não encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    # Deletar Contato (DELETE)
    elif request.method == 'DELETE':
        try:
            id_contato = request.data.get('id_contato')
            contato = Contato.objects.get(id_contato=id_contato)
            
            # Deleta o contato do banco de dados
            contato.delete()
            return Response({'message': 'Contato deletado com sucesso'}, status=status.HTTP_204_NO_CONTENT)
        except Contato.DoesNotExist:
            return Response({'error': 'Contato não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    else:
        return Response({'error': 'Método não suportado'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# CRUD - Consultas
def consulta_crud(request):
    # Inserir nova Consulta (POST)
    if request.method == 'POST':
        consulta = ConsultaSerializer(data=request.data)

        if not consulta.is_valid():
            return Response(consulta.errors, status=status.HTTP_400_BAD_REQUEST)

        # Verifica se o profissional associado à consulta existe
        try:
            profissional_id = consulta.validated_data['profissional'].id_profissional
            Profissional.objects.get(id_profissional=profissional_id)
        except Profissional.DoesNotExist:
            return Response({'error': 'Não existe profissional vinculado ao id passado'}, status=status.HTTP_404_NOT_FOUND)
        
        # Salva a consulta no banco de dados
        consulta.save()
        return Response(consulta.data, status=status.HTTP_201_CREATED)
    
    # Atualizar Consulta (PUT)
    elif request.method == 'PUT':
        id_consulta = request.data.get('id_consulta')
        
        try:
            # Busca a consulta a ser atualizada
            consulta = Consulta.objects.get(id_consulta=id_consulta)
            serializer = ConsultaSerializer(consulta, data=request.data, partial=True)
            
            # Valida os novos dados
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            # Salva as alterações
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Consulta.DoesNotExist:
            return Response({'error': 'Consulta não encontrada'}, status=status.HTTP_404_NOT_FOUND)

    # Deletar Consulta (DELETE)
    elif request.method == 'DELETE':
        try:
            id_consulta = request.data.get('id_consulta')
            consulta = Consulta.objects.get(id_consulta=id_consulta)
            
            # Deleta a consulta do banco de dados
            consulta.delete()
            return Response({'message': 'Consulta deletada com sucesso'}, status=status.HTTP_204_NO_CONTENT)
        except Consulta.DoesNotExist:
            return Response({'error': 'Consulta não encontrada'}, status=status.HTTP_404_NOT_FOUND)
    
    # Consulta pelo id do profissional (GET)
    elif request.method == 'GET':
        id_profissional = request.data.get('id_profissional')
        try:
            # Busca todas as consultas relacionadas ao profissional
            consulta = Consulta.objects.filter(profissional=id_profissional)

            if not consulta.exists():
                return Response({'error': 'Consulta não encontrada'}, status=status.HTTP_404_NOT_FOUND)
            
            # Serializa as consultas e retorna os dados
            serializer = ConsultaSerializer(consulta, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Profissional.DoesNotExist:
            return Response({'error': 'Profissional não encontrado'}, status=status.HTTP_404_NOT_FOUND)

    else:
        return Response({'error': 'Método não suportado'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
