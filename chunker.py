from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.preprocess.metadata import MetadataManager
import re
class Chunker:
    def __init__(self):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=200,
            separators=[
                "\n## ",
                "\n# ",
                "\n\n",
                "\n",
                ". ",
                "; ",
                ", ",
                " ",
                ""
            ]
        )
        self.metadata_manager = MetadataManager()
    def chunk_documents(self, documents):
        all_chunks = []
        for document in documents:
            metadata = self.metadata_manager.enrich_metadata(document)
            sections = re.split(
                r'(?=^\d+(?:\.\d+)*\s)',
                document["text"],
                flags=re.MULTILINE
            )
            chunk_counter = 1
            for section in sections:
                if not section:
                    continue
                section = section.strip()
                if not section:
                    continue
                lines = section.split("\n")
                heading = lines[0].strip()
                chunks = self.splitter.split_text(section)
                for chunk in chunks:
                    if len(chunk.split()) < 30:
                        continue
                    chunk_metadata = metadata.copy()
                    chunk_metadata["chunk_id"] = (
                        f"{metadata['source'].replace('.pdf', '')}"
                        f"_p{metadata['page']}"
                        f"_c{chunk_counter}"
                    )
                    chunk_counter += 1
                    all_chunks.append(
                        {
                            "text": chunk,
                            "metadata": chunk_metadata
                        }
                    )
        return all_chunks