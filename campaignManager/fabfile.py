from fabric.api import local

def prepare_deployment(branch_name):
    local('python manage.py test campaignManager')
    local('git add -p && git commit')
    local('git checkout master && git merge '+ branch_name)

def deploy():
    with lcd('/path/to/prod/area')
        local('git checkout master && git pull')
        local('python manage.py migrate cmArmies')
        local('python manage.py migrate cmCampaigns')
        local('python manage.py migrate cmProfiles')
        local('python manage.py test campaignManager')
        local('sudo restart httpd graceful')
