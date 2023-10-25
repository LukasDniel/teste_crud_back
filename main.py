from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)

# Configurações do banco de dados
app.config['MYSQL_HOST'] = 'jobs.visie.com.br'
app.config['MYSQL_USER'] = 'lucasdaniel'
app.config['MYSQL_PASSWORD'] = 'bHVjYXNkYW5p'
app.config['MYSQL_DB'] = 'lucasdaniel'

# Configurar o CORS para permitir solicitações de 'http://localhost:5173'
CORS(app, resources={r"/pessoas/*": {"origins": "http://localhost:5173"}})

mysql = MySQL(app)

# Rota para listar todas as pessoas
@app.route('/pessoas', methods=['GET'])
def listar_pessoas():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM pessoas')
    pessoas = cur.fetchall()
    cur.close()

    # Converter os dados em um dicionário
    pessoas_dict = [{'id_pessoa': pessoa[0], 'nome': pessoa[1], 'data_admissao': pessoa[5]} for pessoa in pessoas]

    return jsonify(pessoas_dict)


# Rota para obter uma pessoa por ID
@app.route('/pessoas/<int:id_pessoa>', methods=['GET'])
def obter_pessoa(id_pessoa):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM pessoas WHERE id_pessoa = %s', (id_pessoa,))
    pessoa = cur.fetchone()
    cur.close()
    if pessoa:
        # Criar um dicionário com os campos desejados
        pessoa_dict = {
            'id_pessoa': pessoa[0],
            'nome': pessoa[1],
            'rg': pessoa[2],
            'cpf': pessoa[3],
            'data_nascimento': pessoa[4],
            'data_admissao': pessoa[5]
        }
        return jsonify(pessoa_dict)
    else:
        return jsonify({'mensagem': 'Pessoa não encontrada'}), 404
# Rota para adicionar uma nova pessoa
@app.route('/pessoas', methods=['POST'])
def adicionar_pessoa():
    data = request.get_json()
    nome = data['nome']
    rg = data['rg']
    cpf = data['cpf']
    data_admissao = data['data_admissao']
    data_nascimento = data.get('data_nascimento', None)  # Use get() para lidar com campos opcionais

    cur = mysql.connection.cursor()
    if data_nascimento is not None:
        cur.execute('INSERT INTO pessoas (nome, rg, cpf, data_admissao, data_nascimento) VALUES (%s, %s, %s, %s, %s)', (nome, rg, cpf, data_admissao, data_nascimento))
    else:
        cur.execute('INSERT INTO pessoas (nome,rg, cpf, data_admissao) VALUES (%s, %s, %s, %s)', (nome, rg, cpf, data_admissao))
    mysql.connection.commit()
    cur.close()
    return jsonify({'mensagem': 'Pessoa adicionada com sucesso'})



@app.route('/pessoas/<int:id_pessoa>', methods=['PUT'])
def atualizar_pessoa(id_pessoa):
    data = request.get_json()
    nome = data['nome']
    rg = data['rg']
    cpf = data['cpf']
    data_nascimento = data['data_nascimento']
    data_admissao = data['data_admissao']

    try:
        cur = mysql.connection.cursor()
        cur.execute('UPDATE pessoas SET nome = %s, rg = %s, cpf = %s, data_nascimento = %s, data_admissao = %s WHERE id_pessoa = %s', (nome, rg, cpf, data_nascimento, data_admissao, id_pessoa))
        mysql.connection.commit()
        cur.close()
        return jsonify({'mensagem': 'Pessoa atualizada com sucesso'})
    except Exception as e:
        return jsonify({'erro': str(e)})


# Rota para excluir uma pessoa por ID
@app.route('/pessoas/<int:id_pessoa>', methods=['DELETE'])
def excluir_pessoa(id_pessoa):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM pessoas WHERE id_pessoa = %s', (id_pessoa,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'mensagem': 'Pessoa excluída com sucesso'})

if __name__ == '__main__':
    app.run(debug=True)
