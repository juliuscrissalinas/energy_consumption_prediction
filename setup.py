from setuptools import find_packages, setup

setup(
    name="ec_prediction",
    packages=find_packages(exclude=["ec_prediction_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
