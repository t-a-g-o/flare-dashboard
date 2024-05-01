from flask import Flask, send_from_directory, request, jsonify, render_template, redirect, session
import os
import json
import subprocess
import socket
import time
from datetime import datetime

#
# Username and password to log into the Dashboard
#
username = 'admin'
password = 'admin'





app = Flask(__name__)
app.secret_key = 'session'
def check_authentication():
    if 'logged_in' in session and session['logged_in']:
        return True
    return False
def localip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        return ip
    except socket.error:
        return None
@app.errorhandler(404)
def page_not_found(e):
    return redirect('/')
@app.route('/send', methods=['POST'])
def send_command():
    global terminal_log
    data = request.get_json()
    command = data['command']
    try:
        output = subprocess.run(command, shell=True, capture_output=True, text=True)
        terminal_log = output.stdout
        terminal_log = terminal_log.replace('\n', '<br/>')
        return jsonify({'success': True}), 200
    except Exception as e:
        terminal_log = f"Couldn't send the command: {e}"
        return jsonify({'success': False}), 500
@app.route('/update', methods=['GET'])
def getlog():
    global terminal_log
    time.sleep(1)
    return jsonify({'terminalLog': terminal_log})

@app.route('/services', methods=['GET'])
def getservices():
    time.sleep(1) 
    registered_dir = '../assets/registered/'
    try:
        with open('../assets/validkeys.txt', 'r') as f:
            lines = len(f.readlines())
            licenses_stored = lines
    except:
        licenses_stored = 'N/A'
    try:
        registered_dir = '../assets/registered/'
        keys_activated = len([name for name in os.listdir(registered_dir) if os.path.isdir(os.path.join(registered_dir, name))])
    except:
        keys_activated = 'N/A' 
    try:
        recent_folders = sorted([name for name in os.listdir(registered_dir) if os.path.isdir(os.path.join(registered_dir, name))], key=lambda x: os.path.getctime(os.path.join(registered_dir, x)), reverse=True)[:10]
        recent_validates = [path.split(os.path.sep)[-1] for path in [os.path.join(registered_dir, folder) for folder in recent_folders]]
    except:
        recent_validates = 'N/A'
    try:
        with open('../flare.log') as f:
            logging = f.read()
            logging = logging.replace('\n', '<br/>')
    except:
        logging = 'No log file'
    try:
        apache_status = subprocess.run(['systemctl', 'status', 'apache2'], capture_output=True, text=True)
        apache_running = '(running)' in apache_status.stdout.lower()
    except Exception as e:
        apache_running = False
    try:
        cloudflare_status = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
        cloudflare_running = 'cloudflare' in cloudflare_status.stdout.lower()
    except Exception as e:
        cloudflare_running = False
    flask_running = False
    node_running = False
    python_running = False
    if os.path.exists('../api.lck'): 
        flask_running = True
    if os.path.exists('../main.lck'):
        node_running = True
    if os.path.exists('../assets/watcher.lck'):
        python_running = True
    if apache_running == True:
        apache_service_status = './images/running.png'
    else:
        apache_service_status = './images/notrunning.png'
    if cloudflare_running == True:
        cloudflare_service_status = './images/running.png'
    else:
        cloudflare_service_status = './images/notrunning.png'

    if flask_running == True:
        flask_service_status = './images/running.png'
    else:
        flask_service_status = './images/notrunning.png'

    if node_running == True:
        node_service_status = './images/running.png'
    else:
        node_service_status = './images/notrunning.png'

    if python_running == True:
        python_service_status = './images/running.png'
    else:
        python_service_status = './images/notrunning.png'

        service_status = {
        'apache_service': apache_service_status,
        'flask_service': flask_service_status,
        'cloudflare_service': cloudflare_service_status,
        'python_service': python_service_status,
        'node_service': node_service_status,
        'licenses_stored': licenses_stored,
        'keys_active': keys_activated,
        'recent_validates': recent_validates
    }
    return jsonify(service_status)

@app.route('/')
def root():
    if check_authentication():
        return redirect('/dashboard')
    else:
        return render_template('unlock.html', localip=localip())
