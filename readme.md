# DOKUMENTACE EXTRAKCE INFORMACÍ Z DOKUMENTŮ
# 1. ÚVOD
## 1.1 Současný stav projektu:
- Kód nyní načte jeden PDF soubor, vyextrahuje informace včetně tabulek a vše pošle do databáze. Ke zpracování používá 2 AI nástroje. První je Openai chatbot a druhý je document intelligence studio.

## 1.2 Jak by se dalo pokračovat:
- Redefinování promptů (`questions` v main.py souboru), aby se dosáhlo co nejlepších odpovědí od chatbotu. Redefinování musí proběhnout v souladu se stakeholdery (Šárkou Serbusovou).

- Místo načtení jednoho PDF souboru vymyslet způsob, jak se načtou dokumenty (PDF i Word) rovnou z databáze (ISORu). Dále vymyslet způsob, jak se budou vyextrahované informace ukládat do databáze dynamicky (tj. vytvoření ID, názvu analýzy, přiřazení k skupině subjektů (GCC)).

- Vyzkoušet informace z tabulek vyextrahovat pomocí document intelligence studia a poté se Openai chatbotem dotazovat. Tím by se dalo dotazovat přímo nad informaci, které jsou uložené v tabulkách.

- Místo techniky prompt chainingu, která kombinuje jednak prompt, jednak textove chunky z pdf, zkusit využít embeddingy. Pro více informací viz kód v sekci [Může se hodit](#7-může-se-hodit).

Grafická reprezentace procesu:

![Flowchart](Flowchart.jpg)

Reprezentace procesu pseudokódem:
```plaintext
Start
|
|-- Load Environment Variables
|
|-- Initialize AzureChatOpenAI Client
|
|-- Initialize DocumentIntelligence Client
|
|-- Define Functions
|   |-- extract_text_from_pdf
|   |-- get_pdf_files
|   |-- extract_table_data_from_pdf
|   |-- database
|
|-- Get PDF Files from Directory
|
|-- For Each PDF File
|   |-- Extract Text from PDF
|   |-- Combine Text Chunks
|   |
|   |-- For Each Question
|   |   |-- Formulate Context and Question
|   |   |-- Get Response from Azure OpenAI
|   |   |-- Store Response
|   |
|   |-- Extract Table Data from PDF
|   |-- Update Responses into Database
|
End
```


# 2. [GitHub Repo](https://code.rbi.tech/raiffeisen/rbcz-digi-analyza)
- obsahuje všechny dosavadní kódy a dokumentaci.
  
    - Nejprve je nutné mít přístupy a klíče. Klíče se v kódu volají z .env, to znamená vytvořit virtuální prostředí a do něj vypsat údaje.

        ```sh
        AZURE_OPENAI_KEY = 'placeholder'
        AZURE_OPENAI_ID = 'placeholder'
        DOCUMENT_STUDIO_END_POINT = 'https://rbczdi01.cognitiveservices.azure.com/'
        DOCUMENT_STUDIO_KEY = 'placeholder'
        ORACLE_USER = 'placeholder'
        ORACLE_PASSWORD = 'placeholder' 
        ```

    1. **oracle database:** Pro přístup kontaktovat Václava Arnoše
        ```python
        user=os.getenv("ORACLE_USER")
        password=os.getenv("ORACLE_PASSWORD")
        ``` 
    2. **openai api:** Pro přístup viz bod [4](#4-dokumentace-rbcz-azure-openai-api).
        ```python
        default_headers={"id": os.getenv("AZURE_OPENAI_ID")}
        openai_api_key=os.getenv("AZURE_OPENAI_KEY")
        ```

    3. **document intelligence api:** Pro přístup kontaktovat Martina Hajného
        ```python
        endpoint=os.getenv("DOCUMENT_STUDIO_END_POINT")
        key=os.getenv("DOCUMENT_STUDIO_KEY")
        ```

    - **DB_connection.py**

        Tento skript slouží jako ukázka, jak se připojit k databázi a aktualizovat data.

    - **document_answering.py**

        Tento skript ukazuje, jak vypromptovat informace z pdf dokumentu a uložit je do csv souboru.  

    - **document_intelligence.py**

        Tento skript extrahuje tabulky z pdf souboru a uloží ji do HTML tagů, které jsou nutné pro správné uložení do oracle databáze (v aplikaci se pak ukážou jako tabulky).

    - **main.py**

        Hlavní skript, který v sobě implementuje všechny 3 předchozí kódy. 
        Kód automatizuje proces extrakce informací z PDF dokumentů a jejich ukládání do databáze. Zde je stručný popis kroků, které kód provádí:

        1.**Načtení nastavení**: Kód načte potřebné nastavení a přihlašovací údaje z prostředí.

        2. **Inicializace služeb**: Kód inicializuje dvě služby:

            **AzureChatOpenAI**: Tato služba umožňuje komunikaci s umělou inteligencí, která odpovídá na otázky.

            **DocumentIntelligenceClient**: Tato služba analyzuje PDF dokumenty a extrahuje z nich tabulky.
            Načtení PDF souborů: Kód načte všechny PDF soubory z určené složky.

        3. **Definování promptů**: Obsahuje všechny prompty, která nám poskytla Šárka a její tým. 

        4. **Zpracování PDF souborů**: Pro každý PDF soubor kód:

            Extrahuje text z PDF souboru.
            Položí každou otázku umělé inteligenci a získá odpovědi.
            Extrahuje tabulky z PDF dokumentu.

        5. **Uložení odpovědí do databáze**: Kód uloží získané odpovědi a tabulky do databáze.

        6. **Výpis odpovědí**: Kód vytiskne odpovědi a tabulky pro každý PDF soubor.

    - **mapping.txt**

        obsahuje názvy formulářových polí v aplikaci a jejich korespondující sloupce v oracle databázi.  

    - **feedback.docx**

        obsahuje zpětnou vazbu na prvotní prompty od Šárky a jejího týmu. 

    - **requirements.txt**

        obsahuje všechny nutné balíčky pro rozběhnutí kódů. pro instalaci je možné využít příkaz:
        ```
        pip install -r requirements.txt
        ```

# 3. [Python v RB - návody a dokumentace](https://python.rb.cz/)
- jak nainstalovat Python,
- jak si zažádat o přístup do Artifactory (repozitář balíčku jako pandas, openai, etc.)
- jak vytvořit virtuální prostředí
- jak nainstalovat balíčky
- doporučuji používat VSCode a tyto rozšíření (Jupyter, Office Viewer, Rainbow CSV, vscode-pdf, GitHub Copilot)
# 4. [Dokumentace RBCZ Azure OpenAI API](https://confluence.rb.cz/confluence/x/L6t2C)
- jak zažádat o id a klíč 
- jak používat openai api + [ukázky kódů](https://git.rb.cz/bitbucket/projects/PYT/repos/example-ai-getting-started/browse)

# 5. Oracle databáze
- přístup zajistí Václav Arnoš
- název testovací databáze: 
```
BDW1L1S
```
- název tabulky, ve které jsou uložená data:
```
DAAnalysisSheetData
```
- *mapping.txt* usnadňuje orientaci v tabulce. Ukazuje formulářové pole v aplikaci a příslušný sloupec v tabulce


# 6. [Aplikace](https://bi.rb.cz/aicat)
-  testovací aplikace

# 7. Může se hodit:
    
-   Příručka Datového Analytika:
    https://confluence.rb.cz/confluence/display/PDA

-   Ask your document aplikace: https://risk-test.rb.cz/corporate_inquiry + kód https://code.rbi.tech/ICZAA744/Corp-Annual-Reports-Inquiry (obsahuje embeddingy, rag a další)

    