from setuptools import setup, find_packages

setup(
    name='perflame',
    version='0.0.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    author='shi0rik0',
    description='Profile with Linux perf and draw flame graphs',
    install_requires=['setuptools'],
    entry_points={
        'console_scripts': [
            'perflame = perflame:main'
        ]
    },
    package_data={
        'perflame': ['FlameGraph/**']
    },
)
