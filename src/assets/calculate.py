import src.assets.dicts as dicts

def snp_type_calculate(snp_list):
    for type, list  in dicts.snps_dict.items():
        if list == snp_list:
            return type

def snp_sub_type_calculate(snp_sub_list):
    for type, list  in dicts.snp_sub_type_dict.items():
        if list == snp_sub_list:
            return type
