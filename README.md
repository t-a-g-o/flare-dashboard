<div align="center">
    </a>
    <br />
    <img align="center" src="https://cdn.tago.works/apps/flare/img/webdash.png">
    
   ![GitHub last commit](https://img.shields.io/github/last-commit/t-a-g-o/flare-webapp)
   ![GitHub issues](https://img.shields.io/github/issues-raw/t-a-g-o/flare-webapp)
   ![GitHub](https://img.shields.io/github/license/t-a-g-o/flare-webapp)

   **VERSION 1.0**
    
</div>

> This Web dashboard makes it eaiser to configure [Flare](https://github.com/tagoworks/flare), and look at different statistic and data about Flare.


# Getting Started
### Clone and setup the web files
1. CD into the Flare main directory
2. Clone the repository:
   ```shell
   sudo git clone https://github.com/t-a-g-o/flare-dashboard webdash
   ```
3. CD into the new directory:
   ```shell
   cd webdash
   ```
4. Create a python virtual environment:
   ```shell
   sudo python3 -m venv env
   ```
5. Activate the environment:
   ```shell
   source env/bin/activate
   ```
6. Install the required modules:
   ```shell
   sudo pip3 install -r requirements.txt
   ```
### Start the webapp
1. If you haven't already, activate the environment:
   ```shell
   source env/bin/activate
   ```
2. Run the app with sudo:
   ```shell
   sudo python3 app.py
   ```

**By default, the dashboard will be hosted on port 2 and the login will be admin:admin**

# License
This project is published under the [MIT license](./LICENSE)
