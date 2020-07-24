import setuptools

with open('README.md') as readme:
    long_description = readme.read()

setuptools.setup(
    name='heimdall-framework',
    version='0.0.1',
    author='Ivan Zlatanov',
    author_email='me@iv.an',
    description='Heimdall Framework is a Python USB threat evaluation framework for Linux that is designed to detect malicious behavior in USB mass storage devices',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Heimdall-Framework/heimdall-framework',
    packages=setuptools.find_packages(where='source.core.python'),
    package_dir={
        '': 'source/core/python/'
    },
    entry_points={
        'console_scripts':[
            'heimdall-framework = main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'   
)