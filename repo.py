from pathlib import Path
import json, csv
from lead import Lead

class LeadRepository:
    """Encapsula a lógica de persistência e acesso a dados dos Leads."""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.data_dir = db_path.parent
        self.data_dir.mkdir(exist_ok=True)

    def _load(self) -> list[Lead]:
        """Carrega os leads do arquivo JSON e os converte em objetos Lead."""
        if not self.db_path.exists():
            return []
        try:
            raw_leads = json.loads(self.db_path.read_text(encoding="utf-8"))
            return [Lead.from_dict(data) for data in raw_leads]
        except json.JSONDecodeError:
            # Se corromper, começa vazio (decisão didática)
            return []

    def _save(self, leads: list[Lead]):
        """Salva a lista de objetos Lead no arquivo JSON."""
        raw_leads = [lead.to_dict() for lead in leads]
        self.db_path.write_text(json.dumps(raw_leads, ensure_ascii=False, indent=2), encoding="utf-8")

    def read_leads(self) -> list[Lead]:
        """Retorna todos os leads."""
        return self._load()

    def create_lead(self, lead: Lead):
        """Adiciona um novo lead."""
        leads = self._load()
        leads.append(lead)
        self._save(leads)

    def export_csv(self, path: Path = None) -> Path | None:
        """Exporta os leads para CSV. Retorna o caminho do arquivo ou None em caso de erro."""
        path = path if path else (self.data_dir / "leads.csv")
        leads = self._load()
        
        # Converte a lista de objetos Lead para uma lista de dicionários para o csv.DictWriter
        leads_data = [lead.to_dict() for lead in leads]
        
        try:
            with path.open("w", newline="", encoding="utf-8") as f:
                # Os fieldnames devem corresponder às chaves no dicionário retornado por lead.to_dict()
                fieldnames = ["name","company","email","stage","created"]
                w = csv.DictWriter(f, fieldnames=fieldnames)
                w.writeheader()
                w.writerows(leads_data)
            return path
        except PermissionError:
            # Caso o arquivo esteja aberto em outro programa, por exemplo
            return None

# Inicializa o repositório para uso no app.py
DATA_DIR = Path(__file__).resolve().parent / "data"
DB_PATH = DATA_DIR / "leads.json"
lead_repository = LeadRepository(DB_PATH)

# Funções de compatibilidade para manter a interface original, mas usando a classe
def read_leads():
    return lead_repository.read_leads()

def create_lead(lead):
    lead_repository.create_lead(lead)

def export_csv(path=None):
    return lead_repository.export_csv(path)
