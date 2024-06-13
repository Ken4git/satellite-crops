from setuptools import find_packages
from setuptools import setup

setup(name='satellitecrops',
      version="0.0.1",
      description="Satellite crops project @ Le Wagon",
      license="MIT",
      packages=find_packages(),
      # include_package_data: to install data from MANIFEST.in
      include_package_data=True,
      zip_safe=False)
