

from lib.extractors.corenlp import Converter


r_name = "per:employee_or_member_of"

a_r_name = Converter.convert_to_simplified_relation_name(r_name)

print(r_name, " -> ", a_r_name)

