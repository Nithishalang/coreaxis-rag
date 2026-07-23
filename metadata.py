import re
class MetadataManager:
    def __init__(self):
        self.department_mapping = {
            "employee_handbook.pdf": {
                "department": "Human Resources",
                "document_type": "Employee Handbook"
            },
            "finance_handbook.pdf": {
                "department": "Finance",
                "document_type": "Finance Department Handbook"
            },
            "engineering_handbook.pdf": {
                "department": "Software Engineering",
                "document_type": "Software Engineering Department Handbook"
            },
            "ai_ml_handbook.pdf": {
                "department": "AI & Machine Learning",
                "document_type": "AI & Machine Learning Department Handbook"
            },
            "information_security_handbook.pdf": {
                "department": "Information Security",
                "document_type": "Information Security Department Handbook"
            },
            "it_handbook.pdf": {
                "department": "Information Technology",
                "document_type": "Information Technology Department Handbook"
            }
        }
    def extract_section(self, text):
        match = re.search(
            r'^\d+(\.\d+)*',
            text,
            re.MULTILINE
        )
        if match:
            return match.group()
        return "Unknown"
    def extract_heading(self, text):
        lines = text.strip().split("\n")
        if not lines:
            return "Unknown"
        first_line = lines[0].strip()
        if len(first_line) > 150:
            return "Unknown"
        return first_line
    def enrich_metadata(self, document):
        metadata = document["metadata"].copy()
        filename = metadata["source"]
        metadata.update(
            self.department_mapping.get(
                filename,
                {
                    "department": "Unknown",
                    "document_type": "Unknown"
                }
            )
        )
        metadata["section"] = self.extract_section(
            document["text"]
        )
        metadata["heading"] = self.extract_heading(
            document["text"]
        )
        return metadata