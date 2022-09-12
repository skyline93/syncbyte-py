from setuptools import setup, find_packages

setup(
    name="syncbyte",
    version="0.1.0",
    python_requires=">=3.8",
    packages=find_packages(),
    package_data={"syncbyte": ["alembic.ini"]},
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
        "boto3",
        "eventlet",
    ],
    extras_require={
        "dev": [
            "black",
            "pytest",
            "wheel",
            "twine",
            "pip-tools",
        ]
    },
    entry_points={
        'console_scripts': [
            'syncbyte = syncbyte.__main__:cli',
        ]
    },
)
