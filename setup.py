import setuptools

setuptools.setup(
    name='pymojang',
    version='1.0',
    author='Lucino772',
    author_email='lucapalmi772@gmail.com',
    licence='MIT',
    description='It\'s a full wrapper arround de Mojang API and Mojang Authentication API',
    packages=['mojang'],
    install_requires=['requests','validators']
)