import re
class TextCleaner:
    def clean_text(self, text: str):
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")
        text = text.replace("\t", " ")
        text = re.sub(r"[ ]{2,}", " ", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        text = "\n".join(
            line.rstrip()
            for line in text.splitlines()
        )
        return text.strip()

    def clean_documents(self, documents):
        cleaned_documents = []
        for document in documents:
            cleaned_documents.append({
            "text": self.clean_text(document["text"]),
            "metadata": document["metadata"]
        })
        return cleaned_documents