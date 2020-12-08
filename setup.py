import requests
import setuptools


with open('README.md') as readme:
    long_description = readme.read()

def get_leatest_version():
    return requests.get("https://tx58wj5h27.execute-api.eu-central-1.amazonaws.com/dev/get_latest_version").json()['version']

setuptools.setup(
    name='heimdall_framework',
    version=get_leatest_version(),
    author='Ivan Zlatanov',
    author_email='i_zlatanpv@protonmail.com',
    description='Heimdall Framework is a Python USB threat evaluation framework for Linux that is designed to detect malicious behavior in USB mass storage devices',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Heimdall-Framework/heimdall-framework',
    package_dir={
        'heimdall_framework': 'heimdall_framework',
        'heimdall_framework.modules': 'heimdall_framework/modules'
    },
    packages=setuptools.find_packages(),
    entry_points={  
        'console_scripts':[
            'heimdall_framework = heimdall_framework.main:run',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)