import pandas as pd
import re
import argparse

from helper_function import startsandendswith,contact


def main(params):

    file_name = params.file_name

    if not file_name.endswith('.xlsx'):
        return f"Can only accept source files in excel format, for the moment"
    
    data = pd.read_excel(file_name,header=None)
    
    l = ['message','Done','Transfer','(Minus','Cancelled','Cash','*20/05/21*','No']
    
    orders = []
    carts = []
    cleaned_orders = []
    delivery_time = []
    ordered_time = []
    amount = []
    location = []
    phone_no = []
    name = []
    date = []
    item = []

    for row in data[0]:
        if isinstance(row,int):
            carts.append(row)
        elif any(map(lambda x:x in l,row.split())):
           pass
        elif not startsandendswith(row):
            carts.append(row)
        else:
            carts.append(row)
            orders.append(carts)
            carts = []
   
    
    for order in orders:
        if 'EDITED' not in order[0] and 'Edited' not in order[0]:
            cleaned_orders.append(order)
            
    

    for features in cleaned_orders:
        delivery_time.append(re.sub('[*]+', '', features[-1]))
        ordered_time.append(features[0].split(' ')[1])
        amount.append(re.sub("[^\d\.]", "", features[-2]))
        location.append(features[-3])
        phone_no.append(features[-4])
        name.append(features[-5])
        date.append(re.sub('[,]+', '', features[0].split(' ')[0]))
        item.append(','.join(features[1:-5]))
        
        
    table = pd.DataFrame(list(zip(date, ordered_time,item,location,name,phone_no,amount,delivery_time)),
               columns =['DATE','ORDER TIME','ITEM','ADDRESS','NAME','CONTACT','AMOUNT','DELIVERY TIME'])
    
    table['CONTACT'] = table.apply(lambda row: contact(row), axis=1)
    
    with pd.ExcelWriter('tabular_sendme_data.xlsx') as writer:
            table.to_excel(writer, sheet_name = 'sheet1', index = True)
            
    print(f"successfully converted {file_name} to a tabular form")


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='convert raw data to tabular form')


    parser.add_argument('--file_name',help="path/name of the file")
   

    args = parser.parse_args()
    

    main(args)
