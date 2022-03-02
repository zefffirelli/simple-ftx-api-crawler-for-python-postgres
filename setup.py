import setuptools

setuptools.setup(
    name="Simple Python Postgres FTX API Crawler",
    version="0.1",
    description="Simple scripts to crawl the FTX API and load results into MySQL",
    url="https://github.com/zefffirelli/simple-python-ftx-api",
    author="@zefffirelli",
    install_requires=["dotenv", "postgres", "psycopg"],
    author_email="",
    packages=setuptools.find_packages(),
    zip_safe=False
)