<div align="center">
    </a>
    <br />
    <img align="center" src="https://cdn.discordapp.com/attachments/1092315227057561630/1230745160464338954/flare.png?ex=66346fc0&is=6621fac0&hm=b6dafeba296665988c5afaad3b1dd3d82abf143f1fdc76cd7299e259c94564cd&">
    
   ![GitHub last commit](https://img.shields.io/github/last-commit/t-a-g-o/flare-webapp)
   ![GitHub issues](https://img.shields.io/github/issues-raw/t-a-g-o/flare-webapp)
   ![GitHub](https://img.shields.io/github/license/t-a-g-o/flare-webapp)

   **VERSION 0.1**
    
</div>

> This Web dashboard makes it eaiser to configure [Flare](https://github.com/tagoworks/flare), and look at different statistic and data about Flare.

<br />
<div align="center">
<img width="538.8" height="448.8" src="https://cdn.discordapp.com/attachments/1092315227057561630/1233800533219737663/preview.png?ex=662e69ca&is=662d184a&hm=453095cfa109961d7632f23b5fdf64f737dbbb51734fc4a12843c4f6078612f0&">
</div>

# Getting Started
### Create webdash directory
1. CD to the Flare main directory
2. Create a new directory:
   ```shell
   sudo mkdir webdash
   ```
### Clone and setup the web files
1. CD into the new webapp directory
3. Clone the repository:
   ```shell
   sudo git clone https://github.com/t-a-g-o/flare-webapp .
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
   pip3 install -r requirements.txt
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
**By default, the dashboard will be hosted on port 2**

I will be working on this webapp more and more to make it way nicer and include a lot more functions, I just wanted to do this to see if it was possible with the knowledge I have.

# License
This project is published under the [MIT license](./LICENSE)
