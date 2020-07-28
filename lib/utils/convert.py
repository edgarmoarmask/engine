


class Convert:

    @staticmethod
    def ToBool(value):
        result  = value.lower() in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']
        return result


