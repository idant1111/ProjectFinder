from setuptools import setup, find_packages

setup(
    name='projectfinder',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'click',
        'rich',
        'tqdm',
        'send2trash'
    ],
    entry_points={
        'console_scripts': [
            'projectfinder = projectfinder.cli:cli',
        ],
    },
)
