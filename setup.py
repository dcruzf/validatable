import re
from importlib.machinery import SourceFileLoader
from pathlib import Path

from setuptools import setup


def normalize(name):
    return re.sub(r"[-_.]+", "-", name).lower()


THIS_DIR = Path(__file__).resolve().parent
long_description = (THIS_DIR / "README.md").read_text()
version = SourceFileLoader("version", "validatable/version.py").load_module()

setup(
    name="validatable",
    version=version.VERSION,
    description="Validatable provides a single class definition "
    "for SqlAlchemy Table and Pydantic BaseModel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Daniel França",
    author_email="daniel@ci.ufpb.br",
    packages=["validatable"],
    license="MIT",
    python_requires=">=3.6.1",
    install_requires=["pydantic", "sqlalchemy"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Unix",
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet",
    ],
)
