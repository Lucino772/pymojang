import setuptools

with open('./README.md', 'r') as fp:
    long_description = fp.read()

setuptools.setup(
    name='pymojang',
    version='1.3.1',
    author='Lucino772',
    author_email='lucapalmi772@gmail.com',
    licence='MIT',
    url='https://github.com/Lucino772/pymojang',
    description='It\'s a full wrapper arround the \
         Mojang API and Mojang Authentication API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9"
    ],
    packages=setuptools.find_packages(),
    install_requires=['requests', 'validators', 'pyjwt[crypto]', 'msal'],
    keywords=['minecraft', 'mojang', 'python3'],
    project_urls={
        'Documentation': 'https://pymojang.readthedocs.io/en/latest/'
    }
)
