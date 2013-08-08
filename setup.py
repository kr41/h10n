import os
from setuptools import setup


version = '0.2b1'
here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

setup(
    name='h10n',
    version=version,
    description='Humanization: i18n & l10n framework',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Internationalization",
        "Topic :: Software Development :: Localization",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: BSD License",
    ],
    keywords='',
    author='Dmitry Vakhrushev',
    author_email='self@kr41.net',
    url='https://bitbucket.org/kr41/h10n',
    download_url='https://bitbucket.org/kr41/h10n/downloads',
    packages=['h10n'],
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
