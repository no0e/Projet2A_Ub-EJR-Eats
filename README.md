# Project Context 
The EJR’s famed galette-saucisse has become the most sought-after delicacy in all of
Rennes. To meet the growing demand, EJR has now a 
application to manage both orders and deliveries.

This project Python-based application in the form of a api
streamlines the ordering and delivery process for EJR while providing a authentication system tailored to three distinct user types.Customer , Delivery Drivers and Administrator.

Every user types run the app the same way.

### PDM package in required.

## Install PDM with pip 

> pip install --user pdm

Check your PDM version with 

> pdm --version

Optionally, use uv "under the hood" for faster installation: 

> pip install --user uv
> pdm config use_uv true

## Note for Onyxia/k8s users

The installation can be handled by the setup script `init_project.sh`.

You can provide that configuration file as a custom initialization script for your vscode image. 

Be sure to provide the ports used by the app in the `Network access` configuration. For example, this app uses the `8000` port.

# Application Features


# How to install the app 

> pdm install


# How to run the app 

> pdm start

This starts a server accessible on `localhost:8000`.

The API is then documented on `localhost:8000/docs`.

# How to reset the databases (both production and testing)

>pdm reset

# How to populate the database for testing or production

- For the main database:

> pdm run filldatabase

- For the test database:

> pdm run filldatabase test

