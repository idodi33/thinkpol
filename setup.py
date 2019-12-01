from setuptools import setup, find_packages


setup(
    name = 'thinkpol',
    version = '0.1.0',
    author = 'Ido Bar-Sella',
    description = 'My final project in the course \'Advanced System Design\'.',
    packages = find_packages(),
    install_requires = ['click', 'flask'],
    tests_require = ['pytest', 'pytest-cov'],
)
