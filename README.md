# CBLD-EDP

> **NOTICE**: This version has been developed following the NGSI-LD Data Models documentation. 
> For this version, the solution provider made every effort to provide a stable and functional release. 
> No thorough user testing aside from the development team was conducted due to the absence of real linked data context providers. 
> There is warranty, expressed or implied, as to the reliability and stability of the solution. 
> The support team remains available to help on any issue that can be encountered and any feedback is thoroughly appreciated.

CEF Context Broker Linked Data integration with the European Data Portal.

This Integration Solution generates from the parameters established in a
configuration file an RDF/XML file containing the datasets representing
CB-LD Data Models chosen to integrate. The output is available
at the location where the solution is deployed.

The Python module to install contains the following main components:

- Integration Solution core component [`cbld_edp/`](src/cbld_edp/): Command
  line interface (CLI) application that offers the options needed to
  work with the integration.
- Integration Solution API [`cbld_edp/api`](src/cbld_edp/api/): The scope of
  this Flask developed API is to allow the accessing to the data from a
  dataset in the RDF file using a custom call. It also provides
  generated RDF through a static URL in order to have it always
  available on the Internet.

## Getting Started

The following instructions will allow you to get a completely functional
CBLD-EDP environment. This is just a guideline about how to install and
deploy the solution. Adapt it to your needs.

### Prerequisites

CBLD-EDP has some requirements that should be accomplished before starting
deploying it.

- Ubuntu 18.04.1 LTS 64-bit or later
- Python 3.6 or later
- pip3 9.0.1 or later

Update packages list in case you didn't do before (recommended):

```commandline
sudo apt update
```

#### Python 3.7 installation

Python 3 is already installed in Ubuntu 18 distributions. However, in
case you want to use Python 3.7, follow the next steps to install it.

First update packages list and install the prerequisites:

```commandline
sudo apt install software-properties-common
```

Then add the deadsnakes PPA to your sources list:

```commandline
sudo add-apt-repository ppa:deadsnakes/ppa
```

Last, install Python 3.7 with:

```commandline
sudo apt install python3.7
```

You can verify if everything is alright just typing (it should print
Python version number):

```commandline
$ python3.7 --version
Python 3.7.3
```

#### pip3 installation

pip3 will be used as the package manager for Python. It will be used for
CBLD-EDP installation, so must be installed before starting the
deployment.

After packages list update, install pip for Python 3:

```commandline
sudo apt install python3-pip
```

You can verify the installation typing:

```console
$ pip3 --version
pip 9.0.1 from /usr/lib/python3/dist-packages (python 3.7)
```

### Installing and deploying

#### CBLD-EDP core component

To install the Integration Solution, download this repository as a ZIP
file and move it to the machine where you want to deploy it. Once you
got it, install it using pip:

```commandline
sudo pip3 install /path/to/cbld_edp.zip
```

It should have installed too every dependency (Click, configobj, Flask,
Gunicorn, requests and time-uuid) of the CBLD-EDP. In case it didn't or
you aren't sure of it, install them directly using
[`requirements.txt`](requirements.txt) file. First unzip it cause it's
on downloaded ZIP file:

```commandline
unzip /path/to/cb_edp.zip
pip3 install -r /path/to/requirements.txt
```

You can check it's installed launching `show` pip3 command:

```commandline
$ pip3 show cbld-edp
---
Metadata-Version: 1.0
Name: cbld-edp
Version: 1.0
Summary: FIWARE Context Broker instance integration with the EDP
Home-page: https://github.com/ConnectingEurope/Context-Broker-EDP-LD
Location: /usr/local/lib/python3.7/dist-packages
Requires: Click, configobj, Flask, gunicorn, requests, time-uuid
Classifiers:
Entry-points:
  [console_scripts]
  cbld-edp=cbld_edp.commands:cli
```

#### CBLD-EDP API

The Integration Solution includes an API for:

1. Doing requests to the CB configured in order to get responses from
   browsable HTTP requests
2. Publishing the RDF/XML file generated for harvesting by the EDP

