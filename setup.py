from setuptools import setup, find_packages

setup(
    name="dateling",
    version="1.0.0",
    description=(
        "dateling provides a normalized formal language and grammar for handling relative time expressions. "
        "It includes a DSL (domain-specific language) to represent time anchors, offsets, and modifiers, "
        "along with a robust parser and resolver to evaluate these expressions into concrete dates. "
        "The name 'dateling' comes from combining 'date' and 'handling', reflecting its purpose of handling complex date computations"
    ),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nostaljic/dateling",
    author="jaypyon",
    author_email="scorpion@dgu.ac.kr",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "python-dateutil"
    ],
    python_requires=">=3.11",
)
