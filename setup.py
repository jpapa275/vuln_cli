from setuptools import setup, find_packages

setup(
    name='vuln_cli',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'pandas',
        'requests',
        'tabulate',
        'PyYaml'
    ],
    entry_points={
        'console_scripts': [
            'vuln_cli = vuln_cli:cli',
        ],
    },
)