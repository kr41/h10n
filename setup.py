import os
from setuptools import setup, find_packages

version = '0.1b1'
here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

setup(
    name='h10n',
    version=version,
    description='Humanization is a Python framework ' \
                'for localization & internationalization',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Internationalization",
        "Topic :: Software Development :: Localization",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: BSD License",
    ],
    keywords='',
    author='Dmitry Vakhrushev',
    author_email='self@kr41.net',
    url='http://code.google.com/p/h10n/',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=True,
    test_suite='nose.collector',
    install_requires=['pyyaml'],
    entry_points="""\
        [h10n.scanner]
        path = h10n.source:scan_path
        asset = h10n.source:scan_asset
        py = h10n.source:scan_py
        [h10n.source.file]
        .yaml = h10n.source:YAMLSource
        .yml = h10n.source:YAMLSource
    """,
)
