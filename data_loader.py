from google import genai
from llama_index.readers.file import PDFReader
from llama_index.core.node_parser import SentenceSplitter

EMBED_DIM = 3072
GOOGLE_API_KEY = "AIzaSyDvNxeCTJEtiAzlcVqYw07GaXq_TcmQi_w"

splitter = SentenceSplitter(chunk_size=1000, chunk_overlap=200)


def load_and_chunk_pdf(path: str):
    docs = PDFReader().load_data(file=path)
    text = [d.text for d in docs if getattr(d, "text", None)]
    chunks = []
    for t in text:
        chunks.extend(splitter.split_text(t))
    return chunks


def embed_texts(texts: list[str]) -> list[list[float]]:
    client = genai.Client(api_key=GOOGLE_API_KEY)  # default v1beta, required for embed
    embeddings = []
    for t in texts:
        response = client.models.embed_content(
            model="models/gemini-embedding-001",  # ✅ correct model with prefix
            contents=t
        )
        embeddings.append(response.embeddings[0].values)
    return embeddings