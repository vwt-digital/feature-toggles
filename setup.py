import os

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    install_requires = f.read().splitlines()

with open('test-requirements.txt') as f:
    test_requires = f.read().splitlines()


setuptools.setup(
    name="featuretoggles",
    version=os.getenv('TAG_NAME', '0.0.0'),
    author='VWT Digital',
    author_email='support@vwt.digital',
    description="A package to configure feature flags and log the use of the toggles",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vwt-digital/feature-toggles",
    install_requires=install_requires,
    test_suite="tests",
    tests_require=test_requires,
    packages=setuptools.find_packages(),
    license='GPLv3+',
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.7',
)
