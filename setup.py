from setuptools import setup, find_packages

setup(
    name="LabelBoxDatasets",
    version="0.1",
    packages=find_packages(),
    description='Manages Datasets from a GCP source for Labelbox',
    install_requires=[
        'labelbox',
        'google',
        'uuid'
    ],
)