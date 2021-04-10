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
The `BusEMTMad` class allows you to leverage information about buses in the great city of Madrid, which is provided by the EMT (Empresa Municipal de Transportes); this class wrapps the [Block 3 TRANSPORT BUSEMTMAD](https://apidocs.emtmadrid.es/#api-Block_3_TRANSPORT_BUSEMTMAD) section in the official documentation, although not all the functions/webmethods are wrapped.

The following are the functions/webmethods wrapped at the moment:

- **infoLines(dateRef) -** It returns the list of active bus lines in the reference date.
- **infoLine(self, lineId, dateRef) -** It returns detailed info of a specific bus line in the reference date.
- **infoStops -** It returns the list of active bus stops and information about them.
- **infoStop(stopId) -** It returns detailed info of a specific bus stop.
- **lineStops(lineId,direction) -** It returns the list of bus stops of a bus line keeping in mind the direction (1 - start to end, 2 - end to start)
- **issues(lineId) -** It returns details about incidents or issues identified and impacting bus lines.
- **busesArrivals(stopId, lineId="") -** It returns the real time estimation of how far the buses are from the stop and how much time will take them to get to the bus stop. Only buses from the line specified will be considered (*lineId is optional*).

`test_busemtmad.py` let you test this service easily; before you can use it, get your own XClientID and passkey and store them into the `credentials.ini` file. `test_busemtmad.py -h` will give you all the details on how to run it:

```
$ export PYTHONPATH=$PYTHONPATH:`pwd`
$ tests/test_busemtmad.py -h
usage: test_busemtmad.py [-h] [-lid LINEID] [-sid STOPID] [-dir {1,2}]
                         {infoLines,infoLine,infoStops,infoStop,lineStops,issues,busesArrivals} credentialsFile

positional arguments:
  {infoLines,infoLine,infoStops,infoStop,lineStops,issues,busesArrivals}
                        what is going to be requested to the BusEMTMad service
  credentialsFile       path to the file with info to access the service

optional arguments:
  -h, --help            show this help message and exit
  -lid LINEID, --lineId LINEID
                        bus line identifier for actions 'infoLine', 'lineStops' and 'issues'; this argument is optional
                        for action 'busesArrivals'
  -sid STOPID, --stopId STOPID
                        stop identifier for action 'infoStop' and 'busesArrivals'
  -dir {1,2}, --direction {1,2}
                        direction to be considered to analyze line info for action 'linesStops'; 1 for start to end, 2
                        for end to start
```


## BiciMAD Go

## ParkingEMTMad
