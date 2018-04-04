from jinja2 import Environment, FileSystemLoader
import mantis

PATH = '.'
FILENAME = 'new-major-release.j2'

env = Environment(loader=FileSystemLoader(PATH))


def get_codename():
    """ Get the new ceph release """
    return 'mimic'


def get_target(codename):
    return 'storage7-ceph-%s-el7' % codename


def get_tags(codename):
    tags = {
        'candidate': 'storage7-ceph-%s-candidate' % codename,
        'build':     'storage7-ceph-%s-el7-build' % codename,
        'testing':   'storage7-ceph-%s-testing' % codename,
        'release':   'storage7-ceph-%s-release' % codename,
    }
    return tags


def get_buildlogs_mapping(codename):
    mapping = 'storage7-ceph-{codename}-testing|7/storage/x86_64/ceph-{codename}/|7/storage/x86_64/ceph-{codename}/|7/storage/x86_64/ceph-{codename}/'.format(codename=codename)  # NOQA: E501
    return mapping


def get_name():
    """ Get my name """
    return 'Ken'


if __name__ == '__main__':
    codename = get_codename()
    content = {
        'tags': get_tags(codename),
        'target': get_target(codename),
        'buildlogs_mapping': get_buildlogs_mapping(codename),
        'name': get_name()
    }

    text = env.get_template(FILENAME).render(content)

    summary = 'set up CBS for Ceph %s' % codename
    project = 'Buildsys'
    category = 'community buildsys'
    # Before filing this issue, search this summary title to see if we've
    # already filed it.
    issue = mantis.find_issue(summary)
    if issue:
        print('existing ticket https://bugs.centos.org/view.php?id=%d' % issue)
        raise SystemExit()
    issue = mantis.new_issue(summary, text, project, category)
    print('created https://bugs.centos.org/view.php?id=%d' % issue)
