import setuptools


version = '1.0.0'


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="discord-overlay",
    url='https://bashtian.fr/apps/python/discord_overlay',
    version=version,
    author="Bashtian",
    author_email="contact@bashtian.fr",
    description="A Discord PyQT5 app or component to provide discord overlay base on Discord RPC events.",
    license='GNU GENERAL PUBLIC LICENSE 3.0 (GPL v3.0)',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    platforms=[
        'Windows',
        'Linux',
        'OSX'
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: GNU GPL :: GNU GENERAL PUBLIC LICENSE 3.0 (GPL v3.0)",

        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: Implementation :: CPython',

        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries',
    ],
    install_requires=[
        'websocket-client==1.0.0',
        'Click==8.0.1',
        'PyQT5==5.15.4',
        'requests==2.25.1',
    ],
    entry_points='''
        [console_scripts]
        discord-overlay=do.scripts.entrypoint:main
    ''',
)
