from fabric.api import local

def prepare_deployment(branch_name):
    local('python manage.py test')
    local('git add -p && git commit')
    local('git checkout master && git merge '+ branch_name)

def deploy():
    with lcd('/path/to/prod/area')
        local('git checkout master && git pull')
        local('python manage.py migrate')
        local('python manage.py test')
        local('sudo restart httpd graceful')
