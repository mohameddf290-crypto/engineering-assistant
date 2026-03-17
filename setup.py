from setuptools import setup, find_packages

setup(
    name="engineering-assistant",
    version="0.1.0",
    description="Engineering Assistant — Music Production AI. Every brain built from scratch.",
    author="mohameddf290-crypto",
    packages=find_packages(exclude=["tests*"]),
    python_requires=">=3.9",
    install_requires=[
        "essentia",
        "numpy",
        "scipy",
        "librosa",
        "fastapi",
        "uvicorn",
        "pydantic",
        "torch",
    ],
    extras_require={
        "dev": [
            "pytest",
        ],
    },
)
