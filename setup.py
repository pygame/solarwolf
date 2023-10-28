from setuptools import setup, find_packages

setup(
    name='solarwolf',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: pygame',
        'Topic :: Games/Entertainment :: Arcade',
    ],
    license='LGPL',
    author='Pete "ShredWheat" Shinners',
    author_email='pete@shinners.org',
    maintainer='Rene Dudfield',
    maintainer_email='renesd@gmail.com',
    description='SolarWolf is an action/arcade game written entirely in Python.',
    include_package_data=True,
    long_description='SolarWolf is an action/arcade game written entirely in Python.',
    package_dir={'solarwolf': 'solarwolf'},
    packages=find_packages(),
    # package_data={'solarwolf': []},
    url='https://github.com/pygame/solarwolf',
    install_requires=['pygame'],
    version='1.6.0',
    entry_points={
        'console_scripts': [
            'solarwolf=solarwolf.cli:main',
        ],
    },
)
