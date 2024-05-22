from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time, json, os
from os import getenv
from typing import Optional

class JudicialProceedingsScrapingService:

    def __init__(self):
        # Configure Chrome options
        self.chrome_options = Options()
        self.chrome_options.add_argument(getenv("USER_AGENT"))
        self.chrome_options.add_argument("--headless")

        # Configure the WebDriver using webdriver-manager
        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=self.chrome_options)

    def fill_form(self, process_data: dict) -> list:
        """
            Method responsible for submitting the search form data and obtaining the
            search results.

            Parameters:
                - Dictionary with the identification of the plaintiff or defendant
                and the type of person (1 = Plaintiff, 2 = Defendant)

            Return:
                - Data collected from the search
                - In case of an error, the exception is returned
        """

        try:
            # Open the web page
            self.driver.get(
                'https://procesosjudiciales.funcionjudicial.gob.ec/busqueda-filtros'
            )

            # Determine which input field to use based on person type
            if process_data["person_type"] == "1":
                input_actor = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'mat-input-1'))
                )

            elif process_data["person_type"] == "2":
                input_actor = WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.ID, 'mat-input-3'))
                )

            else:
                self.close_browser()

                return Exception("¡Seleccione un tipo de persona correcta!")

            input_actor.send_keys(process_data["identifier"])

            submit_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//button[contains(@class, "boton-buscar") and @type="submit"]')
                )
            )

            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//button[contains(@class, "boton-buscar") and @type="submit" and not(@disabled)]')
                )
            )

            submit_button.click()

            # Check for the existence of the snack-bar container indicating no results
            try:
                WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'div.cdk-overlay-container mat-snack-bar-container')
                    )
                )
                snack_bar_message = self.driver.find_element(By.CSS_SELECTOR, 'div.cdk-overlay-container mat-snack-bar-container .mat-mdc-snack-bar-label').text
                if "La consulta no devolvió resultados" in snack_bar_message:
                    self.close_browser()

                    return {"message": "La consulta no devolvió resultados."}

            except TimeoutException:
                # If the snack-bar is not found, continue to get the records
                records = self.get_records()
                self.download_json_file(records)
                return records

        except Exception as e:
            return str(e)

    def get_records(self) -> list:
        """
            Method in charge of extracting the information from the records found after sending the form.

            Parameters:
                - It does not receive parameters, it simply uses the class driver itself.

            Return:
                - Records found associated with the identification received
                - In case of an error, the exception is returned
        """
        try:
            final_data = []

            while True:
                records = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.causa-individual'))
                )

                for i in range(len(records)):
                    record_id = records[i].find_element(By.CLASS_NAME, 'id').text
                    date = records[i].find_element(By.CLASS_NAME, 'fecha').text
                    process_number = records[i].find_element(By.CLASS_NAME, 'numero-proceso').text
                    action_infraction = records[i].find_element(By.CLASS_NAME, 'accion-infraccion').text
                    detail_element = records[i].find_element(By.CSS_SELECTOR, '.detalle a')

                    time.sleep(1)
                    detail_element.click()

                    time.sleep(2)
                    details_data = self.get_details_records()

                    final_data.append({
                        "id": record_id,
                        "date": date,
                        "process_number": process_number,
                        "action_infraction": action_infraction,
                        "details": details_data
                    })

                    time.sleep(1)
                    self.driver.back()

                    records = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.causa-individual'))
                    )

                try:
                    next_button = self.driver.find_element(By.CSS_SELECTOR, '.mat-mdc-paginator-navigation-next')
                    if 'mat-mdc-button-disabled' in next_button.get_attribute('class'):
                        break

                    else:
                        next_button.click()
                        WebDriverWait(self.driver, 10).until(EC.staleness_of(records[0]))

                except NoSuchElementException:
                    break

            self.close_browser()

            return final_data

        except Exception as e:
            return str(e)

    def get_details_records(self) -> list:
        """
            Method in charge of going to each one of the detail records and obtaining it.

            Parameters:
                - It does not receive parameters, it simply uses the class driver itself.

            Return:
                - Details found associated with the register received
                - In case of an error, the exception is returned
        """
        try:
            final_data = []

            while True:
                records = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.lista-movimientos .movimiento-individual'))
                )

                for i in range(len(records)):
                    incident_number = records[i].find_element(By.CLASS_NAME, 'numero-incidente').text
                    entry_date = records[i].find_element(By.CLASS_NAME, 'fecha-ingreso').text
                    actors = records[i].find_element(By.CLASS_NAME, 'lista-actores').text
                    defendants = records[i].find_element(By.CLASS_NAME, 'lista-demandados').text
                    judicial_proceedings = records[i].find_element(By.CSS_SELECTOR, '.actuaciones-judiciales a')

                    time.sleep(1)
                    judicial_proceedings.click()

                    time.sleep(2)
                    judicial_proceedings_data = self.obtain_legal_proceedings()

                    final_data.append({
                        "id": incident_number,
                        "entry_date": entry_date,
                        "actors": actors,
                        "defendants": defendants,
                        "judicial_proceedings": judicial_proceedings_data
                    })

                    time.sleep(1)
                    self.driver.back()

                    records = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.lista-movimientos .movimiento-individual'))
                    )

                try:
                    next_button = self.driver.find_element(By.CSS_SELECTOR, '.mat-mdc-paginator-navigation-next')
                    if 'mat-mdc-button-disabled' in next_button.get_attribute('class'):
                        break

                    else:
                        next_button.click()
                        WebDriverWait(self.driver, 10).until(EC.staleness_of(records[0]))

                except NoSuchElementException:
                    break

            return final_data

        except Exception as e:
            return str(e)

    def obtain_legal_proceedings(self) -> list:
        """
            Method for obtaining the court proceedings of each detail associated with each record.

            Parameters:
                - It does not receive parameters, it simply uses the class driver itself.

            Return:
                - Judicial proceedings found associated with the detail received
                - In case of an error, the exception is returned
        """
        try:
            final_data = []

            while True:

                records = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.panel-expansion .actuaciones-judiciales'))
                )

                for record in records:
                    panels = record.find_elements(By.CLASS_NAME, 'mat-expansion-panel')

                    for panel in panels:
                        date = panel.find_element(By.CSS_SELECTOR, '.cabecera-tabla span').text
                        content = panel.find_element(By.CSS_SELECTOR, '.cabecera-tabla .title').text

                        final_data.append({"date": date, "detail" : content})

                break

            return final_data

        except Exception as e:
            return str(e)

    @classmethod
    def download_json_file(self, data : list | dict, folder = '/Downloads') -> Optional[Exception]:
        """
            Method in charge of downloading the supplied data in json form

            Parameters:
                - Data in the form of a dictionary or list, so that it can be converted to json

            Return:
                - In case of an error, the exception is returned
        """
        try:
            json_data = json.dumps(data)

            download_folder = os.path.expanduser('~') + folder

            file_path = os.path.join(download_folder, 'records_obtained.json')

            with open(file_path, 'w') as file:
                file.write(json_data)

        except Exception as e:
            return str(e)

    def close_browser(self):
        self.driver.quit()