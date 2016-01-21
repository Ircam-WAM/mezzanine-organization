#!/usr/bin/python

import os

path = os.getcwd()
vcss = ['git', 'svn', 'hg']

def is_repo_root(path):
    content = os.listdir(path)
    for vcs in vcss:
        if '.' + vcs in content:
            return True
    return False

while not is_repo_root(path):
    path = os.sep.join(path.split(os.sep)[:-1])

path = os.sep.join(os.getcwd().split(os.sep)[:-2])
name = path.split(os.sep)[-1].lower()
conf = path + os.sep + 'docker-compose.yml'
service = '/etc/init.d/' + name

print 'installing ' + name + '...'

if not os.path.exists('/etc/init.d/docker'):
    os.system('wget -qO- https://get.docker.com/ | sh')
    os.system('pip install docker-compose')

f = open('init.sh.example', 'r')
rules = f.read() % (name, name, conf)
f.close()

f = open(service, 'w')
f.write(rules)
f.close()

os.system('chmod 755 ' + service)
os.system('update-rc.d ' + name + ' defaults')

print 'done'
