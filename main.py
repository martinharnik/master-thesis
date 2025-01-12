from langchain.schema import HumanMessage
from utils import get_pdf_files, extract_text_from_pdf, extract_table_data_from_pdf, database, llm

# Directory containing the PDF files
pdf_directory = "./pdf_files"  # Replace with the name of your directory

# Get all PDF files in the directory
pdf_files = get_pdf_files(pdf_directory)

# Define the questions to be asked
questions = [
    "Dej mi přesný přepis všech informací týkajících se činnosti klienta, co je jeho hlavní činností, jaký je výrobní cyklus klienta.",
    "Dej mi přesný přepis strategických plánů společnosti do budoucna, na co se chce společnost zaměřovat.",
    "Dej mi přesný přepis informací o sezonnosti businessu firmy. Pokud najdeš informace prokazující změnu, nebo volatilitu tržeb a ziskovosti v průběhu roku v závislosti na období, uveď je.",
    "Kdo jsou jeho hlavní zákazníci, jakým způsobem s nimi spolupracuje, jak dlouho s nimi spolupracuje, do jakých odvětví dodává, jaké má uzavřené smlouvy, objednávky. Jaká je závislost na odběratelích, jak je možné je nahradit, jaká je diverzifikace, jaké jsou platební podmínky, z jakých destinací jsou zákazníci, jaká je výše exportu, jakým způsobem získává nové zákazníky.",
    "Kdo jsou jeho hlavní dodavatelé, jakým způsobem s nimi spolupracuje, jak dlouho s nimi spolupracuje, jaká je závislost na konkrétním dodavateli, jaká je možnost substituce dodavatele, jaká je diverzifikace, jaké jsou platební podmínky, volatilita ceny komodit, z jakých destinací odebírá, jaké jsou hlavní vstupy, jaká je výše importu.",
    "Dej mi přesný přepis týkající se zásob, vývoj objemu a kvality zásob + doba obratu + časová struktura.",
    "Dej mi přesný přepis zkušeností manažerů, délku jejich fungování ve firmě, zda existuje nějaký key man risk a v čem spočívá.",
    "Dej mi přesný přepis všech informací, které se týkají zakázek, pokud se jedná o společnost zabývající se zakázkovou výrobou, pokud ne, nech pole prázdné.",
    "Dej mi přesný přepis informací o výrobních závodech, skladovacích kapacitách, strojních kapacitách a množství zaměstnanců, které souvisí s kapacitními možnostmi firmy, jakou klient využívá technologii a jaké je její stáří.",
    "Dej mi přesný přepiš informací týkající charakteristiky odvětví nebo také Industry characteristics. Informace v souboru jsou rozděleny nadpisy a odrážkami.",
    "Dej mi přesný přepiš informací týkající vývoj odvětví nebo také Industry development. Informace v souboru jsou rozděleny nadpisy a odrážkami.",
    "Dej mi přesný přepiš informací týkající pozice na trhu nebo také Market position. Informace v souboru jsou rozděleny nadpisy a odrážkami.",
    "Dej mi přesný přepiš informací týkající srovnání s konkurencí nebo také Peer Analysis. Informace v souboru jsou rozděleny nadpisy a odrážkami.",
    "Pokud existují nějaké negativní informace o spolupráci s bankami, prodlení ve splácení, neplnění podmínek a další, uveď je zde.",
    "Dej mi přesný přepis toho, s jakými bankami klient spolupracuje, jaké produkty využívá, jaká je současná doba spolupráce s bankou.",
    "Dej mi přesný přepis provozního financování, které klient využívá - kdy jsou splatné, výše poskytnutého limitu, výše zůstatku ke konci roku, poskytovatel úvěru a další informace, které s provozním financováním souvisí.",
    "Dej mi přesný přepis investičních úvěrů, které klient využívá - kdy jsou splatné, účel, výše celkového poskytnutého limitu, výše zůstatku ke konci roku, splátky v jednotlivých letech, poskytovatel úvěru a další informace, které s investičními půjčkami souvisí. Pokud nejsou žádné informace na toto téma k dispozici, jako odpověď uveď pouze slovo “N/A”.",
    "Dej mi přesný přepis leasingů, které klient využívá - kdy jsou splatné, výše celkového poskytnutého limitu, výše zůstatku ke konci roku, splátky v jednotlivých letech, poskytovatel úvěru, účel poskytnutí a další informace, které s leasingy souvisí. Pokud nejsou žádné informace na toto téma k dispozici, jako odpověď uveď pouze slovo “N/A”.",
    "Dej mi přesný přepis garancí ve smyslu bankovních záruk, jaké klient využívá. Vynech záruky poskytnuté některou sesterskou, mateřskou, nebo dceřinou společností. Dej mi informace o objemu limitů, objemu a trvání vystavených záruk, typy záruk a další informace související s bankovními zárukami. Pokud nejsou žádné informace na toto téma k dispozici, jako odpověď uveď pouze slovo “N/A”.",
    "Dej mi přesný přepis využívání faktoringu, jeho poskytovatel, výše limitu a výše zůstatku ke konci roku. Pokud nejsou žádné informace na toto téma k dispozici, jako odpověď uveď pouze slovo “N/A”.",
    "jaká část příjmů nebo výdajů je v jiné měně než v CZK, zda má otevřenou pozici (příjmy v cizí měně jsou větší než výdaje v cizí měně nebo naopak). Pokud existuje otevřená pozice (nepokrytá přirozeným zajištěním) zjišťujeme, zda ji klient dozajišťuje nějakým jiným způsobem.",
    "Dej mi shrnutí finanční situace klienta.",
    "Dej mi přesný přepis celoročních a průběžných finančních výkazů, vývoj tržeb, obchodní marže, EBITDA, EBITDA marže, výkonové spotřeby, osobní náklady, jiné provozní náklady a výnosy, všechny další významné položky týkající se výkazů zisku a ztrát, meziroční porovnání. Dej mi přesný přepis rozvahy, konkrétně kapitálové struktury, EqR, FAC, CR, krátkodobých a dlouhodobých půjček, obchodních závazků a pohledávek, intragroup pohledávek a závazků, jiných pohledávek a závazků , zásob. Najdi nadpis Financial Risk Evaluation a od něj dál vyber část týkající se přístušné společnosti. Tuto sekci pak přesně přepiš.",
    "Dej mi přesný přepis informace týkající se schopnosti vedení a managementu plánovat. Pokud existují informace o plnění plánu z předchozích let, uveď je zde.",
    "Dej mi přesný přepis projekce klienta na další období, týkající se vývoje tržeb, EBITDA, CAPEX, pokrytí dluhové služby, DSCR, změna pracovního kapitálu, vývoje vlastního kapitálu, nákladových úroků, splácení úvěrů."
]

