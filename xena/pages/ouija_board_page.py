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

import time

from flask import current_app as app
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait as Wait
from xena.pages.diablo_pages import DiabloPages
from xena.test_utils import util


class OuijaBoardPage(DiabloPages):
    SEARCH_INPUT = (By.ID, 'input-search')
    SEARCH_SELECT_BUTTON = (By.XPATH, '//div[@aria-haspopup="listbox"]')
    SEARCH_SELECT_SELECTION = (By.XPATH, '//input[@id="ouija-filter-options"]/preceding-sibling::div')
    SEARCH_SELECT_OPTION = (By.XPATH, '//div[@role="listbox"]/div[@role="option"]//div[contains(@class, "title")]')

    FILTER_ALL_OPTION = (By.XPATH, '//div[@role="option"][contains(., "All")]')
    FILTER_DO_NOT_EMAIL_OPTION = (By.XPATH, '//div[@role="option"][contains(., "Do Not Email")]')
    FILTER_INVITED_OPTION = (By.XPATH, '//div[@role="option"][contains(., "Invited")]')
    FILTER_NOT_INVITED_OPTION = (By.XPATH, '//div[@role="option"][contains(., "Not Invited")]')
    FILTER_PARTIALLY_APPROVED_OPTION = (By.XPATH, '//div[@role="option"][contains(., "Partially Approved")]')
    FILTER_SCHEDULED_OPTION = (By.XPATH, '//div[@role="option"][contains(., "Scheduled")]')

    NO_RESULTS_MSG = (By.ID, 'message-when-zero-courses')

    COURSE_ROW = (By.XPATH, '//div[@id="courses-data-table"]//tbody/tr')

    def load_page(self):
        app.logger.info('Loading the Ouija Board')
        self.driver.get(f'{app.config["BASE_URL"]}/ouija')
        self.wait_for_ouija_title()

    def wait_for_ouija_title(self):
        self.wait_for_diablo_title('Ouija Board')

    # SEARCH AND FILTER

    @staticmethod
    def search_courses_option_xpath(status):
        return f'//div[@role="listbox"]/div[@role="option"]//div[contains(@class, "title")][text()="{status}"]'

    def search_for_string(self, string, status):
        app.logger.info(f'Searching courses for {string} with status {status}')
        self.wait_for_element_and_type(OuijaBoardPage.SEARCH_INPUT, string)
        self.wait_for_element_and_click(OuijaBoardPage.SEARCH_SELECT_BUTTON)
        self.wait_for_element_and_click((By.XPATH, self.search_courses_option_xpath(status)))

    def search_for_course_code(self, section):
        app.logger.info(f'Searching for course code {section.code}')
        self.wait_for_element_and_type(OuijaBoardPage.SEARCH_INPUT, section.code)
        time.sleep(1)

    def filter_for_option(self, opt_locator):
        if not self.is_present(opt_locator) or not self.element(opt_locator).is_displayed():
            self.wait_for_element_and_click(OuijaBoardPage.SEARCH_SELECT_BUTTON)
        self.wait_for_element_and_click(opt_locator)
        time.sleep(2)
        self.wait_for_filter_search()

    def wait_for_filter_search(self):
        results = OuijaBoardPage.COURSE_ROW
        no_results = OuijaBoardPage.NO_RESULTS_MSG
        Wait(self.driver, util.get_long_timeout()).until(
            ec.visibility_of_any_elements_located(results) or ec.visibility_of_element_located(no_results),
        )
        time.sleep(2)

    def is_course_in_results(self, section):
        return self.is_present(OuijaBoardPage.course_row_locator(section))

    def filter_for_all(self):
        app.logger.info('Filtering by option All')
        self.filter_for_option(OuijaBoardPage.FILTER_ALL_OPTION)

    def filter_for_do_not_email(self):
        app.logger.info('Filtering by option Do Not Email')
        self.filter_for_option(OuijaBoardPage.FILTER_DO_NOT_EMAIL_OPTION)

    def filter_for_invited(self):
        app.logger.info('Filtering by option Invited')
        self.filter_for_option(OuijaBoardPage.FILTER_INVITED_OPTION)

    def filter_for_not_invited(self):
        app.logger.info('Filtering by option Not Invited')
        self.filter_for_option(OuijaBoardPage.FILTER_NOT_INVITED_OPTION)

    def filter_for_partially_approved(self):
        app.logger.info('Filtering by option Partially Approved')
        self.filter_for_option(OuijaBoardPage.FILTER_PARTIALLY_APPROVED_OPTION)

    def filter_for_scheduled(self):
        app.logger.info('Filtering by option Scheduled')
        self.filter_for_option(OuijaBoardPage.FILTER_SCHEDULED_OPTION)

    # COURSES

    @staticmethod
    def course_row_locator(section):
        return By.XPATH, f'//tr[contains(., "{section.code}")]'

    def wait_for_course_results(self):
        Wait(self.driver, util.get_short_timeout()).until(
            ec.visibility_of_any_elements_located(OuijaBoardPage.COURSE_ROW),
        )

    def wait_for_course_result(self, section):
        Wait(self.driver, util.get_short_timeout()).until(
            ec.visibility_of_element_located(OuijaBoardPage.course_row_locator(section)),
        )

    def course_row_link(self, section):
        return self.element((By.ID, f'link-course-{section.ccn}'))

    def course_row_code_el(self, section):
        return self.element((By.XPATH, f'//tr[@id="{section.ccn}"]/td[2]'))

    def course_row_title_el(self, section):
        return self.element((By.XPATH, f'//tr[@id="{section.ccn}"]/td[3]'))

    def course_row_instructors_el(self, section):
        return self.element((By.XPATH, f'//tr[@id="{section.ccn}"]/td[4]'))

    def course_row_room_el(self, section):
        return self.element((By.XPATH, f'//tr[@id="{section.ccn}"]/td[5]'))

    def course_row_days_el(self, section):
        return self.element((By.XPATH, f'//tr[@id="{section.ccn}"]/td[6]'))

    def course_row_time_el(self, section):
        return self.element((By.XPATH, f'//tr[@id="{section.ccn}"]/td[7]'))

    def course_row_status_el(self, section):
        return self.element((By.ID, f'course-{section.ccn}-status'))

    def click_sign_up_page_link(self, section):
        app.logger.info(f'Clicking the link to the sign up page for {section.code}')
        self.wait_for_page_and_click((By.ID, f'link-course-{section.ccn}'))
