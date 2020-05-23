[![Build Status](https://travis-ci.org/idodi33/Thinkpol.svg?branch=master)](https://travis-ci.org/idodi33/Thinkpol) [![Documentation Status](https://readthedocs.org/projects/thinkpol/badge/?version=latest)](https://thinkpol.readthedocs.io/en/latest/?badge=latest)
# Thinkpol

My final project in the course 'Advanced System Design'. See [full documentation](https://thinkpol.readthedocs.io/en/latest/?).

## Installation

1. Clone the repository and enter it:

    ```sh
    $ git clone git@github.com:idodi33/Thinkpol.git
    ...
    $ cd Thinkpol/
    ```

2. Run the installation script and activate the virtual environment:

    ```sh
    $ ./scripts/install.sh
    ...
    $ source .env/bin/activate
    [Thinkpol] $ # you're good to go!
    ```

3. Make sure you've installed `docker` and `docker-compose`.

4. To check that everything is working as expected, run a docker of rabbitmq and mongo, and finally run the tests:

    ```sh
    $ sudo docker run -d -p 5672:5672 rabbitmq
    ...
    $ sudo docker run -d -p 27017:27017 mongodb
    ...
    $ pytest tests/
    ...
    ```

## Usage
The basic functionality of `thinkpol` can be acheived through the `scripts/run-pipeline.sh` script. This launches all of the project's components and allows you to upload a file using a client and view its contents by browsing to a gui server.

First, run the script:

    ```sh
    $ cd ./scripts
    $ ./run-pipeline.sh
    ... # this might take a little while
    ```

Now you can [run a client](#the-client) and browse through the data on http://127.0.0.1:8080. 



The 'Thinkpol' package provides 3 functions that can be called with 'python -m': *upload_thought*, which uploads a thought to the thoughts directory; *run_server*, which runs a server which recieves the thoughts; and *run_webserver*, which displays all thoughts in a webpage.

```sh
(from the directory that contains 'thinkpol')
$ python -m thinkpol upload_thought '127.0.0.1:8000' 1 Hi
* Thinkpol uploads 'Hi' to user-1's directory in the current time subdirectory. Sends the data to 127.0.0.1:8000. *
$ python -m thinkpol run_server '127.0.0.1:8000' /data
* Thinkpol recieves data from 127.0.0.1:8000 and stores it in /data. *
$ python -m thinkpol run_webserver '127.0.0.1:5000' /data
* Thinkpol displays thoughts from the /data directory in 127.0.0.1:8000. *
```

## Modules
The `thinkpol` package includes a [client](#the-client), which streams cognition snapshots to a [server](#the-server), which then publishes them to a message queue, where multiple [parsers](#the-parsers) read the snapshot, parse various parts of it, and publish the parsed results, which are then [saved](#the-saver) to a database.
The results are then exposed via a [RESTful API](#the-api), which is consumed by a [CLI](#the-cli); there's also a [GUI](#the-gui), which visualizes the results in various ways.

### The Client
The client reads files and uploads them to a server. The client can either accept and [read](#the-reader) a `binary` file ending with '.mind', or a `protobuf` file ending with '.mind.gz'. 

The client is available as `thinkpol.client` and exposes the following API:

```pycon 
>>> from cortex.client import upload_sample
>>> upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz')
… # upload path to host:port
```
   
As well as the following CLI: 

```sh 
python -m cortex.client upload-sample \
  -h/--host '127.0.0.1'             \   # '127.0.0.1' is the default host
  -p/--port 8000                    \   # 8000 is the default port
  'snapshot.mind.gz'
```

### The Server
The server accepts connections from clients, receives uploaded samples and publishes them to a publishing function. The default publishing function sends the samples to a message queue.

The server is available as `thinkpol.server` and exposes the following API:

```pycon 
>>> from cortex.server import run_server
>>> def print_message(message):
...     print(message)
>>> run_server(host='127.0.0.1', port=8000, publish=print_message)
… # listen on host:port and pass received messages to publish
```
    
The server also exposes the following CLI (the message queue url is of the form `scheme://host:port`):

```sh 
$ python -m cortex.server run-server \
  -h/--host '127.0.0.1'          \  # '127.0.0.1' is the default port
  -p/--port 8000                 \  # 8000 is the default port
  'rabbitmq://127.0.0.1:5672/'
```
    
### The Parsers
The parsers consume samples from a message queue, parse it in various ways, and publish back the processed results. 
There are currently parsers for 4 parts of the snapshot: `depth_image`, `color_image`, `pose` and `feelings`. Documentation on how to add new parsers is available [here](#adding-new-parser).

The parsers are available in `thinkpol.parsers` and expose the following API:

```pycon
>>> from cortex.parsers import run_parser
>>> data = … 
>>> result = run_parser('pose', data)
```
    
