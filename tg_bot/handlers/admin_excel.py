from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from aiogram.types import InputFile
from openpyxl import Workbook
from openpyxl.styles import Font
from tg_bot.DBSM import fetchall
import os

admin_ids = [1446691883, 1842494556] 

def register_excel(dp: Dispatcher):
    dp.register_message_handler(excel_review, lambda message: message.from_user.id in admin_ids, commands=["excel"])


async def excel_review(message: types.Message, state: FSMContext):
    wb = Workbook()
    wb.remove(wb["Sheet"])
    sheet = wb.create_sheet("Заявки", 0)
    data = fetchall()
    sheet["A1"] = "Номер"
    sheet['A1'].font = Font(color="FF0000")  
    sheet["B1"] = "ФИО"
    sheet['B1'].font = Font(color="FF0000")  
    sheet["C1"] = "Адрес"
    sheet['C1'].font = Font(color="FF0000") 
    sheet["D1"] = "Телефон"
    sheet['D1'].font = Font(color="FF0000")
    sheet["E1"] = "Категория"
    sheet['E1'].font = Font(color="FF0000")   
    sheet["F1"] = "Комментарий"
    sheet['F1'].font = Font(color="FF0000")    
    sheet["G1"] = "Работник"
    sheet['G1'].font = Font(color="FF0000")  
    sheet["H1"] = "Заказ"
    sheet['H1'].font = Font(color="FF0000") 
    sheet["I1"] = "Фото замера"
    sheet['I1'].font = Font(color="FF0000")  
    sheet["J1"] = "Дата добавления"
    sheet['J1'].font = Font(color="FF0000")  

    for i in range(len(data)):
        sheet[f"A{i+2}"] = data[i]["id"]
        sheet[f"B{i+2}"] = data[i]["name"]
        sheet[f"C{i+2}"] = data[i]["adress"]
        sheet[f"D{i+2}"] = data[i]["phone"]
        sheet[f"E{i+2}"] = data[i]["cat"]
        sheet[f"F{i+2}"] = data[i]["comment"]
        sheet[f"G{i+2}"] = f'@{data[i]["worker"]}'
        sheet[f"H{i+2}"] = data[i]["order"]
        sheet[f"I{i+2}"] = data[i]["zamer"]
        sheet[f"J{i+2}"] = data[i]["date"]

    
    if not os.path.isdir("tg_bot/excel"):
        os.mkdir("tg_bot/excel")
    wb.save("tg_bot/excel/Отчет.xlsx")
    await message.answer_document(document= InputFile("tg_bot/excel/Отчет.xlsx"))
    


