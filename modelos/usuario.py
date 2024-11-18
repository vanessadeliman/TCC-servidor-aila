class Usuario:
    def __init__(self, nome, email, instituicao, cargo):
        self.nome = nome
        self.email = email
        self.instituicao = instituicao
        self.cargo = cargo

    @classmethod
    def from_json(cls, data):

        return cls(
            nome=data.get("nome"),
            email=data.get("email"),
            instituicao=data.get("instituicao"),
            cargo=data.get("cargo"),
        )

    def tojson(self):
        return {"nome":self.nome, "email":self.email, "instituicao":self.instituicao, "cargo":self.cargo}
