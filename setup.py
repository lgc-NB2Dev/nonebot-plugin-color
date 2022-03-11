import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nonebot-plugin-color",
    version="0.1.0",
    author="monsterxcn",
    author_email="monsterxcn@gmail.com",
    description="A specified color image generator for Nonebot2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/monsterxcn/nonebot-plugin-color",
    project_urls={
        "Bug Tracker": "https://github.com/monsterxcn/nonebot-plugin-color/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=['nonebot-plugin-color'],
    python_requires=">=3.7.3,<4.0",
    install_requires=[
        'nonebot2>=2.0.0a14',
        'nonebot-adapter-onebot>=2.0.0b1'
    ],
)