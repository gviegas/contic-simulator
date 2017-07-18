# Contic Simulator

The Contic Simulator is used to issue commands to a [Contic OSGPb](https://github.com/gviegas/contic-osgpb) network and send the
collected data to the [Contic Server](https://github.com/gviegas/contic-server).

A local communication is made with a Contic OSGPb Data Concentrator using named pipes. Preconfigured commands are issued through the Data Concentrator, which send requests to the Units on the network. The Simulator reads the responses received by the Data Concentrator and send them to be stored on the Contic Server.

## Run

To run the application, just execute the [simulator.py](script/simulator.py) script ([Python 3](https://www.python.org/) must be installed).

## License

This project is under the terms of the [MIT License](LICENSE.md).

