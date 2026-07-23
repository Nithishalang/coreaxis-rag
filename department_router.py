from sentence_transformers import SentenceTransformer
import numpy as np
class DepartmentRouter:
    def __init__(self):
        self.model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )
        self.departments = {
            "Human Resources":
            """
            Employees, leave, holidays, attendance,
            recruitment, promotion, appraisal,
            resignation, benefits, payroll,
            employee handbook
            """,
            "Finance":
            """
            Budget, accounting, invoices,
            expenses, procurement, reimbursement,
            payroll, taxes, finance handbook
            """,
            "Software Engineering":
            """
            APIs, backend, frontend,
            coding, Git, Docker,
            Kubernetes, CI/CD,
            software engineering handbook
            """,
            "AI & Machine Learning":
            """
            LLMs, RAG, machine learning,
            neural networks, embeddings,
            computer vision, MLOps,
            AI handbook
            """,
            "Information Security":
            """
            Cybersecurity, CISO,
            security incidents,
            access control,
            encryption,
            compliance,
            security handbook
            """,
            "Information Technology":
            """
            IT support,
            hardware,
            operating systems,
            networking,
            Active Directory,
            VPN,
            servers,
            IT handbook
            """
        }
        self.department_embeddings = {}
        for department, description in self.departments.items():
            self.department_embeddings[department] = self.model.encode(
                description,
                normalize_embeddings=True
            )
    def route(self, query, threshold=0.80):
        query_embedding = self.model.encode(
        query,
        normalize_embeddings=True
    )
        scores = {}
        for department, embedding in self.department_embeddings.items():
            similarity = float(np.dot(query_embedding, embedding))
            scores[department] = similarity
        sorted_departments = sorted(
            scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        selected_departments = [
        department
        for department, score in sorted_departments[:2]
]
        print("\nDepartment Scores")
        print("=" * 40)
        for dept, score in scores.items():
            print(f"{dept:30} {score:.4f}")
        print("\nSelected Departments:", selected_departments)
        return selected_departments, scores
if __name__ == "__main__":
    router = DepartmentRouter()
    while True:
        question = input("\nQuestion: ")
        department, scores = router.route(question)
        print("\nPredicted Department:")
        print(department)
        print("\nScores:")
        for dep, score in scores.items():
            print(f"{dep:<30} {score:.3f}")