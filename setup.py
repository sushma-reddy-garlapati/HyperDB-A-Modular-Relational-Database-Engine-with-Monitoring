from setuptools import setup, find_packages

setup(
    name="hyperdb",
    version="0.1.0",
    author="Sushmareddy Garlapati",
    description="A modular relational database engine with buffer management and monitoring",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "prometheus_client",
        "requests",
        "pytest"
    ],
    entry_points={
        "console_scripts": [
            "hyperdb-dashboard=dashboard:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
