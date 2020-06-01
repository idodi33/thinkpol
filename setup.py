from setuptools import setup, find_packages


setup(
    name = 'thinkpol',
    version = '1.0.0',
    author = 'Ido Bar-Sella',
    description = 'My final project in the course \'Advanced System Design\'.',
    packages = find_packages(),
    install_requires = ['click', 'flask', 'furl', 'pymongo', 'flask_cors', 'requests',
    'werkzeug.routing', 'bson.json_util', 'pika', 'PIL', 'matplotlib.pyplot', 'numpy'],
    tests_require = ['pytest', 'pytest-cov'],
)
