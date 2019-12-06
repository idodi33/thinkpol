# Thinkpol
My final project in the course 'Advanced System Design'.
Full documentation here: 

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

3. To check that everything is working as expected, run the tests:


    ```sh
    $ pytest tests/
    ...
    ```

## Usage
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
