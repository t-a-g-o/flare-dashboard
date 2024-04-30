<div align="center">
    </a>
    <br />
    <img align="center" src="https://cdn.discordapp.com/attachments/1092315227057561630/1234661647516438558/webdash.png?ex=66318bc3&is=66303a43&hm=61e991bcdd9217dbd11eec0657b59c54a5aadc4329011005caff620482e62f5f&">
    
   ![GitHub last commit](https://img.shields.io/github/last-commit/t-a-g-o/flare-webapp)
   ![GitHub issues](https://img.shields.io/github/issues-raw/t-a-g-o/flare-webapp)
   ![GitHub](https://img.shields.io/github/license/t-a-g-o/flare-webapp)

   **VERSION 0.1**
    
</div>

> This Web dashboard makes it eaiser to configure [Flare](https://github.com/tagoworks/flare), and look at different statistic and data about Flare.

<br />
<div align="center">
<img width="498.6" height="271.2" src="https://cdn.discordapp.com/attachments/1092315227057561630/1234875441526079579/showcase.png?ex=663252e0&is=66310160&hm=51da4ff2b518e6bf019d9bbe13ef2380dac81b242de95bf6b203ce2ab0cfb385&">
</div>

# Getting Started
### Create webdash directory
1. CD to the Flare main directory
2. Create a new directory:
   ```shell
   sudo mkdir webdash
   ```
### Clone and setup the web files
1. CD into the new webdash directory
3. Clone the repository:
   ```shell
   sudo git clone https://github.com/t-a-g-o/flare-dashboard .
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
# More information
**By default, the dashboard will be hosted on port 2 and the login will be admin:admin**

I will be working on this webapp more and more to make it way nicer and include a lot more functions, I just wanted to do this to see if it was possible with the knowledge I have.

# License
This project is published under the [MIT license](./LICENSE)
