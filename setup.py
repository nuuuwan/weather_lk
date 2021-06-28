'''Setup.'''

import time
import setuptools

DIST_NAME = 'weather_lk'
with open('README.md', 'r') as fh:
    long_description = fh.read()

IS_RELEASE = False
MAJOR, MINOR, PATCH = 1, 0, 0
if IS_RELEASE:
    version = '%d.%d.%d' % (MAJOR, MINOR, PATCH)
else:
    # PRE-RELEASE
    ts = time.strftime('%Y%m%d%H%M%S0000', time.localtime())
    version = '%d.%d.%d.%s' % (MAJOR, MINOR, PATCH, ts)

setuptools.setup(
    name='%s-nuuuwan' % DIST_NAME,
    version=version,
    author='Nuwan I. Senaratna',
    author_email='nuuuwan@gmail.com',
    description='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nuuuwan/%s' % DIST_NAME,
    project_urls={
        'Bug Tracker': 'https://github.com/nuuuwan/%s/issues' % DIST_NAME,
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    python_requires='>=3.6',

    install_requires=[
        'bs4',
        'selenium',
        'tweepy',
        'utils-nuuuwan',
    ],
)
