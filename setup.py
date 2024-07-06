from numpy.distutils.core import setup

package_data = {
    'Shor-Algorithm': [
        'shor/*',
    ]
}

setup(
    name='Shor-Algorithm',
    python_requires='>=3.7',
    version="0.1",
    packages=['shor'],
    package_data=package_data,
    scripts=['bin/shors_algorithm'],
    description="Shor-Algorithm",
    author="Vinicius L Bilck",
    author_email="bilck.vinicius1998@gmail.com",
    url='https://github.com/ViniBilck/Shor-Algorithm',
    platform='Linux',
    license="MIT License",
    classifiers=['Programming Language :: Python :: 3.7'],
)