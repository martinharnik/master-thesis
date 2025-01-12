import oracledb
import contextlib
import fitz
import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from azure.ai.documentintelligence import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence.models import AnalyzeResult

# Load environment variables
load_dotenv()

# Initialize the AzureChatOpenAI client
llm = AzureChatOpenAI(
    default_headers={"id": os.getenv("AZURE_OPENAI_ID")},
    azure_endpoint=os.getenv("AZURE_ENDPOINT"),
    azure_deployment="gpt-4o_deployment0",
    api_version="2024-02-01",
    openai_api_key=os.getenv("AZURE_OPENAI_KEY"),
    max_tokens=4096,
    temperature=0.5,
    )

# Initialize the Azure Document Intelligence client
document_intelligence_client = DocumentAnalysisClient(
    endpoint=os.getenv("AZURE_ENDPOINT"),
    credential=AzureKeyCredential(os.getenv("AZURE_KEY"))
)

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    """
    Extracts all text from a PDF file.

    Args:
        pdf_path (str): The file path to the PDF document.

    Returns:
        list: A list of strings, where each string represents the text content of a page in the PDF.
    """
    with fitz.open(pdf_path) as pdf:
        chunks = []  
        for page in pdf:
            text = page.get_text()
            chunks.append(text)
        return chunks

# Function to get all PDF files in the directory
def get_pdf_files(directory):
    """
    Retrieves all PDF files in a specified directory.

    Args:
        directory (str): The directory path to search for PDF files.

    Returns:
        list: A list of file paths for all PDF files found in the directory.
    """
    return [
        os.path.join(directory, file)
        for file in os.listdir(directory)
        if file.endswith('.pdf')
    ]

def extract_table_data_from_pdf(pdf_path):
    """
    Extracts table data from a PDF using the prebuilt layout model of Azure Document Intelligence.

    Args:
        pdf_path (str): The file path to the PDF document.

    Returns:
        str: HTML string containing all extracted tables.
    """
    # Open the PDF file in binary mode
    with open(pdf_path, "rb") as f:
        # Initiate table extraction using the prebuilt-layout model
        poller = document_intelligence_client.begin_analyze_document(
            "prebuilt-layout",
            analyze_request=f,
            content_type="application/octet-stream"
        )

        # Get the result of the analysis
        result: AnalyzeResult = poller.result()

        # Initialize a list to store HTML representations of the tables
        table_data = []

        # Loop through all tables in the result
        for table in result.tables:
            # Start constructing the HTML for the table
            table_html = "<table>\n"

            # Extract header cells (row index 0)
            header_row = [cell for cell in table.cells if cell.row_index == 0]
            if header_row:
                table_html += "<tr>\n"
                for cell in header_row:
                    table_html += f"<th>{cell.content}</th>\n"
                table_html += "</tr>\n"

            # Extract data rows (all other rows beyond header)
            for row_idx in range(1, table.row_count):
                table_html += "<tr>\n"
                row_cells = [cell for cell in table.cells if cell.row_index == row_idx]
                for cell in row_cells:
                    table_html += f"<td>{cell.content}</td>\n"
                table_html += "</tr>\n"

            # Close the table tag and add spacing for clarity
            table_html += "</table>\n<br>\n"

            # Append the constructed table HTML to the list
            table_data.append(table_html)

        # Join and return all table HTML strings as one consolidated string
        return "".join(table_data)


@contextlib.contextmanager
def database():
    """
    Context manager to handle the setup and teardown of a database connection.

    Yields:
        oracledb.Connection: An Oracle database connection object.
    """
    # Set up the Oracle database client and establish a connection
    oracledb.init_oracle_client()
    db = oracledb.connect(
        user=os.getenv("DB_USER"),  
        password=os.getenv("DB_PASSWORD"), 
        dsn=os.getenv("DB_DSN")  
    )

    # Provide the database connection to the caller
    yield db  

    # Close the database connection after use
    db.close()