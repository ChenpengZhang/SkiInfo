from skiField import SkiField


class SkiFields:

    def __init__(self, ski_fields: list[SkiField]):
        self.skiFields = ski_fields
        self.count = len(ski_fields)
        self.names = [field.en_name for field in ski_fields]
