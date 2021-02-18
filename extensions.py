from schematics.exceptions import ValidationError
from schematics.types import StringType as SchematicsStringType


class StringType(SchematicsStringType):
    MESSAGES = {
        'convert': "Couldn't interpret '{0}' as string.",
        'decode': "Invalid UTF-8 data.",
        'max_length': "should be less than {0} characters.",
        'min_length': "must be at least {0} characters.",
        'regex': "String value did not match validation regex.",
    }

    def validate_length(self, value, context=None):
        length = len(value)
        if self.max_length is not None and length > self.max_length:
            raise ValidationError(self.messages['max_length'].format(self.max_length))

        if self.min_length is not None and length < self.min_length:
            raise ValidationError(self.messages['min_length'].format(self.min_length))
