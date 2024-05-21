from services.JudicialProceedingsScrapingService import JudicialProceedingsScrapingService as SJPS

class JudicialProceedingsScrapingController:
    def __init__(self):
        self.scraper = SJPS()

    def fill_form_and_submmit(self, process_data : dict):
        """
            Method in charge of searching and extracting the records associated with the
            identifier and type of person received.

            Parameters:
                - Dictionary with the identification of the plaintiff or defendant
                and the type of person (1 = Plaintiff, 2 = Defendant)

            Return:
                - Data found in the search
                - In case of an error, the exception is returned
        """
        try:
            return self.scraper.fill_form(process_data)

        except Exception as error:
            return error