from flask import Blueprint, jsonify, request
from models import atividade_model
from clients.pessoa_service_client import PessoaServiceClient

atividade_bp2 = Blueprint('atividade_bp2', __name__)

@atividade_bp2.route('/', methods=['GET'])
def listar_atividades():
    atividades = atividade_model.listar_atividades()
    return jsonify(atividades)

@atividade_bp2.route('/<int:id_atividade>', methods=['GET'])
def obter_atividade(id_atividade):
    try:
        atividade = atividade_model.obter_atividade(id_atividade)
        return jsonify(atividade)
    except atividade_model.AtividadeNotFound:
        return jsonify({'erro': 'Atividade não encontrada'}), 404

@atividade_bp2.route('/<int:id_atividade>/professor/<int:id_professor>', methods=['GET'])
def obter_atividade_para_professor(id_atividade, id_professor):
    try:
        # Obtém a atividade com respostas
        atividade = atividade_model.obter_atividade(id_atividade)
        # Verifica se o professor leciona a disciplina
        if not PessoaServiceClient.verificar_leciona(id_professor, atividade['id_disciplina']):
            # Se o professor não leciona, remove as respostas
            atividade = atividade.copy()
            atividade.pop('respostas', None)
        # Retorna a atividade (com ou sem respostas, dependendo do caso)
        return jsonify(atividade)
    except atividade_model.AtividadeNotFound:
        return jsonify({'erro': 'Atividade não encontrada'}), 404
    

# Criar uma nova atividade
@atividade_bp2.route('/', methods=['POST'])
def criar_atividade():
    # Obter os dados da requisição
    dados = request.get_json()
    # Validar se os dados necessários foram enviados
    if 'id_disciplina' not in dados or 'enunciado' not in dados:
        return jsonify({'erro': 'Campos obrigatórios não foram fornecidos'}), 400
    # Criar a nova atividade
    nova_atividade = atividade_model.criar_atividade(dados)
    
    return jsonify(nova_atividade), 201

# Atualizar uma atividade existente
@atividade_bp2.route('/<int:id_atividade>', methods=['PUT'])
def atualizar_atividade(id_atividade):
    dados = request.get_json()
    try:
        atividade_atualizada = atividade_model.atualizar_atividade(id_atividade, dados)
        return jsonify(atividade_atualizada), 200
    except atividade_model.AtividadeNotFound:
        return jsonify({'erro': 'Atividade não encontrada'}), 404

# Excluir uma atividade existente
@atividade_bp2.route('/<int:id_atividade>', methods=['DELETE'])
def excluir_atividade(id_atividade):
    try:
        atividade_model.excluir_atividade(id_atividade)
        return jsonify({'mensagem': 'Atividade excluída com sucesso'}), 200
    except atividade_model.AtividadeNotFound:
        return jsonify({'erro': 'Atividade não encontrada'}), 404