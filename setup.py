from setuptools import setup, find_packages
setup(
    name="egenix-mx-base",
    version="3.2.9",
    description="eGenix mx Base Distribution for Python - mxDateTime, mxTextTools, mxProxy, mxTools, mxBeeBase, mxStack, mxQueue, mxURL, mxUID",
    author = "eGenix.com Software GmbH",
    author_email = "info@egenix.com",
    license = "eGenix.com Public License 1.1.0; Copyright (c) 1997-2000, Marc-Andre Lemburg, All Rights Reserved; Copyright (c) 2000-2015, eGenix.com Software GmbH, All Rights Reserved",
    packages=find_packages(),
    include_package_data=True,
)
