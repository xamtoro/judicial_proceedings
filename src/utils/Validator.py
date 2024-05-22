from jsonschema import validate, ValidationError
from os import getenv
import json

class Validator:

    @classmethod
    def validate_data(cls, data : dict, option : str):
        """
            Method responsible for validating input data.

            Parameters:
                - data : dictionary
                - option : string

            Returns:
                - Raises a ValidationError exception
        """

        messages = {
            "type": "El campo {} debe ser de tipo {}.",
            "required": "El campo {} es requerido.",
            "minLength" : "El campo {} debe tener como mínimo {} caracteres.",
            "maxLength" : "El campo {} debe tener como máximo {} caracteres.",
            "pattern" : "El campo {} no cumple con el formato de correo electrónico.",
            "pattern_v2" : "El campo {} no puede ser numerico ni alfanumerico.",
            "enum" : "El campo {} debe tener un valor entre 0 y 1.",
            "minimum" : "El campo {} no puede ser menor de {} digitos.",
            "maximum" : "El campo {} no puede ser mayor a {} digitos.",
            "maxItems" : "El campo {} solo tiene permitido 3 items."
        }

        with open(getenv("JSONSCHEMA_PATH")) as file:
            schema = json.loads(file.read())
            file.close()

        try:
            payload = cls.transform_data(data)
            validate(payload, schema[option])
            return payload

        except ValidationError as e:
            field = ".".join(map(str, e.path))

            if e.validator == "required":
                error = messages["required"].format(e.message.split("'")[1])

            elif e.validator == "minimum":
                error = messages["minimum"].format(field, e.schema["minimum"])

            elif e.validator == "maximum":
                error = messages["maximum"].format(field, e.schema["maximum"])

            elif e.validator == "enum":
                error = messages["enum"].format(field)

            elif e.validator == "format":
                error = messages["format"].format(field)

            elif e.validator == "pattern":

                if field != "email":
                    error = messages["pattern_v2"].format(field)
                else:
                    error = messages["pattern"].format(field)

            elif e.validator == "minLength":
                error = messages["minLength"].format(field, e.schema["minLength"])

            elif e.validator == "maxLength":
                error = messages["maxLength"].format(field, e.schema["maxLength"])

            elif e.validator == "type":
                error = messages["type"].format(field, e.schema["type"])

            elif e.validator == "maxItems":
                error = messages["maxItems"].format(field)

            raise ValidationError(error)

    @classmethod
    def transform_data(cls, data) -> dict:
        """
            Method responsible for validating if the data comes from a form or JSON.

            Parameters:
                - data: form or JSON

            Return:
                - Dictionary containing the data

            Returns:
                - dict: Data in dictionary form
        """

        try:
            # Check if the data comes from a JSON request
            if data.headers.get('Content-Type') == 'application/json':
                payload = data.get_json()

            elif data.headers.get('Content-Type') in ['application/x-www-form-urlencoded', 'multipart/form-data']:
                data = data.form
                payload = dict(map(lambda key: (key, data[key]), filter(lambda key: True, data.keys())))

            else:
                raise ValidationError("Content-Type not supported")

            return payload

        except ValidationError as error:
            raise Exception(error)

    @classmethod
    def validate_type_error(cls, error) -> str:
        """
            Method in charge of validating the type of error in order to return a message to the view.

            Parameters:
                - error: Error that has occurred

            Return:
                - Error message
        """
        try:
            if "ValidationError" in f"{type(error)}":
                return "¡Por favor ingresa los datos correctamente!"
            else:
                print(error)
                return "¡Ups! ha ocurrido un error inesperado"

        except Exception as error:
            raise error