Setting up a new Ceph release
=============================

The next release of Ceph is codenamed "nautilus". We want to build and host
this in CentOS's system. Here are the steps to set that up.

Installing CBS client
---------------------

Please install the CBS client (CLI) on your system. You will need it to build
new RPMs and manage builds. Instructions at https://wiki.centos.org/SIGGuide

Configuring CBS
---------------

The first step is to open a `ticket <https://bugs.centos.org/>`_ with the
CentOS CBS administrators. The CBS admins will configure three things for us:

1. Create our set of Koji tags (eg. ``-candidate``, ``-testing``, and
   ``-release``).

2. Create our Koji build `target <http://cbs.centos.org/koji/buildtargets>`_
   (eg. ``storage7-ceph-nautilus-el7``).

3. `Configure <https://wiki.centos.org/SIGGuide/Content/BuildLogs>`_ the Yum
   repository "downloads" `site <https://buildlogs.centos.org/centos/7/>`_ for
   the builds.
   
Here is the nautilus ticket: https://bugs.centos.org/view.php?id=15269 (`A
script <new-major-release.py>`_ can file these automatically.)

Creating centos-release-ceph-nautilus package
---------------------------------------------

For each major Ceph release, we must create a "-release" package.

This process is `in flux
<https://lists.centos.org/pipermail/centos-devel/2018-November/017093.html>`_,
but basically we will need to coordinate with Niels de Vos <ndevos@redhat.com>
to create the new repository in GitHub for this package.

Once you have the GitHub repository location:

1. Clone the repository::

    git clone git@github.com:CentOS-Storage-SIG/centos-release-ceph.git
    cd centos-release-ceph
    git checkout nautilus

2. Copy the `centos-release-ceph-luminous
   <https://github.com/CentOS-Storage-SIG/centos-release-ceph-luminous>`_
   release package, and globally search-and-replace "luminous" to "nautilus".
   Note the ``.repo`` file is named "Luminous", so rename this to "Nautilus",
   etc.

3. Create the SRPM (see the instructions in the README)::

    rpmbuild -bs ...

4. Ensure the package is whitelisted ("added") to the three CentOS Extras
   tags::

    cbs add-pkg --owner ktdreyer core7-extras-common-candidate centos-release-ceph-nautilus
    cbs add-pkg --owner ktdreyer core7-extras-common-testing centos-release-ceph-nautilus
    cbs add-pkg --owner ktdreyer core7-extras-common-release centos-release-ceph-nautilus

5. Build the SRPM with CBS (see instructions in the README)::

    cbs build ...

6. Push your `changes
   <https://github.com/CentOS-Storage-SIG/centos-release-ceph/commit/2d27abb289727eaa98927805f9c2759ef974a0cb>`_
   to the ``nautilus`` branch in GitHub. This ensures we have a record of the
   code in Git for future modifications.

At this point you will have your first build in CBS.

Clarifying note: Our first build here is going into *CentOS Extras*, not into
our Storage SIG/ceph nautilus repo. The ``-release`` package is the only one
like this. It simply bootstraps the user's
``/etc/yum.repos.d/CentOS-Ceph-Nautilus.repo`` file so they can obtain the rest
of the Ceph packages.

Moving builds through -testing and -release
-------------------------------------------

When you build anything in CBS, the system will automatically tag that build
into the ``-candidate`` tag. ``-candidate`` just means that the build *could*
go somewhere, but it is not ready to go into a testing Yum repository yet.

Continuing from above, your ``centos-release-ceph-nautilus`` package will be
tagged into ``core7-extras-common-candidate`` to start.

To move this build into the "testing" repository, we will tag it into the
``-testing`` CBS tag::

    cbs tag-build core7-extras-common-testing centos-release-ceph-nautilus-1.1-1.el7.centos

Once the build is in ``core7-extras-common-testing``, the CBS administrators
will put it into the "testing" repository at
https://buildlogs.centos.org/centos/7/extras/x86_64/ .

The CBS administrators run `mash <https://pagure.io/mash>`_ in a `cron script
<https://git.centos.org/blob/sig-core!cbs-tools.git/master/scripts!mash_run.sh>`_
every two hours to push builds to the testing repository. If you do not see
the build on the buildlogs.centos.org web server two hours after tagging in
-testing in CBS, contact the admins in #centos-devel.

To move this build into the "release" repository, we will tag it into the
``-release`` CBS tag::

    cbs tag-build core7-extras-common-release centos-release-ceph-nautilus-1.1-1.el7.centos

Once the build is in the ``-release`` tag, the CBS administrators will GPG-sign
it and put it into the main Yum repositories that are mirrored everywhere. For
``core7-extras-common-release``, this is
http://mirror.centos.org/centos/7/extras/x86_64/.  (TODO: figure out what
triggers this, and how long to wait).

Using the centos-release-ceph-nautilus package
----------------------------------------------

