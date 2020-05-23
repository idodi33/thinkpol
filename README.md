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

## Modules
The `thinkpol` package includes a [client](#the-client), which streams cognition snapshots to a [server](#the-server), which then publishes them to a message queue, where multiple [parsers](#the-parsers) read the snapshot, parse various parts of it, and publish the parsed results, which are then [saved](#the-saver) to a database.
The results are then exposed via a [RESTful API](#the-api), which is consumed by a [CLI](#the-cli); there's also a [GUI](#the-gui), which visualizes the results in various ways.

### The Client
The client reads files and uploads them to a server. The client can either accept and read `binary` files ending with '.mind', or `protobuf` files ending with '.mind.gz'. 

The client is available as `thinkpol.client` and exposes the following API:

```pycon 
>>> from thinkpol.client import upload_sample
>>> upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gz')
… # upload path to host:port
```
   
As well as the following CLI: 

```sh 
python -m thinkpol.client upload-sample \
  -h/--host '127.0.0.1'             \   # '127.0.0.1' is the default host
  -p/--port 8000                    \   # 8000 is the default port
  'snapshot.mind.gz'
```

### The Server
The server accepts connections from clients, receives uploaded samples and publishes them to a publishing function. The default publishing function sends the samples to a message queue (rabbitmq by default).

The server is available as `thinkpol.server` and exposes the following API:

```pycon 
>>> from thinkpol.server import run_server
>>> def print_message(message):
...     print(message)
>>> run_server(host='127.0.0.1', port=8000, publish=print_message)
… # listen on host:port and pass received messages to publish
```
    
As well as the following CLI (the message queue url is of the form `scheme://host:port`):

```sh 
$ python -m thinkpol.server run-server \
  -h/--host '127.0.0.1'          \  # '127.0.0.1' is the default port
  -p/--port 8000                 \  # 8000 is the default port
  'rabbitmq://127.0.0.1:5672/'
```
    
### The Parsers
The parsers consume samples from a message queue, parse it in various ways, and publish back the processed results. 
There are currently parsers for 4 parts of the snapshot: `depth_image`, `color_image`, `pose` and `feelings`. Documentation on how to add new parsers is available [here](#adding-a-new-parser).

The parsers are available as `thinkpol.parsers` and expose the following API:

```pycon
>>> from thinkpol.parsers import run_parser
>>> data = … 
>>> result = run_parser('pose', data)
```

Which accepts a parser name and some raw data, as consumed from the message queue, and returns the result, as published to the message queue. 

The parsers also provide the following CLI:

```sh
$ python -m thinkpol.parsers parse 'pose' 'snapshot.raw' > 'pose.result'
```

Which accepts a parser name and a path to some raw data, as consumed from the message queue, and prints the result, as published to the message queue (optionally redirecting it to a file). This way of invocation runs the parser exactly once.
The CLI also supports running the parser as a service, which works with a message queue indefinitely:

```sh
$ python -m thinkpol.parsers run-parser 'pose' 'rabbitmq://127.0.0.1:5672/'
```

#### Adding a New Parser
In the context of this project, a parser is a function that receives a snapshot and returns an object that is then sent to the message queue. A parser's name must always start with `parse_`, like `parse_color_image`.

In order to add a new parser, place it in a .py file (preferrably named after the parser) and place the file in `thinkpol.parsers`. An automatic framework will collect the parser and integrate it with the rest of the system.


### The Saver
The saver consumes results from the message queue, as published by the parsers, and saves them to a database (mongodb by default).

The saver is available as `thinkpol.saver` and exposes the following API:

```pycon
>>> from thinkpol.saver import Saver
>>> saver = Saver(database_url)
>>> data = …
>>> saver.save('pose', data)
```

As well as the following CLI:

```sh
$ python -m thinkpol.saver save                     \
      -d/--database 'mongodb://127.0.0.1:27017'   \
     'pose'                                       \
     'pose.result' 
```

Which accepts a topic name and a path to some raw data, as consumed from the message queue, and saves it to a database. This way of invocation runs the saver exactly once.
The CLI also supports running the saver as a service, which works with a message queue indefinitely:

```sh
$ python -m thinkpol.saver run-saver  \
      'mongodb://127.0.0.1:27017'   \
      'rabbitmq://127.0.0.1:5672/'
```

### The API
The API reads data from the database and exposes it through a dedicated server.
The API supports the following endpoints:

- **GET /users**
    
    Returns the list of all the supported users, including their `ID`s and `name`s only.
    
- **GET /users/user-id**
    
    Returns the specified user's details: `ID`, `name`, `birthday` and `gender`.

- **GET /users/user-id/snapshots**
    
    Returns the list of the specified user's snapshot IDs and datetimes only.|

- **GET /users/user-id/snapshots/snapshot-id**
    
    Returns the specified snapshot's details: ID, datetime, and the available results' names only (e.g. `pose`).

- **GET /users/user-id/snapshots/snapshot-id/result-name**
    
    Returns the specified snapshot's result in a reasonable format. Supports `pose`, `color-image`, `depth-image` and `feelings`. Anything that has large binary data (so `color_image` and `depth_image`) contains metadata only.

- **GET /users/user-id/snapshots/snapshot-id/result-name/data**
    
    Returns the binary data of result fields that contain that.

The API is available as `thinkpol.api` and exposes the following API:

```pycon
>>> from thinkpol.api import run_api_server
>>> run_api_server(
...     host = '127.0.0.1',
...     port = 5000,
...     database_url = 'mongodb://127.0.0.1:27017',
... )
… # listen on host:port and serve data from database_url
```

As well as the following CLI:

```sh
$ python -m thinkpol.api run-server \
      -h/--host '127.0.0.1'       \     # '127.0.0.1' is the default host
      -p/--port 5000              \     # 5000 is the default port
      -d/--database 'mongodb://127.0.0.1:27017'
```

### The CLI
The CLI reads data from the API server and presents it:

```sh
$ python -m thinkpol.cli get-users
…
$ python -m thinkpol.cli get-user user-id
…
$ python -m thinkpol.cli get-snapshots user-id
…
$ python -m thinkpol.cli get-snapshot user-id snapshot-id
…
$ python -m thinkpol.cli get-result user-id snapshot-id result-name     # e.g. result-name == "pose"
…
```

All commands accept the `-h/--host` and `-p/--port` flags to configure the host and port, but default to the API's address.
The get-result command also accepts the `-s/--save` flag that, if specified, receives a path, and saves the result's data to that path.

### The GUI
The GUI consumes the API and reflects it, using `flask` and `react`.

The GUI is available at `thinkpol.gui` and exposes the following API:

```pycon
>>> from cortex.gui import run_server
>>> run_server(
...     host = '127.0.0.1',
...     port = 8080,
...     api_host = '127.0.0.1',
...     api_port = 5000,
... )
```

As well as the following CLI:

```sh
$ python -m cortex.gui run-server \
      -h/--host '127.0.0.1'       \     # '127.0.0.1' is the default gui host
      -p/--port 8080              \     # 8080 is the default gui port
      -H/--api-host '127.0.0.1'   \     # '127.0.0.1' is the default api host
      -P/--api-port 5000                # 5000 is the default api port
 ```
 
