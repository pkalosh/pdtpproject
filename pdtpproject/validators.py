from django.core.exceptions import ValidationError
def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf']
    if not ext in valid_extensions:
        raise ValidationError(u'Unsupported file extension. Kindly upload PDF files only.')

def valid_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.xls','.xlsx',]
    if not ext in valid_extensions:
        raise ValidationError(u'Unsupported file extension.Please Upload an Excel File')
