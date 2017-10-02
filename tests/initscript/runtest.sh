#!/bin/bash
# vim: dict=/usr/share/rhts-library/dictionary.vim cpt=.,w,b,u,t,i,k
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   runtest.sh of /CoreOS/at/Sanity/initscript
#   Description: Initscript sanity
#   Author: Radek Biba <rbiba@redhat.com>
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#   Copyright (c) 2009 Red Hat, Inc. All rights reserved.
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

# Include rhts environment
. /usr/bin/rhts-environment.sh
. /usr/share/rhts-library/rhtslib.sh

PACKAGE="at"
SERVICE="atd"

rlJournalStart
    rlPhaseStartSetup "Prepare"
        rlServiceStop $SERVICE
    rlPhaseEnd
    if rlIsRHEL "<7"; then
        rlPhaseStartTest "Mandatory actions"
            for ACTION in "start" "stop" "restart" "force-reload" "status" ; do
                rlRun "grep -i \"usage.*$ACTION\" /etc/init.d/$SERVICE"
            done
        rlPhaseEnd
    fi
    rlPhaseStartTest "Start"
        rlRun "service $SERVICE start" 0
        rlRun "service $SERVICE status" 0
        rlRun "service $SERVICE start" 0
        rlRun "service $SERVICE status" 0
        rlRun "service $SERVICE restart" 0
        rlRun "service $SERVICE status" 0
        rlRun "service $SERVICE force-reload" 0
        rlRun "service $SERVICE status" 0
        rlRun "service $SERVICE try-restart" 0
        rlRun "service $SERVICE status" 0
    rlPhaseEnd
    rlPhaseStartTest "Stop"
        rlRun "service $SERVICE stop" 0
        rlRun "service $SERVICE status" 3
        rlRun "service $SERVICE stop" 0
        rlRun "service $SERVICE status" 3
        rlRun "service $SERVICE try-restart" 0
        rlRun "service $SERVICE status" 3
    rlPhaseEnd
    rlPhaseStartTest "Dead service"
        rlRun "touch /var/lock/subsys/$SERVICE"
        rlRun "service $SERVICE status" $(
                    if rlIsRHEL "<7"; then
                        echo 2;
                    else
                        echo 3;
                    fi
                )
        rlRun "service $SERVICE start" 0
        rlRun "service $SERVICE status" 0
    rlPhaseEnd
    rlPhaseStartTest "Invalid arguments"
        rlRun "service $SERVICE" 2
        rlRun "service $SERVICE fubar" 2
    rlPhaseEnd

    rlPhaseStartCleanup "Restore"
        rlServiceRestore $SERVICE
    rlPhaseEnd
rlJournalPrintText
rlJournalEnd