# Process each PDF file separately
for pdf_file in pdf_files:
    # Extract text from the PDF document
    pdf_chunks = extract_text_from_pdf(pdf_file)

    # Combine all text chunks into a single string
    pdf_text = " ".join(pdf_chunks)

    # Prepare a list to store responses for the current PDF
    responses = []

    # Iterate through each question
    for question in questions:
        # Create a clear and concise context with the question
        context_and_question = f"""
        Jsi asistent pro extrakci informací z PDF dokumentů. Úkolem je poskytnout odpovědi na konkrétní otázky.
        Následující text je obsahem PDF dokumentu:
        {pdf_text}

        Úkol: Odpověz na následující otázku v českém jazyce:
        {question}

        - Poskytuj fakta na základě textu a vyhýbej se spekulacím.
        - Nepoužívej žádné speciální formátování (** nebo ###).
        - Odpovědi by měly být stručné, přehledné, a v odstavcích.
        """

        # Get the response from Azure OpenAI
        response = llm.invoke(input=[HumanMessage(content=context_and_question)]).content
        # Append the response to the list
        responses.append(response)

    # Extract table data from the PDF document
    table_data = extract_table_data_from_pdf(pdf_file) 

    # Update the responses into the database
    with database() as my_db:
        update_queries = [
            ("UPDATE \"DAAnalysisSheetData\" SET \"BusinessModel\" = :1 WHERE \"Id\" = 202", responses[0]),
            ("UPDATE \"DAAnalysisSheetData\" SET \"BusinessStrategy\" = :1 WHERE \"Id\" = 202", responses[1]),
            ("UPDATE \"DAAnalysisSheetData\" SET \"BusinessSeasonalityDescription\" = :1 WHERE \"Id\" = 202", responses[2]),
            ("UPDATE \"DAAnalysisSheetData\" SET \"BusinessCustomersISOR\" = :1 WHERE \"Id\" = 202", responses[3]),
            ("UPDATE \"DAAnalysisSheetData\" SET \"BusinessSuppliersISOR\" = :1 WHERE \"Id\" = 202", responses[4]),
            ("UPDATE \"DAAnalysisSheetData\" SET \"BusinessInventoryManagement\" = :1 WHERE \"Id\" = 202", responses[5]),
            ("UPDATE \"DAAnalysisSheetData\" SET \"BusinessManagement\" = :1 WHERE \"Id\" = 202", responses[6]),
            ("UPDATE \"DAAnalysisSheetData\" SET \"BusinessBacklog\" = :1 WHERE \"Id\" = 202", responses[7]),
            ("UPDATE \"DAAnalysisSheetData\" SET \"BusinessCapacityIssueDescript~\" = :1 WHERE \"Id\" = 202", responses[8]),
            ("UPDATE \"DAAnalysisSheetData\" SET \"IndustryCharacteristics\" = :1 WHERE \"Id\" = 202", responses[9]),
            ("UPDATE \"DAAnalysisSheetData\" SET \"IndustryDevelopment\" = :1 WHERE \"Id\" = 202", responses[10]),
            ("UPDATE \"DAAnalysisSheetData\" SET \"IndustryMarketPosition\" = :1 WHERE \"Id\" = 202", responses[11]),
            ("UPDATE \"DAAnalysisSheetData\" SET \"IndustryPeerAnalysis\" = :1 WHERE \"Id\" = 202", responses[12]),
            ("UPDATE \"DAAnalysisSheetData\" SET \"BankPositionRiskDescription\" = :1 WHERE \"Id\" = 202", responses[13]),
            ("UPDATE \"DAAnalysisSheetData\" SET \"BankPositionRiskRelationShipD~\" = :1 WHERE \"Id\" = 202", responses[14]),
            ("UPDATE \"DAAnalysisSheetData\" SET \"BankPositionOperatingLimitsDe~\" = :1 WHERE \"Id\" = 202", responses[15]),
            ("UPDATE \"DAAnalysisSheetData\" SET \"BankPositionInvestmentLoans\" = :1 WHERE \"Id\" = 202", responses[16]),
            ("UPDATE \"DAAnalysisSheetData\" SET \"BankPositionLeasings\" = :1 WHERE \"Id\" = 202", responses[17]),
            ("UPDATE \"DAAnalysisSheetData\" SET \"BankPositionGuarantee\" = :1 WHERE \"Id\" = 202", responses[18]),
            ("UPDATE \"DAAnalysisSheetData\" SET \"BankPositionFactoring\" = :1 WHERE \"Id\" = 202", responses[19]),
            ("UPDATE \"DAAnalysisSheetData\" SET \"FxOpenPosition\" = :1 WHERE \"Id\" = 202", responses[20]),
            ("UPDATE \"DAAnalysisSheetData\" SET \"FinancialBalance\" = :1 WHERE \"Id\" = 202", responses[21]),
            ("UPDATE \"DAAnalysisSheetData\" SET \"FinancialInterim\" = :1 WHERE \"Id\" = 202", responses[22]),
            ("UPDATE \"DAAnalysisSheetData\" SET \"ProjectionPlanningDescription\" = :1 WHERE \"Id\" = 202", responses[23]),
            ("UPDATE \"DAAnalysisSheetData\" SET \"ProjectionOutlookDescription\" = :1 WHERE \"Id\" = 202", responses[24]),
            ("UPDATE \"DAAnalysisSheetData\" SET \"BusinessOther\" = :1 WHERE \"Id\" = 202", table_data)
        ]     
        # Execute update queries in the database
        with my_db.cursor() as cursor:
            for query, response in update_queries:
                cursor.execute(query, [response])
            my_db.commit()        