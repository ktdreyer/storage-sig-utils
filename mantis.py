import os
from zeep import Client
try:
    from configparser import SafeConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser


URL = 'https://bugs.centos.org/api/soap/mantisconnect.php?wsdl'
CREDENTIAL_FILE = os.path.expanduser('~/.mantistoken')


client = Client(URL)


def credentials():
    """
    Read this user's Mantis username/password.

    $ cat ~/.mantistoken
    [bugs.centos.org]
    username = ktdreyer
    password = my$ecretpa$$word

    :returns: (username, password) tuple
    """
    cfg = SafeConfigParser()
    cfg.read(CREDENTIAL_FILE)
    section = 'bugs.centos.org'
    username = cfg.get(section, 'username')
    password = cfg.get(section, 'password')
    return (username, password)


def find_issue(summary):
    """ Returns the ticket ID number, or 0 if nothing matched. """
    username, password = credentials()
    result = client.service.mc_issue_get_id_from_summary(username, password,
                                                         summary)
    return result


def new_issue(summary, description, project, category):
    """ Returns the new ticket ID number """
    username, password = credentials()
    project_id = client.service.mc_project_get_id_from_name(username,
                                                            password, project)
    print(project_id)
    issue = {'summary': summary,
             'description': description,
             'project': {'id': project_id},
             'category': category,
             }
    result = client.service.mc_issue_add(username, password, issue)
    return result