@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/')
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if data:
        user = data.get('username')
        passw = data.get('password')
        if user == username and passw == password:
            session['logged_in'] = True
            session['last_activity'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return jsonify({'message': 'Login successful'}), 200
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    else:
        return jsonify({'message': 'Invalid request format'}), 400
@app.route('/static/<path:filename>')
def serve_static(filename):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        return send_from_directory(os.path.join(root_dir, 'static'), filename)
@app.route('/images/<path:filename>')
def serve_image(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'images'), filename)
@app.route('/dashboard')
def dashboard(log=""):
    if check_authentication():
        try:
            with open('../assets/validkeys.txt', 'r') as f:
                lines = len(f.readlines())
                licenses_stored = lines
        except:
            licenses_stored = 'N/A'
        try:
            registered_dir = '../assets/registered/'
            keys_activated = len([name for name in os.listdir(registered_dir) if os.path.isdir(os.path.join(registered_dir, name))])
        except:
            keys_activated = 'N/A'
        try:
            recent_folders = sorted([name for name in os.listdir(registered_dir) if os.path.isdir(os.path.join(registered_dir, name))], key=lambda x: os.path.getctime(os.path.join(registered_dir, x)), reverse=True)[:10]
            recent_validates = [path.split(os.path.sep)[-1] for path in [os.path.join(registered_dir, folder) for folder in recent_folders]]
        except:
            recent_validates = 'N/A'
        try:
            with open('../flare.log') as f:
                logging = f.read()
                logging = logging.replace('\n', '<br/>')
        except:
            logging = 'No log file'
        try:
            apache_status = subprocess.run(['systemctl', 'status', 'apache2'], capture_output=True, text=True)
            apache_running = '(running)' in apache_status.stdout.lower()
        except Exception as e:
            apache_running = False
        try:
            cloudflare_status = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
            cloudflare_running = 'cloudflare' in cloudflare_status.stdout.lower()
        except Exception as e:
            cloudflare_running = False
        flask_running = False
        node_running = False
        python_running = False
        if os.path.exists('../api.lck'): 
            flask_running = True
        if os.path.exists('../main.lck'):
            node_running = True
        if os.path.exists('../assets/watcher.lck'):
            python_running = True
        with open('dashboard.html', 'r') as f:
            html_content = f.read()
        html_content = html_content.replace('{{ licenses_stored }}', str(licenses_stored))
        html_content = html_content.replace('{{ keys_activated }}', str(keys_activated))
        html_content = html_content.replace('{{ logging }}', logging)
        html_content = html_content.replace('{{ terminallog }}', log)
        html_content = html_content.replace('{{ recent_validates }}', '<br/>'.join(recent_validates))
        html_content = html_content.replace('{{ localip }}', localip())
        if apache_running == True:
            html_content = html_content.replace('{{ apache_service }}', './images/running.png')
        else:
            html_content = html_content.replace('{{ apache_service }}', './images/notrunning.png')
        if cloudflare_running == True:
            html_content = html_content.replace('{{ cloudflare_service }}', './images/running.png')
        else:
            html_content = html_content.replace('{{ cloudflare_service }}', './images/notrunning.png')

        if flask_running == True:
            html_content = html_content.replace('{{ flask_service }}', './images/running.png')
        else:
            html_content = html_content.replace('{{ flask_service }}', './images/notrunning.png')

        if node_running == True:
            html_content = html_content.replace('{{ node_service }}', './images/running.png')
        else:
            html_content = html_content.replace('{{ node_service }}', './images/notrunning.png')

        if python_running == True:
            html_content = html_content.replace('{{ python_service }}', './images/running.png')
        else:
            html_content = html_content.replace('{{ python_service }}', './images/notrunning.png')

        return html_content
    else:
        return redirect('/')
@app.route('/secrets')
def secrets():
    if check_authentication():
        with open('secrets.html', 'r') as f:
            html_content = f.read()
        try: 
            with open('../assets/identifiers.txt', 'r') as f:
                lines = f.readlines()
                for i in range(len(lines)):
                    if "PRIVATE KEY IDENTIFIER" in lines[i]:
                        privatekey = lines[i+1].strip()
                        break
                for i in range(len(lines)):
                    if "PUBLIC KEY IDENTIFIER" in lines[i]:
                        publickey = lines[i+1].strip()
                        break
        except:
            privatekey = 'NOT FOUND'
            publickey = 'NOT FOUND'
        html_content = html_content.replace('{{ localip }}', localip())
        html_content = html_content.replace('{{ privatekey }}', privatekey)
        html_content = html_content.replace('{{ publickey }}', publickey)
        return html_content
    else:
        return redirect('/')
@app.route('/log')
def log():
    if check_authentication():
        with open ('log.html', 'r')as f:
            html_content = f.read()
        try:
            with open ('../flare.log', 'r') as f:
                logs = f.read()
                logs = logs.replace('\n', '<br/>')
        except Exception as e:
            logs = "Couldn't read log file"
        html_content = html_content.replace('{{ localip }}', localip())
        html_content = html_content.replace('{{ logging }}', logs)
        return html_content
    else:
        return redirect('/')
@app.route('/config', methods=['GET','POST'])
def configure():
    if check_authentication():
        if request.method == 'POST': 
            with open('../config.json', 'r') as f:
                config_data = json.load(f)
            data = request.get_json()
            for key, value in data.items():
                if value.strip():
                    config_data[key] = value
            with open('../config.json', 'w') as f:
                json.dump(config_data, f, indent=4)
            return jsonify({"message": "Configuration updated successfully"}), 200

        else:
            with open('config.html', 'r') as f:
                html_content = f.read()
            try: 
                    with open('../config.json', 'r') as f:
                        data = json.load(f)
                    token = data['token']
                    guildID = data['guildID']
                    ownerID = data['ownerID']
                    onlySendIn = data['onlySendIn']
                    logChannel = data['logChannel']
                    webdavDir = data['webdavDir']
                    webdavLink = data['webdavLink']
            except:
                    token = 'Discord Bot Token'
                    guildID = '123456891234567891'
                    ownerID = '123456891234567891'
                    onlySendIn = '123456891234567891'
                    logChannel = '123456891234567891'
                    webdavDir = '/var/www/accs'
                    webdavLink = 'https://auth.yourdomain.com/'
            html_content = html_content.replace('{{ localip }}', localip())
            html_content = html_content.replace('{{ token_saved }}', token)
            html_content = html_content.replace('{{ guildid_saved }}', guildID)
            html_content = html_content.replace('{{ ownerid_saved }}', ownerID)
            html_content = html_content.replace('{{ sendinid_saved }}', onlySendIn)
            html_content = html_content.replace('{{ logid_saved }}', logChannel)
            html_content = html_content.replace('{{ webdir_saved }}', webdavDir)
            html_content = html_content.replace('{{ weblink_saved }}', webdavLink)
            return html_content
    else:
        return redirect('/')
if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0',port='2')