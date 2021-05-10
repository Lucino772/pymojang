import setuptools

with open('./README.md','r') as fp:
    long_description = fp.read()

setuptools.setup(
    name='pymojang',
    version='1.2.0',
    author='Lucino772',
    author_email='lucapalmi772@gmail.com',
    licence='MIT',
    url='https://github.com/Lucino772/pymojang',
    description='It\'s a full wrapper arround de Mojang API and Mojang Authentication API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    install_requires=['requests','validators'],
    keywords=['minecraft','mojang','python3'],
    project_urls={
        'Source': 'https://github.com/Lucino772/pymojang',
        'Documentation': 'https://pymojang.readthedocs.io/en/latest/'
    }
)