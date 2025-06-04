# modelos/usuario.py
class Usuario:
    def __init__(self, nome, email, instituicao, senha):
        self.nome = nome
        self.email = email
        self.instituicao = instituicao
        self.senha = senha

    @classmethod
    def from_json(cls, data):
        nome = data.get('nome')
        email = data.get('email')
        instituicao = data.get('instituicao')
        senha = data.get('senha')

        if not all([nome, email, senha]): 
            raise ValueError("Nome, Email e senha são campos obrigatórios para o usuário.")

        return cls(nome, email, instituicao, senha)

    def tojson(self):
        return {
            "nome": self.nome,
            "email": self.email,
            "instituicao": self.instituicao
        }