def contact(row):
    no = str(row['CONTACT'])
    if no[0] == '2':
        return "+" + no
    else:
        return "+234" + no
    
def startsandendswith(main_str):
    return main_str.startswith("*") and main_str.endswith("*")