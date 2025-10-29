from datetime import date

class Lead:
    """Representa um Lead no sistema CRM."""
    
    def __init__(self, name: str, company: str, email: str, stage: str = "novo", created: str = None):
        self.name = name.strip()
        self.company = company.strip()
        self.email = email.strip()
        self.stage = stage
        self.created = created if created else date.today().isoformat()

    def to_dict(self):
        """Retorna o Lead como um dicionário para serialização."""
        return {
            "name": self.name,
            "company": self.company,
            "email": self.email,
            "stage": self.stage,
            "created": self.created,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Cria um objeto Lead a partir de um dicionário (para desserialização)."""
        return cls(
            name=data["name"],
            company=data["company"],
            email=data["email"],
            stage=data["stage"],
            created=data["created"],
        )

    def __str__(self):
        return f"Lead(Nome: {self.name}, Empresa: {self.company}, E-mail: {self.email}, Estágio: {self.stage})"

    def __repr__(self):
        return f"Lead(name='{self.name}', email='{self.email}')"
