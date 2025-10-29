from lead import Lead
from repo import read_leads, create_lead, export_csv

class CRMApp:
    """Aplicações e lógica de menu do Mini-CRM."""

    def __init__(self):
        # A interface de repositório é simplificada para as funções importadas
        pass

    def add_leads(self):
        name = input("Nome: ").strip()
        company = input("Empresa: ").strip()
        email = input("E-mail: ").strip()
        
        # Validação
        if not name or not email or "@" not in email:
            print("Nome e e-mail válido são obrigatórios.")
            return

        # Criação do objeto Lead
        new_lead = Lead(name=name, company=company, email=email)
        
        # Persistência
        create_lead(new_lead)

        print("✔ Lead adicionado!")

    def list_leads(self):
        leads = read_leads()
        if not leads:
            print("Nenhum lead ainda.")
            return
        
        print("\n# | Nome                 | Empresa            | E-mail")
        print("--+----------------------+-------------------+-----------------------")
        for i, l in enumerate(leads):
            # Acessando atributos do objeto Lead
            print(f"{i:02d}| {l.name:<20} | {l.company:<17} | {l.email:<21}")

    def search_flow(self):
        q = input("Buscar por: ").strip().lower()
        if not q:
            print("Consulta vazia.")
            return
            
        leads = read_leads()
        results = []
        for i, l in enumerate(leads):
            # Usando atributos do objeto Lead para a busca
            blob = f"{l.name} {l.company} {l.email}".lower()
            if q in blob:
                results.append((i, l))
                
        if not results:
            print("Nada encontrado.")
            return
            
        print("\n# | Nome                 | Empresa            | E-mail")
        print("--+----------------------+-------------------+-----------------------")
        for i, l in results:
            print(f"{i:02d}| {l.name:<20} | {l.company:<17} | {l.email:<21}")

    def export_leads(self):
        path = export_csv()
        if path is None:
            print("Não consegui escrever o CSV. Feche o arquivo se estiver aberto e tente novamente.")
        else:
            print(f"✔ Exportado para: {path}")

    def print_menu(self):
        print("\nMini CRM de Leads — Aula 2 (Adicionar/Listar/Buscar/CSV)")
        print("[1] Adicionar lead")
        print("[2] Listar leads")
        print("[3] Buscar (nome/empresa/e-mail)")
        print("[4] Exportar CSV")
        print("[0] Sair")

    def main(self):
        while True:
            self.print_menu()
            op = input("Escolha: ").strip()
            if op == "1":
                self.add_leads()
            elif op == "2":
                self.list_leads()
            elif op == "3":
                self.search_flow()
            elif op == "4":
                self.export_leads()
            elif op == "0":
                print("Até mais!")
                break
            else:
                print("Opção inválida.")

if __name__ == "__main__":
    app = CRMApp()
    app.main()
