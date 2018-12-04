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
<https://github.com/CentOS-Storage-SIG/centos-release-ceph-luminous>`_ release
package, and globally search-and-replace "luminous" to "nautilus". Note the
``.repo`` file is named "Luminous", so rename this to "Nautilus", etc.

3. Create the SRPM (see the instructions in the README)::

    rpmbuild -bs ...

4. Build the SRPM with CBS (see instructions in the README)::

    cbs build ...

5. Push your `changes
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
https://buildlogs.centos.org/centos/7/extras/x86_64/ . A cron job runs every
two hours to push builds to the testing repository. If you do not see the build
on the buildlogs.centos.org web server two hours after tagging in CBS, contact
the admins in #centos-devel.

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
