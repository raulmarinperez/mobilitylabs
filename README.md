# Python wrapper for the mobilitylabs API
This repo contains a Python library with some classes to easily access the [mobilitylabs API](https://apidocs.emtmadrid.es/) which allows the access to the **BusEMTMad**, **BiciMAD Go** and **ParkingEMTMad** services among other information. These services are part of the [MobilityLabs Madrid](https://mobilitylabs.emtmadrid.es/en) open and interoperable platform.

In addition to the Python wrapper **some test applications are included**; this will help to let you know how to everything works and, on top of that, you can use it to interact with the service once you get your own credencials and store them in the `credentials.ini` file.

The following are the requirements needed to make it work:

- **Python 3** (3.7.3+)
- A **XClientID** and **passkey** in order to use the services; you can get your own XClientID and passkey by following the steps outlined in [Create an application in the EMTing portal](https://mobilitylabs.emtmadrid.es/en/doc/new-app), which is reduced down to:
  1. Creating your own **developer account**
  2. Creating an **EMTing Application**

This Python library has been successfully tested with [OSBDET S21R1](https://github.com/raulmarinperez/osbdet/tree/vs21r1) on a Debian 10 x64 host.

## BusEMTMad

## BiciMAD Go

## ParkingEMTMad
