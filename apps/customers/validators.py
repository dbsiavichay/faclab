from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def code_validator(code):
    code_long = len(code)
    province_code = int(code[:2])
    province_ok = province_code in range(1, 25) or province_code == 30
    long_ok = code_long in (10, 13)
    is_valid = False

    if province_ok and long_ok:
        third_digit = int(code[2])
        natural = code_long == 10
        public = code_long == 13 and third_digit == 6
        private = code_long == 13 and third_digit == 9
        base = 10 if natural else 11
        coefficients = (2, 1, 2, 1, 2, 1, 2, 1, 2)

        if public:
            coefficients = (3, 2, 7, 6, 5, 4, 3, 2)
        elif private:
            coefficients = (4, 3, 2, 7, 6, 5, 4, 3, 2)

        checker = len(coefficients)

        total = 0

        for i, value in enumerate(coefficients):
            p = int(code[i]) * value

            if natural:
                total += p if p < 10 else int(str(p)[0]) + int(str(p)[1])
            else:
                total += p

        module = total % base
        result = base - module if module != 0 else 0

        is_valid = result == checker

    if not is_valid:
        raise ValidationError(
            _("%(value)s is not a valid value"),
            params={"value": code},
        )