From this point our ``centos-release-ceph-nautilus`` package is pushed out to
CentOS' mirror system for CentOS Extras. All CentOS users can "yum install" our
build from CentOS Extras now::

    # Already done on most CentOS systems:
    # yum-config-manager --enable extras

    # Install our newly-released build: 
    yum install centos-release-ceph-nautilus

Now these users will have an ``/etc/yum.repos.d/CentOS-Ceph-Nautilus.repo`` on
their systems. This will point at the rest of our Ceph packages. These users
will be able to ``yum install ceph`` and get the nautilus package.

Copying the package list from the older release
-----------------------------------------------

At this point we have a ``storage7-ceph-nautilus-candidate`` tag that is
completely empty::

    cbs list-tagged storage7-ceph-nautilus-candidate

    Build                                 Tag               Built by
    ------------------------------------  ----------------  ----------------

We need to populate this tag.

First, let's find the list of **packages** that are present in the tag for our
older release (luminous)::

    cbs list-pkgs --tag=storage7-ceph-luminous-candidate
    Package             Tag                     Extra Arches    Owner
    ------------------- ----------------------- --------------- ---------------
    oniguruma           storage7-ceph-luminous-candidate        alphacc
    python-logutils     storage7-ceph-luminous-candidate        gfidente
    ...

Visually inspect this list of source package names.

Note anything that is end-of-life/unsupported. You don't want to carry ancient
unsupported packages over into the next major release. For example,
``radosgw-agent`` is really old and should not be carried along into nautilus.

Once you have copied and edited your list of packages for nautilus, run those
through ``cbs add-pkg`` so we are able to tag the builds::

    cbs add-pkg --owner ktdreyer storage7-ceph-nautilus-candidate ceph-ansible jq ...
    cbs add-pkg --owner ktdreyer storage7-ceph-nautilus-testing ceph-ansible jq ...
    cbs add-pkg --owner ktdreyer storage7-ceph-nautilus-release ceph-ansible jq ...

At this point you've set the package lists for your tags. Check them with
``cbs list-pkgs``, like so::

    cbs list-pkgs --tag=storage7-ceph-luminous-candidate
    cbs list-pkgs --tag=storage7-ceph-luminous-testing
    cbs list-pkgs --tag=storage7-ceph-luminous-release

Copying the build list from the older release
---------------------------------------------

Now that we've configured our package lists, we can tag some builds.

Let's find the list of **builds** that are currently tagged for the older
release (luminous)::

    cbs list-tagged storage7-ceph-luminous-candidate --latest
    Build                             Tag               Built by
    --------------------------------  ----------------  ----------------
    babeltrace-1.2.4-3.1.el7          storage7-ceph-luminous-candidate  koji
    ceph-12.2.5-0.el7                 storage7-ceph-luminous-candidate  gfidente
    ceph-ansible-3.2.0-0.rc8.1.el7    storage7-ceph-luminous-candidate  ktdreyer
    ...

Visually inspect this list of build NVRs (*name* - *version* - *release*).

As above when we were checking ``list-pkgs``, make a note to drop anything that
is end-of-life/unsupported.

*Also*, we also don't want to copy the ``ceph-12.2.5-0.el7`` build into
nautilus either. Remember, this set of tags is just for ``ceph-14.0.0`` and
newer.

Once you have assembled your list of build NVRs to tag from luminous into
nautilus, you can tag these into ``storage7-ceph-nautilus-candidate``::

   cbs tag-build storage7-ceph-nautilus-candidate babeltrace-1.2.4-3.1.el7 ceph-ansible-3.2.0-0.rc8.1.el7 ...

CBS will run a number of `tagBuild
<http://cbs.centos.org/koji/tasks?method=tagBuild&state=active&view=tree&order=-id>`_
tasks, one per build, as it adds each build into our ``-nautilus-candidate``
tag.

Once those ``tagBuild`` tasks finish, you should be able to see all your newly-tagged builds with ``list-tagged``::

    cbs list-tagged storage7-ceph-nautilus-candidate

Buildroots and kojira
---------------------

As we begin to populate our ``-nautilus-candidate`` tag, you will notice a
`kojira <http://cbs.centos.org/koji/tasks?owner=kojira&state=all>`_ user will
begin to generate a set of new repositories for us with ``newRepo`` and
``createrepo`` tasks. kojira will regenerate our **buildroots** every time the
``storage7-ceph-nautilus-el7-build`` tag or its children change. A "buildroot"
is a Yum repository within Koji that defines which RPMs are available when we
build any new packages.

You can inspect these buildroot repositories at
http://cbs.centos.org/kojifiles/repos/storage7-ceph-nautilus-el7-build/latest/x86_64/
. The ``pkglist`` file is handy to get a birds-eye view of what RPMs are in
that particular buildroot (yum repo).

Once we see that CBS's kojira has generated a buildroot for our
``storage7-ceph-nautilus-el7-build`` tag, we are ready to build Ceph itself in
CBS.
