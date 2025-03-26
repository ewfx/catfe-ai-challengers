from setuptools import setup, find_packages

setup(
    name="ai_automation_platform",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai",
        "tiktoken",
        "langchain",
        "flask",
        "GitPython",
        "python-dotenv",
        "streamlit",
        "faiss-cpu",
        "unstructured",
        "langchain-community",
        "langchain-openai",
        "uvicorn",
        "fastapi",
        "pydantic",
        "requests"
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered automated testing system",
    keywords="testing, automation, AI, LLM",
    url="https://github.com/Nagarjuna32/GenAI_TestingSystem",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.8",
)
