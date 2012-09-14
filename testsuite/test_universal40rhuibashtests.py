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
import sys
import os
import pytest

@pytest.mark.parametrize("testname", common.RHUItests_list_base())
def test_RHUItest(testname, rhel_release):
    """ Launches specific tests from RHUIQE bash test suite

    :param testname: Test name
    :type testname: ``str``

    :raises: pytest.Failed
    """
    result, rc = common.shellcall("cd rhui-tests/ && ./test.sh %s" % testname)
    if rc != 0:
        sys.stderr.write(common.shellcall("cd rhui-tests/ && ./collect.sh")[0])
        common.shellcall("cd rhui-tests/ && rm -f results")
        pytest.fail(msg="Test %s failed!" % testname)
