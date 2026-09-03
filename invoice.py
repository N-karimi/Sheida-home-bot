import openpyxl
from DQL import get_users, get_cart_shopping, get_cart_item, get_product_info


def create_invoice(cid):
    wb = openpyxl.load_workbook('factor.xlsm', keep_vba=True)
    sheet = wb['Invoice']

# اطلاعات مشتری
    user = get_users(cid)
    sheet['D10'].value = user['first_name']
    sheet['I12'].value = user['phone']
    sheet['C14'].value = user['address']

# سبد خرید
    cart = get_cart_shopping(cid)
    if not cart:
        wb.close()
        return None
    items = get_cart_item(cart['id'])
    if not items:
        wb.close()
        return None

# اولین ردیف محصولات
    pid_first_row = 18
    total_price = 0

# آوردن محصولات از Database
    for i in range(len(items)):
        item = items[i]
        product = get_product_info(item['prod_id'])
        row = pid_first_row + i
        name = product['name']
        number = item['number']
        price = int(product['price'])
        sheet[f'C{row}'].value = name
        sheet[f'F{row}'].value = number
        sheet[f'H{row}'].value = price
        item_total = number * price
        sheet[f'I{row}'].value = item_total
        total_price += item_total

# جمع کل
    sheet['I38'].value = total_price

# قابل پرداخت
    sheet['I41'].value = total_price

# ذخیره فاکتور
    file_name = f'invoice_{cid}.xlsm'

    wb.save(file_name)
    wb.close()

    return file_name