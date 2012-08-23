#!/usr/bin/env python2
#   Author(s): Milan Falesnik <mfalesni@redhat.com>
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Copyright (c) 2012 Red Hat, Inc. All rights reserved.
#
#   This copyrighted material is made available to anyone wishing
#   to use, modify, copy, or redistribute it subject to the terms
#   and conditions of the GNU General Public License version 2.
#
#   This program is distributed in the hope that it will be
#   useful, but WITHOUT ANY WARRANTY; without even the implied
#   warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#   PURPOSE. See the GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public
#   License along with this program; if not, write to the Free
#   Software Foundation, Inc., 51 Franklin Street, Fifth Floor,
#   Boston, MA 02110-1301, USA.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import common
import pytest
import os

def test_import_ssh_certificate(audreyvars):
    JENKINS_SSH_KEY_LOCATION = audreyvars.get("JENKINS_SSH_KEY_LOCATION", "None")
    JENKINS_SSH_DIR = audreyvars.get("JENKINS_SSH_DIR", "/root/.ssh")
    if JENKINS_SSH_KEY_LOCATION.lower() == "none":
        # Key is not present, skipping
        pytest.skip(msg="SSH key is not present, skipping")
    # Create JENKINS_SSH_DIR
    if not os.path.isdir(JENKINS_SSH_DIR):
        common.mkdir(JENKINS_SSH_DIR)
    # Prepare variable to store file name
    target = ""
    if not JENKINS_SSH_KEY_LOCATION.startswith("/"):
        # Key is file in local directory
        filename = "%s/KATELLO_REGISTER/%s" % (common.audrey_service_path, JENKINS_SSH_KEY_LOCATION)
        target = "%s/%s" % (JENKINS_SSH_DIR, JENKINS_SSH_KEY_LOCATION)
        if not os.path.isfile(filename):
            pytest.fail(msg="Unable to find file '%s'" % filename)
        common.copy(filename, target)
    else:
        # Key is file or URL
        if JENKINS_SSH_KEY_LOCATION.startswith("http"):
            # It's an URL
            target = "%s/%s" % (JENKINS_SSH_DIR, common.filename_from_url(JENKINS_SSH_KEY_LOCATION))
            common.run("wget -O \"%s\" \"%s\"" % (target, JENKINS_SSH_KEY_LOCATION))
        else:
            # It's a file somewhere in filesystem
            if not os.path.isfile(filename):
                pytest.fail(msg="Unable to find file '%s'" % filename)
            target = "%s/%s" % (JENKINS_SSH_DIR, os.path.basename(JENKINS_SSH_KEY_LOCATION))
            common.copy(JENKINS_SSH_KEY_LOCATION, target)           
    # Verify that key is in place
    if not os.path.isfile(target):
        pytest.fail(msg="Importing the key was unsuccessful, key is not present in '%s'" % target)
    # Add the key into authorized keys
    authkeys = "%s/authorized_keys" % JENKINS_SSH_DIR
    with open(authkeys, "a") as authfile:
        with open(target, "r") as keyfile:
            authfile.write(key.file.read)
    # Verify again that the file exists
    # Verify that key is in place
    if not os.path.isfile(authkeys):
        pytest.fail(msg="Importing the key was unsuccessful, file '%s' does not exist" % authkeys)