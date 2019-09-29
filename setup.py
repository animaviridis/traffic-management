import setuptools


setuptools.setup(
    name="traffic_management",
    version="0.0.1",
    author="Dominika Dlugosz",
    author_email="dominika.a.m.dlugosz@gmail.com",
    description="Traffic management system - 'Foundations of AI' class assignment",
    url="https://github.com/animaviridis/traffic-management",
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=['numpy>=1.17.2', 'pyddl']
)
