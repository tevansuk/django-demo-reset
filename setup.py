from setuptools import setup, find_packages

setup(name='django-demo-reset',
    version='0.1-alpha',
    author='Tom Evans',
    author_email='tevans.uk@googlemail.com',
    packages=find_packages(),
    long_description='App which resets model\'s dates relative to a previous demo date',)

