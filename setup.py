from setuptools import setup, find_packages


tests_deps = [
    "tox",
    "pytest"
]

setup(
    name="mybar",
    version="0.0.1",
    description="CLI app to manage your bar.",
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"mybar": ["resources/*.json"]},
    url="https://github.com/Suenweek/mybar",
    author="Suenweek",
    install_requires=[
        "click",
        "attrs",
        "sqlalchemy",
        "appdirs"
    ],
    tests_require=tests_deps,
    extras_require={
        "test": tests_deps
    },
    entry_points={
        "console_scripts": [
            "mybar = mybar.cli:main"
        ]
    }
)
