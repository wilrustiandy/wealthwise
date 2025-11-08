def get_form_errors(form_errors):
    error_list = []
    for field, errors in form_errors.items():
        for error in errors:
            error_list.append(f"{field.capitalize()}: {error}")
    return "<br>".join(error_list)