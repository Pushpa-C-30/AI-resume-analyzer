# ─────────────────────────────────────────────
#  Skill taxonomy & job-role definitions
# ─────────────────────────────────────────────

SKILLS_DB = {
    # Programming languages
    "python", "java", "javascript", "typescript", "c++", "c#", "go", "rust",
    "kotlin", "swift", "ruby", "php", "scala", "r", "matlab", "perl",

    # Web / frontend
    "html", "css", "react", "angular", "vue", "next.js", "nuxt", "svelte",
    "bootstrap", "tailwind", "jquery", "webpack", "vite",

    # Backend / frameworks
    "node.js", "express", "django", "flask", "fastapi", "spring", "laravel",
    "asp.net", "rails", "graphql", "rest", "soap",

    # Databases
    "sql", "mysql", "postgresql", "mongodb", "redis", "sqlite", "oracle",
    "cassandra", "elasticsearch", "dynamodb", "firebase",

    # Cloud & DevOps
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "ansible",
    "jenkins", "github actions", "ci/cd", "linux", "bash", "nginx",

    # Data / ML / AI
    "machine learning", "deep learning", "nlp", "natural language processing",
    "computer vision", "tensorflow", "pytorch", "keras", "scikit-learn",
    "pandas", "numpy", "matplotlib", "seaborn", "tableau", "power bi",
    "spark", "hadoop", "airflow", "mlflow", "huggingface", "openai",
    "llm", "langchain", "bert", "gpt",

    # Mobile
    "android", "ios", "react native", "flutter", "xamarin",

    # Tools / Methodologies
    "git", "github", "gitlab", "jira", "confluence", "agile", "scrum",
    "kanban", "tdd", "bdd", "microservices", "api", "sdk",

    # Soft skills
    "communication", "leadership", "teamwork", "problem solving",
    "critical thinking", "project management", "time management",
}

JOB_ROLES = {
    "Data Scientist": {
        "required": ["python", "machine learning", "deep learning", "nlp",
                     "pandas", "numpy", "scikit-learn", "sql"],
        "preferred": ["tensorflow", "pytorch", "spark", "tableau", "r",
                      "mlflow", "airflow", "bert"],
    },
    "Full Stack Developer": {
        "required": ["javascript", "html", "css", "react", "node.js",
                     "sql", "git", "rest"],
        "preferred": ["typescript", "docker", "aws", "mongodb",
                      "next.js", "graphql", "ci/cd"],
    },
    "Backend Developer": {
        "required": ["python", "java", "sql", "rest", "git", "api"],
        "preferred": ["docker", "kubernetes", "aws", "postgresql",
                      "redis", "django", "flask", "microservices"],
    },
    "Frontend Developer": {
        "required": ["javascript", "html", "css", "react", "git"],
        "preferred": ["typescript", "vue", "angular", "webpack",
                      "tailwind", "next.js", "testing"],
    },
    "DevOps Engineer": {
        "required": ["linux", "docker", "kubernetes", "ci/cd", "git", "bash"],
        "preferred": ["aws", "terraform", "ansible", "jenkins",
                      "prometheus", "kubernetes", "python"],
    },
    "Machine Learning Engineer": {
        "required": ["python", "machine learning", "tensorflow", "pytorch",
                     "scikit-learn", "git"],
        "preferred": ["mlflow", "docker", "aws", "spark", "kubernetes",
                      "huggingface", "langchain", "llm"],
    },
    "Mobile Developer": {
        "required": ["android", "ios", "java", "swift", "kotlin"],
        "preferred": ["react native", "flutter", "firebase", "rest", "git"],
    },
    "Cloud Architect": {
        "required": ["aws", "azure", "gcp", "docker", "kubernetes",
                     "terraform", "ci/cd"],
        "preferred": ["linux", "ansible", "python", "microservices",
                      "networking", "security"],
    },
}

STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "up", "about", "into", "through", "during",
    "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
    "do", "does", "did", "will", "would", "could", "should", "may", "might",
    "shall", "can", "need", "dare", "ought", "used", "able", "i", "me", "my",
    "myself", "we", "our", "you", "your", "he", "she", "it", "they", "them",
    "this", "that", "these", "those", "what", "which", "who", "when", "where",
    "why", "how", "all", "each", "every", "both", "few", "more", "most",
    "other", "some", "such", "no", "not", "only", "same", "so", "than",
    "too", "very", "just", "also", "as", "if", "then", "because", "while",
    "although", "however", "therefore", "thus",
}
