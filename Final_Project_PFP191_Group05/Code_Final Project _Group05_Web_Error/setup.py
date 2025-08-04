"""
Setup script for Campus Event Management System
"""

from setuptools import setup, find_packages

setup(
    name="campus-event-management",
    version="1.0.0",
    description="Campus Event Management System with Role-based Access Control",
    author="Campus Event Management Team",
    author_email="admin@campus.edu",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Flask==2.3.3',
        'Werkzeug==2.3.7',
        'Jinja2==3.1.2',
        'MarkupSafe==2.1.3',
        'itsdangerous==2.1.2',
        'click==8.1.7',
        'blinker==1.6.3'
    ],
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    entry_points={
        'console_scripts': [
            'campus-events=run:main',
        ],
    },
)