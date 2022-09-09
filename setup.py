from setuptools import setup, find_packages

setup(
    name="syncbyte",
    version="0.1.0",
    python_requires=">=3.8",
    packages=find_packages(),
    install_requires=[
        "uvicorn",
        "fastapi",
        "pydantic",
        "SQLALchemy",
        "alembic",
        "redis",
        "python-dotenv",
        "psycopg2-binary",
        "celery",
        "boto3"
    ],
    extras_require={
        "dev": [
            "black",
            "pytest",
        ]
    }
)
