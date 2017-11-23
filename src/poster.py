import os
import shutil
import tarfile
import paramiko
import webbrowser
from yaml import load
from jinja2 import Template


def ssh_scp_put(ip, port, username, password, local_file, remote_file):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, username, password)
    sftp = ssh.open_sftp()
    sftp.put(local_file, remote_file)
    ssh.close()


def ssh_cmd(ip, port, username, password, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip, port, username, password)
    ssh.exec_command(command)
    ssh.close()


src_path = os.getcwd()
dst_path = os.path.join(os.path.dirname(os.getcwd()), 'gen')
os.mkdir(dst_path)

path = os.path.join(os.getcwd(), 'poster.yaml')
with open(path, 'r') as file:
    data = load(file)

with open(os.path.join(os.getcwd(), 'poster.html'), 'r') as file:
    template = Template(file.read())

path = os.path.join(os.path.dirname(os.getcwd()), 'gen/poster.html')
with open(path, 'w') as file:
    file.write(template.render(data))

shutil.copytree(os.path.join(src_path, 'css'), os.path.join(dst_path, 'css'))
shutil.copytree(os.path.join(src_path, 'img'), os.path.join(dst_path, 'img'))
shutil.copytree(os.path.join(src_path, 'js'), os.path.join(dst_path, 'js'))

tar_path = os.path.join(dst_path, 'poster.tar.gz')
with tarfile.open(tar_path, "w:gz") as tar:
    tar.add(dst_path, arcname='poster')

with open(os.path.join(os.getcwd(), 'login.yaml'), 'r') as file:
    login = load(file)

ssh_scp_put(login['ip'], login['port'], login['username'], login['password'], tar_path,
            '/var/www/html/poster.tar.gz')
command = 'cd /var/www/html; tar -zxvf /var/www/html/poster.tar.gz'
ssh_cmd(login['ip'], login['port'], login['username'], login['password'], command)

webbrowser.open(login['dest'])

shutil.rmtree(dst_path)
