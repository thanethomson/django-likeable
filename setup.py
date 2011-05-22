#
# django-likeable
#
# See LICENSE for licensing details.
#

from setuptools import setup, find_packages


setup(
    name='django-likeable',
    version='0.0.1',
    description='Simple Django app to facilitate "liking" of any content type.',
    long_description=open('README.rst', 'rt').read(),
    author='Thane Thomson',
    author_email='connect@thanethomson.com',
    license='Apache',
    url='https://github.com/thanethomson/django-likeable',
    packages=find_packages(),
    include_package_data=True,
    classifiers = [
        'Programming Language :: Python',
        'License :: OSI Approved :: BSD License',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    zip_safe=False,
)

