# DEVGRID Challenge

## Development environment with Docker

### Install Docker 

Just select your OS and download [here](https://www.docker.com/products/docker-desktop)

### Build and run the container application

> Run this commands os the base path of this project

If you in an UNIX based OS, just type:

```
$ docker build --platform linux/amd64 -t devgrid-challenge .
$ docker run --platform linux/amd64 -d -p 8081:8080 -v $(pwd):/app devgrid-challenge
```

If you in a Windows OS `PowerShell`, then type:

```
$ docker build --platform linux/amd64 -t devgrid-challenge .
$ docker run --platform linux/amd64 -d -p 8081:8080 -v ${PWD}:/app devgrid-challenge
```

Or if you using Windows with `CMD`, type:

```
$ docker build --platform linux/amd64 -t devgrid-challenge .
$ docker run --platform linux/amd64 -d -p 8081:8080 -v %cd%:/app devgrid-challenge
```

Now just access [http://localhost:8081](http://localhost:8081)

## Standalone Test

If you looking for run the test on your host, set your virtual environment, install dependencies on `requirements.txt` and run:

```
$ pytest test_main.py
```
