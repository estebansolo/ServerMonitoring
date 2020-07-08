# :bar_chart: Server Monitoring

This is the first part of a personal project to track server information and send this data to a backend to constantly monitor it.

## Install

This Script is designed to be executed using a Cron, however before performing the configuration it is necessary to install the required libraries on the server.

```
python3 -m pip install -r requirements.txt
```

The above command will install the libraries included in the **requirements.txt** file, those libraries that the tracker will need to work.

## Configuration

This project must be in the server you want to track.

You need to configure the settings in the `.env` file, this file does not exist, however you have as a template **dotenv**.

### Environment

- `NAME`: In case you want to track multiple servers, you can use this variable to distinguish them. By default **server1**
- `DISKS`: Types of disks we don't want to include in the response. By default is empty
- `ATTEMPS`: Number of attempts before raising an exception in case of not being able to receive a successful response from the url. By default **3**
- `URI`: POST URL to send the information collected from the server. By default **http://localhost/**

### Crontab

Set up a cron via `crontab -e`

```
* * * * * python3 /path/to/app.py > /tmp/monitoring_log.txt 2>&1
```

This tool will be executed every minute.

## Usage

```
Usage: app.py [-h] [--debug] [--no-debug]

optional arguments:
  -h, --help  show this help message and exit
  --debug
  --no-debug
```

`--debug` will print the server information without sending to the server. By default `--no-debug` is selected.

## Changelog

* 1.0.0 Initial release. Send server data
