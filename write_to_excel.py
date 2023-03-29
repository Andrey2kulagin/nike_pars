import openpyxl


def get_product_row(card_data, last_row):
    data_row = []
    data_row.append(card_data['model_sub_name'])
    data_row.append("Товар")
    product_number = str(last_row)
    data_row.append(product_number)
    data_row.append(card_data["model_main_name"])
    photo_string = link_array_to_string(card_data["photos"])
    data_row.append(photo_string)
    data_row.append("")
    data_row.append(card_data["price"])
    data_row.append("доллар")
    data_row.append("")
    data_row.append("")
    return data_row


def link_array_to_string(link_array):
    link_str = ""
    for link in link_array:
        link_str += (link + ' ; ')
    return link_str


def write_excel_row(data_row, last_row, worksheet):
    for col_idx, cell_value in enumerate(data_row, start=1):
        worksheet.cell(row=last_row + 1, column=col_idx, value=cell_value)


def get_size_color_row(size, last_row, main_product_num, article, photos):
    data_row = [""]
    data_row.append("Модификация")
    data_row.append(str(last_row))
    data_row.append("")
    photo_string = link_array_to_string(photos)
    data_row.append(photo_string)
    data_row.append(article)
    data_row.append("")
    data_row.append("")
    data_row.append(str(main_product_num))
    data_row.append(size)
    return data_row


def write_to_file(cards_data):
    workbook = openpyxl.load_workbook('cards_data.xlsx')
    worksheet = workbook.active
    last_row = worksheet.max_row
    main_product_num = None
    is_product_add = False
    for card_data in cards_data:
        if not is_product_add:
            data_row = get_product_row(cards_data[card_data], last_row)
            write_excel_row(data_row, last_row, worksheet)
            main_product_num = last_row
            last_row += 1
            is_product_add = True
        if len(cards_data[card_data]["size"]):
            # обработка всех размеров и их запись
            for size in cards_data[card_data]["size"]:
                data_row = get_size_color_row(size, last_row, main_product_num)
                write_excel_row(data_row, last_row, worksheet)
                last_row += 1
        # Сохраняем файл
    workbook.save('cards_data.xlsx')

