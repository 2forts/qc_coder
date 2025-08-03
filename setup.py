from setuptools import setup, find_packages

setup(
    name='qc_coder',
    version='0.1.0',
    author='Francisco Orts',
    author_email='francisco.orts@ual.es',
    description='Método y sistema para codificación eficiente de circuitos cuánticos mediante entrada simbólica',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/tu_usuario/qc_coder',
    packages=find_packages(include=["qc_coder", "qc_coder.*"]),
    install_requires=[
        'qiskit',
        'cirq',
        'amazon-braket-sdk'
    ],
    python_requires='>=3.7',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    include_package_data=True,
    zip_safe=False,
)
