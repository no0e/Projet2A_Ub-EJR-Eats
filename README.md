# Project Context

The EJR’s famed galette-saucisse has become the most sought-after delicacy in Rennes. To meet the growing demand, EJR has developed a Python-based API application to manage both orders and deliveries. This application streamlines the entire process while providing a secure authentication system tailored to three distinct user types: Customer, Delivery Driver, and Administrator. Each user interacts with the application in a consistent manner, regardless of their role.

### PDM package is required.

## Install PDM with pip

> pip install --user pdm

Check your PDM version with

> pdm --version

Optionally, use uv for faster installation:

> pip install --user uv
> pdm config use_uv true

## Note for Onyxia/k8s users

The setup script `init_project.sh` can handle the installation automatically. This script can be provided as a custom initialization script for your VSCode image. Make sure to expose the correct port (`8000`) in the `Network access` configuration to allow the application to run properly.

# Application Features

The application offers a comprehensive set of features divided by user type. At the core is a secure authentication system that supports login, logout, and session management to ensure secure access. All users can manage their profiles, updating personal information and preferences as needed.

Customers can manage their profiles and delivery addresses, browse the menu, and handle their shopping cart by adding or removing items. They can place orders, select delivery options, and confirm payment, all within the app. 

Delivery drivers have tools to manage their profiles and availability, view delivery queues, and receive order assignments. They can accept or reject deliveries and use integrated navigation features to follow optimized routes for timely delivery. 

Administrators oversee the platform by managing user accounts, including creation, editing, and deletion. They also maintain the menu, adding or removing items and updating availability to ensure smooth operations.

# How to install the app

Installation is straightforward with PDM:

> pdm install

# How to run the app

Start the application with:

> pdm start

The server will run on `localhost:8000`, and the API documentation can be accessed at `localhost:8000/docs`.

# Database Management

## To reset the databases

> pdm reset

## To populate the database

> pdm run filldatabase

For the test database:

> pdm run filldatabase test

# To try every features here are an admin's credentials

Username : aliceasm

Password : hardpwd123