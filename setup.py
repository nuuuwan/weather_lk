import time

import setuptools

DIST_NAME = 'weather_lk'
with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = []
with open('requirements.txt') as fin:
    for line in fin.readlines():
        requirements.append(line.strip())

IS_PRE_RELEASE = True
MAJOR, MINOR, PATCH = 1, 0, 0
if IS_PRE_RELEASE:
    ts = time.strftime('%Y%m%d%H%M%S0000', time.localtime())
    version = '%d.%d.%d.%s' % (MAJOR, MINOR, PATCH, ts)
else:
    version = '%d.%d.%d' % (MAJOR, MINOR, PATCH)

setuptools.setup(
    name="%s-nuuuwan" % DIST_NAME,
    version=version,
    author="Nuwan I. Senaratna",
    author_email="nuuuwan@gmail.com",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nuuuwan/%s" % DIST_NAME,
    project_urls={
        "Bug Tracker": "https://github.com/nuuuwan/%s/issues" % DIST_NAME,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        'camelot-py[cv]',
        'infographics-nuuuwan==1.0.8',
        'matplotlib',
        'numpy',
        'selenium',
        'tweepy==3.10.0',
        'utils-nuuuwan',
    ],
    test_suite='nose.collector',
    tests_require=['nose'],
)
