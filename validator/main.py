from validator.validator import DailyEngagementValidator

def main():
    caminho_csv = r'include/data/2025-05-04.csv'
    validador = DailyEngagementValidator(caminho_csv)

    validador.carregar_csv()
    registros = validador.validar()

    print(f"{len(registros)} registros válidos encontrados.")

if __name__ == "__main__":
    main()
