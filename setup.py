from setuptools import (
    setup,
    find_packages,
)


def get_requirements(filenames):
    r_total = []
    for filename in filenames:
        with open(filename) as f:
            r_local = f.read().splitlines()
            r_total.extend(r_local)
    return r_total


setup(
    name='mmi_kit',
    version='0.24.3',
    python_requires=">=3.6",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Nicolay Rusnachenko',
    author_email='rusnicolay@gmail.com',
    license='MIT License',
    packages=find_packages(),
    install_requires=get_requirements(['dependencies.txt'])
)