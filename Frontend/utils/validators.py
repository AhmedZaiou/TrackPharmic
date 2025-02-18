import re
from qtpy.QtGui import QValidator


class PhoneValidator(QValidator):
    def validate(self, input_text, pos):
        if input_text.isdigit() and (7 <= len(input_text) <= 15):
            return QValidator.Acceptable, input_text, pos
        elif input_text == "" or input_text.isdigit():
            return QValidator.Intermediate, input_text, pos
        else:
            return QValidator.Invalid, input_text, pos


class EmailValidator(QValidator):
    EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]*$")

    def validate(self, input_text, pos):
        if not input_text:
            return QValidator.Intermediate, input_text, pos

        if self.EMAIL_REGEX.fullmatch(input_text):
            return QValidator.Acceptable, input_text, pos

        if "@" in input_text and "." in input_text:
            return QValidator.Intermediate, input_text, pos

        return QValidator.Intermediate, input_text, pos
