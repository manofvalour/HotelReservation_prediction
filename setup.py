from setuptools import setup, find_packages
from typing import List


def get_requirements()-> List[str]:
    requirements_list: List[str]= []

    with open ('requirements.txt', 'r') as file:
        requirements= file.readlines()
        
        for req in requirements:
            requirement=req.strip()

            if requirement and requirement!='-e .':
                requirements_list.append(requirement)

    return requirements_list


setup(
    name="Hotel Management tool",
    version='0.0.1',
    author='Emmanuel',
    packages=find_packages(),
    install_requires=get_requirements()

)
        