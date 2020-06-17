"""
Copyright ©2020. The Regents of the University of California (Regents). All Rights Reserved.

Permission to use, copy, modify, and distribute this software and its documentation
for educational, research, and not-for-profit purposes, without fee and without a
signed licensing agreement, is hereby granted, provided that the above copyright
notice, this paragraph and the following two paragraphs appear in all copies,
modifications, and distributions.

Contact The Office of Technology Licensing, UC Berkeley, 2150 Shattuck Avenue,
Suite 510, Berkeley, CA 94720-1620, (510) 643-7201, otl@berkeley.edu,
http://ipira.berkeley.edu/industry-info for commercial licensing opportunities.

IN NO EVENT SHALL REGENTS BE LIABLE TO ANY PARTY FOR DIRECT, INDIRECT, SPECIAL,
INCIDENTAL, OR CONSEQUENTIAL DAMAGES, INCLUDING LOST PROFITS, ARISING OUT OF
THE USE OF THIS SOFTWARE AND ITS DOCUMENTATION, EVEN IF REGENTS HAS BEEN ADVISED
OF THE POSSIBILITY OF SUCH DAMAGE.

REGENTS SPECIFICALLY DISCLAIMS ANY WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE
SOFTWARE AND ACCOMPANYING DOCUMENTATION, IF ANY, PROVIDED HEREUNDER IS PROVIDED
"AS IS". REGENTS HAS NO OBLIGATION TO PROVIDE MAINTENANCE, SUPPORT, UPDATES,
ENHANCEMENTS, OR MODIFICATIONS.
"""
from diablo.lib.util import email_subject_line, get_names_of_days, readable_join
from flask import current_app as app
from tests.util import override_config


class TestUtils:

    def test_email_subject_line_in_test(self):
        assert email_subject_line('Surfer Rosa') == '[diablo-test] Surfer Rosa'

    def test_email_subject_line_in_prod(self):
        with override_config(app, 'EB_ENVIRONMENT', 'diablo-prod'):
            assert email_subject_line('Trompe le Monde') == 'Trompe le Monde'

    def test_full_day_names(self):
        assert get_names_of_days([]) == []
        assert get_names_of_days(['mon', 'wed', 'fri']) == ['Monday', 'Wednesday', 'Friday']
        assert get_names_of_days(['TU', 'TH']) == ['Tuesday', 'Thursday']
        assert get_names_of_days(['Tuesday', 'Thursday', 'Payday']) == ['Tuesday', 'Thursday', None]

    def test_readable_join(self):
        assert readable_join(None) == ''
        assert readable_join([]) == ''
        assert readable_join(['Moe']) == 'Moe'
        assert readable_join(['Moe', 'Larry']) == 'Moe and Larry'
        assert readable_join(['Moe', 'Larry', 'Curly']) == 'Moe, Larry and Curly'
