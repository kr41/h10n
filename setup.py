from setuptools import setup, find_packages

version = '0.1dev'

setup(
    name='h10n',
    version=version,
    description="",
    long_description="""""",
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Dmitry Vakhrushev',
    author_email='self@kr41.net',
    url='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    test_suite='nose.collector',
    install_requires=[],
)
