import os
import unittest

import psycopg2
from sshtunnel import SSHTunnelForwarder
from sshtunnel import BaseSSHTunnelForwarderError
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pyvirtualdisplay import Display


SSH = {
    'hostname': '146.185.143.168',
    'port': 22,
    'username': 'root',
    'password': 'testQA2019'
}

DATABASE = {
    'host': '127.0.0.1',
    'port': 5432,
    'user': 'mantisbt',
    'password': 'mantisbt2019',
    'db': 'mantisbt',
}

SITE = {
    'url_login': 'http://146.185.143.168',
    'url_test': 'http://146.185.143.168/manage_user_page.php',
    'url_logout': 'http://146.185.143.168/logout_page.php',
    'username': 'administrator',
    'password': 'mantisbt2019',
}


class Test1(unittest.TestCase):
    """Test for ex. 1."""

    # Compare answers in separated test
    data_database = None
    data_site = None

    def setUp(self):
        """Prepare test."""
        self.display = Display(visible=0, size=(1366, 768))
        self.display.start()

        chrome_driver_path = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), '..', 'chromedriver')
        self.driver = webdriver.Chrome(chrome_driver_path)

    def tearDown(self):
        """Finish test."""
        self.driver.close()
        self.driver.quit()
        self.display.stop()

    def test_database(self):
        """Test data parse from remoted database."""
        try:
            # create ssh-tunnel for connectd
            with SSHTunnelForwarder(
                    (SSH['hostname'], SSH['port']),
                    ssh_password=SSH['password'],
                    ssh_username=SSH['username'],
                    remote_bind_address=(DATABASE['host'], DATABASE['port']),
                    local_bind_address=('localhost', 6543)) as tunnel:

                self.assertEqual(tunnel.is_active, True)

                # create database connection and fetch data
                with psycopg2.connect(database=DATABASE['db'],
                                      user=DATABASE['user'],
                                      password=DATABASE['password'],
                                      host=tunnel.local_bind_host,
                                      port=tunnel.local_bind_port) as conn:

                    curs = conn.cursor()
                    curs.execute('''SELECT username, email
                                    FROM mantis_user_table
                                    WHERE enabled IS TRUE;''')
                    rows = curs.fetchall()

                    self.assertIsNotNone(rows)

                    # store answer for separated test
                    self.__class__.data_database = sorted(
                        rows, key=lambda x: x[0])

        except (BaseSSHTunnelForwarderError,):
            assert False, 'Invalid ssh credentials'

        except (psycopg2.OperationalError):
            assert False, 'Invalid database credentials'

    def test_host_web(self):
        """Test data parse from site (quick way)."""
        self.driver.get(SITE['url_test'])

        # login
        elem = self.driver.find_element_by_name("username")
        elem.clear()
        elem.send_keys(SITE['username'])
        elem.send_keys(Keys.RETURN)

        elem = self.driver.find_element_by_name("password")
        elem.clear()
        elem.send_keys(SITE['password'])
        elem.send_keys(Keys.RETURN)

        # selector for target tbody
        _ = '''#main-container > div.main-content > div.page-content > div > div >
        div.widget-box.widget-color-blue2 > div.widget-body >
        div.widget-main.no-padding > div > table > tbody'''

        # waiting for load dom-element (tbody)
        tbody = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, _))
        )

        # collect users data
        def get_users(rows=tbody.find_elements(By.TAG_NAME, "tr")):
            for row in rows:
                yield (row.find_elements(By.TAG_NAME, "td")[0].text,
                       row.find_elements(By.TAG_NAME, "td")[2].text
                       )

        rows = sorted([x for x in get_users()], key=lambda x: x[0])
        self.assertIsNotNone(rows)

        # store answer for separated test
        self.__class__.data_site = rows
        self.driver.get(SITE['url_logout'])

    def test_host_web_full_flow(self):
        """Test data parse from site (with login page before)."""
        self.driver.get(SITE['url_login'])

        # login
        elem = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.NAME, "username"))
        )
        elem.clear()
        elem.send_keys(SITE['username'])
        elem.send_keys(Keys.RETURN)

        # password
        elem = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.NAME, "password"))
        )
        elem.clear()
        elem.send_keys(SITE['password'])
        elem.send_keys(Keys.RETURN)

        # waiting for load users load page and fetch data
        self.driver.get(SITE['url_test'])
        _ = '''#main-container > div.main-content > div.page-content > div > div >
        div.widget-box.widget-color-blue2 > div.widget-body >
        div.widget-main.no-padding > div > table > tbody'''

        # waiting for load dom-element (tbody)
        tbody = WebDriverWait(self.driver, 10).until(
            ec.presence_of_element_located((By.CSS_SELECTOR, _))
        )

        # collect users data
        def get_users(rows=tbody.find_elements(By.TAG_NAME, "tr")):
            for row in rows:
                yield (row.find_elements(By.TAG_NAME, "td")[0].text,
                       row.find_elements(By.TAG_NAME, "td")[2].text
                       )

        rows = [x for x in get_users()]
        self.assertIsNotNone(rows)

        self.driver.get(SITE['url_logout'])

    def test_results(self):
        """Compare sorted answers from database and site."""
        self.assertCountEqual(self.__class__.data_database,
                              self.__class__.data_site)


if __name__ == '__main__':
    unittest.main(failfast=True)
