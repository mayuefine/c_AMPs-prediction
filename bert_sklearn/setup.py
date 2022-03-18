from setuptools import find_packages, setup

setup(
    name="bert_sklearn",
    version="0.2.0",
    description="A sklearn wrapper for Bert",
    packages=find_packages(exclude=['test', 'scripts', 'examples']),
    install_requires=['torch>=0.4.1',
                       'scikit-learn',
                       'numpy',
                       'pandas',
                       'boto3',
                       'requests',
                       'regex',
                       'pytorch_pretrained_bert==0.6.1',
                       'tqdm'],
    python_requires='>=3.5.0',
)
