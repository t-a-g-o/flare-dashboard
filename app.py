from flask import Flask, send_from_directory, request, jsonify
import os, json, subprocess
app = Flask(__name__)
@app.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'static'), filename)
@app.route('/images/<path:filename>')
def serve_image(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'images'), filename)

@app.route('/')
def load():
    with open('load.html', 'r') as f:
        html_content = f.read()
        return html_content
@app.route('/dashboard')
def dashboard():
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
        with open('log.txt') as f:
            logging = f.read()
    except:
        logging = 'No log file'
    try:
        apache_status = subprocess.run(['systemctl', 'status', 'apache2'], capture_output=True, text=True)
        apache_running = 'active' in apache_status.stdout.lower()
    except Exception as e:
        apache_running = False
    try:
        cloudflare_status = subprocess.run(['docker', 'ps'], capture_output=True, text=True)
        cloudflare_running = 'cloudflare' in cloudflare_status.stdout.lower()
    except Exception as e:
        cloudflare_running = False
    try:
        flask_status = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        flask_running = 'flask' in flask_status.stdout.lower()
    except Exception as e:
        flask_running = False
    try:
        node_status = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        node_running = 'node' in node_status.stdout.lower()
    except Exception as e:
        node_running = False
    try:
        with open('../assets/watcher.lck', 'rb') as f:
            f.read()
        python_running = True
    except Exception as e:
        python_running = False
    with open('load.html', 'r') as f:
        base_template = f.read()
    with open('dashboard.html', 'r') as f:
        html_content = f.read()
    html_content = html_content.replace('{{ licenses_stored }}', str(licenses_stored))
    html_content = html_content.replace('{{ keys_activated }}', str(keys_activated))
    html_content = html_content.replace('{{ logging }}', logging)
    html_content = html_content.replace('{{ recent_validates }}', '<br/>'.join(recent_validates))
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
@app.route('/secrets')
def secrets():
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
    html_content = html_content.replace('{{ content }}', f'Private Key= {privatekey}' + '<br /><br />' + f'Public Key= {publickey}')
    return html_content
@app.route('/config')
def configure():
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
            token = data['Discord Bot Token']
            guildID = data['123456891234567891']
            ownerID = data['123456891234567891']
            onlySendIn = data['123456891234567891']
            logChannel = data['123456891234567891']
            webdavDir = data['/var/www/accs']
            webdavLink = data['https://auth.yourdomain.com/']
    html_content = html_content.replace('{{ token_saved }}', token)
    html_content = html_content.replace('{{ guildid_saved }}', guildID)
    html_content = html_content.replace('{{ ownerid_saved }}', ownerID)
    html_content = html_content.replace('{{ sendinid_saved }}', onlySendIn)
    html_content = html_content.replace('{{ logid_saved }}', logChannel)
    html_content = html_content.replace('{{ webdir_saved }}', webdavDir)
    html_content = html_content.replace('{{ weblink_saved }}', webdavLink)
    return html_content
@app.route('/save', methods=['POST'])
def save_config():
    form_data = request.get_json()
    with open('../config.json', 'w') as config_file:
        json.dump(form_data, config_file, indent=2)
    return jsonify({'success': True, 'message': 'Config saved successfully'})
if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0',port='2')