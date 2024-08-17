from setuptools import setup, find_packages

setup(
    name='projectfinder',
    version='0.1',
    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
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
