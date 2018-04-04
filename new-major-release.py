from jinja2 import Environment, FileSystemLoader

# TODO: use https://github.com/morenice/mantisconnect-python

PATH = '.'
FILENAME = 'new-major-release.j2'

env = Environment(loader=FileSystemLoader(PATH))


def get_codename():
    """ Get the new ceph release """
    return 'mimic'


def get_tags(codename):
    tags = {
        'candidate': 'storage7-ceph-%s-candidate' % codename,
        'build':     'storage7-ceph-%s-el7-build' % codename,
        'testing':   'storage7-ceph-%s-testing' % codename,
        'release':   'storage7-ceph-%s-release' % codename,
    }
    return tags


def get_buildlogs_mapping(codename):
    mapping = 'storage7-ceph-{codename}-testing|7/storage/x86_64/ceph-{codename}/|7/storage/x86_64/ceph-{codename}/|7/storage/x86_64/ceph-{codename}/'.format(codename=codename)
    return mapping


def get_name():
    """ Get my name """
    return 'Ken'


if __name__ == '__main__':
    codename = get_codename()
    content = {
        'tags': get_tags(codename),
        'buildlogs_mapping': get_buildlogs_mapping(codename),
        'name': get_name()
    }

    text = env.get_template(FILENAME).render(content)

    print(text)
