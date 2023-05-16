from setuptools import setup, find_packages

setup(
    name = 'snapcli',
    version = '0.1.0',
    url = '',
    description = '',
    packages = find_packages(),
    install_requires = [
        # Github Private Repository
        'ExampleRepo @ git+ssh://git@github.com/example_org/ExampleRepo.git'
    ]
)
