from setuptools import setup

setup(
    name='code-base',
    version='0.0.1',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    install_requires=open('requirements.txt', encoding='utf-8').readlines(),
)
