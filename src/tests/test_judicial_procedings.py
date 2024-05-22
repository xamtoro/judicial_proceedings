from services.JudicialProceedingsScrapingService import JudicialProceedingsScrapingService as JP
from utils.Validator import Validator
from jsonschema import ValidationError

def test_unsuccessful_search():
    """
    This test verifies that the `fill_form` method of the `JudicialProceedingsScrapingService class
    submits the form but finds no records.
    """
    jp = JP()

    process_data = {
        "person_type": "1",
        "identifier": "12345678690"
    }

    result = jp.fill_form(process_data)

    assert isinstance(result, dict)

def test_successful_search():
    """
    This test verifies that the `fill_form` method of the `JudicialProceedingsScrapingService` class
    correctly processes the form data and returns the search results as a list.
    """
    jp = JP()

    process_data = {
        "person_type": "2",
        "identifier": "0992339411001"
    }

    result = jp.fill_form(process_data)

    assert isinstance(result, list)

def test_download_json_file():
    """
    This test verifies that the `download_json_file` method can correctly
    download a JSON file with the provided data and save it to the default
    downloads folder without throwing any exceptions.
    """
    data = [{"message": "should be downloaded in downloads"}]
    result = JP.download_json_file(data)
    assert result is None

def test_download_json_file_error():
    """
    This test verifies that the `download_json_file` method handles errors correctly
    when attempting to download a JSON file. The test expects that an error occurs,
    resulting in the method returning an exception or error message instead of None.
    """
    data = [{"message": "Should not be downloaded"}]
    result = JP.download_json_file(data, "/test")

    assert result is not None

def test_error_message():
    """
    This test validates that the `validate_type_error` method correctly returns
    the error message when invalid data is provided.
    """
    data = ValidationError("This is an intentional error")
    result = Validator.validate_type_error(data)

    assert result == "¡Por favor ingresa los datos correctamente!"