The deployment of this API will need something serving the solution and
other thing that grants access to this server from the Internet. The
technologies suggested to do so are
[Gunicorn](https://github.com/benoitc/gunicorn) and
[Nginx](http://nginx.org/).

##### Gunicorn

Gunicorn should be installed by pip when installing CBLD-EDP. If not,
please launch:

```commandline
sudo pip3 install gunicorn==19.9.0
```

Install required components:

```commandline
sudo apt-get install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
```

Create a service to assign Gunicorn to it with `nano` (or any other
editor you like):

```commandline
sudo nano /etc/systemd/system/cbld-edp.service
```

And paste the following contents replacing the values:

- `{sudoer-user}` for machine’s sudoer user. It is root by default.
- `{user-group}` for a group from the user specified before. You can
  check it using ll command with “Location” value copied before to see
  which groups have the other files and directories. It is staff by
  default.
- `{solution-location}` for "Location" value copied before.

```text
[Unit]
Description=Gunicorn instance to serve CBLD-EDP
After=network.target

[Service]
User={sudoer_user}
Group={user_group}
WorkingDirectory={solution-location}/cb_edp/api
ExecStart=/usr/local/bin/gunicorn --worker-class gthread --workers 3 --threads 1 --bind unix:cbld-edp.sock -m 704 wsgi:app

[Install]
WantedBy=multi-user.target
```

Gunicorn accepts custom configuration for number of workers and threads
that these workers will use. The values set in the text above are the
recommended ones, but can be modified following these equations:

```math
N.workers=2*CPU cores+1
```

```math
N.threads=2*CPU cores
```

Now Gunicorn service can be started:

```commandline
sudo systemctl start cbld-edp
```

To enable Gunicorn launching on boot, launch this command:

```commandline
sudo systemctl enable cbld-edp
```

You can check application service status executing:

```commandline
sudo systemctl status cbld-edp
```

###### Nginx

Install Nginx for Ubuntu:

```commandline
sudo apt-get install nginx
```

You can check Nginx service status running:

```commandline
sudo systemctl status nginx
```

Now it's turn to configure Nginx to proxy requests to the API. To do so
create new server block configuration for the already created Gunicorn
service with `nano` (or any other editor you like):

```commandline
sudo nano /etc/nginx/sites-available/cbld-edp
```

And paste the following contents replacing the values:

- `{your-public-ip-or-dns}` for the public IP of the server or the DNS.
- `{your-custom-route}` for the relative path where the API service will
  be available. It accepts any value (context-data, open-data, cb, etc.)
  and many levels (as many as the Integration Admin wants) but always
  has to include the /api text at the end. Some valid examples:
  - /context-data/api
  - /open-data/cb/catalogue/api
  - /api
- `{solution-location}` for "Location" value copied before.

```text
server {
    listen 80;
    server_name {your-public-ip-or-dns};

    location /{your-custom-route}/api {
        include proxy_params;
        proxy_pass http://unix:{solution-location}/cbld_edp/api/cbld-edp.sock;
    }
}
```

Link the file to the sites-enabled directory to enable Nginx server
block configuration:

```commandline
sudo ln -s /etc/nginx/sites-available/cbld-edp /etc/nginx/sites-enabled
```

Check that there are no errors:

```commandline
sudo nginx -t
```

If it returns no issues, then restart Nginx to load the new
configuration:

```commandline
sudo systemctl restart nginx
```

Now the application should be available on the Internet. Try browsing to
http://`{your-public-ip-or-dns}`/`{your-custom-route}`/api/status

## Built With

- [Python 3.7](https://www.python.org/)
- [Flask](http://flask.pocoo.org/)

## License

This project is licensed under the European Union Public License 1.2
-see the [LICENSE](LICENSE) file for details.

## Contributors

The Context Broker Data Visualisation enabler has been carried out by:

- [CEF Digital](https://ec.europa.eu/cefdigital/wiki/display/CEFDIGITAL/CEF+Digital+Home)
- [everis](https://www.everis.com/)
- [FIWARE](https://www.fiware.org/)
