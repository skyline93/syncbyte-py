from setuptools import setup, find_packages

setup(
    name="syncbyte",
    version="0.1.0",
    python_requires=">=3.10",
    packages=find_packages(),
    install_requires=[
        "click",
        "uvicorn",
        "fastapi",
        "pydantic",
        "python-dotenv",
        "SQLALchemy>=1.4.42",
        "alembic",
        "asyncpg",
    ],
    extras_require={
        "dev": [
            "black",
            "pytest",
        ]
    },
)
