from pathlib import Path

from setuptools import find_packages, setup

# Read README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="rp-django-cli",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["Click>=8.0", "GitPython>=3.1", "Jinja2>=3.0"],
    entry_points={
        "console_scripts": [
            "rp=rp.cli:cli",  #  makes 'rp' command available
        ],
    },
    author="Mazharul Islam",
    author_email="tamim.mazharul28@gmail.com",
    maintainer="Mazharul Islam",
    maintainer_email="tamim.mazharul28@gmail.com",
    license="MIT",
    keywords=["django", "cli", "generator", "template", "project-generator"],
    url="https://github.com/mazharulislam4/rp-django-cli",
    description="Rapid Django project generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: Django",
    ],
)
