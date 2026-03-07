import pandas as pd


def export_excel(data, path):

    df = pd.DataFrame(data)

    df = df[["title", "date", "content", "url"]]

    df.columns = ["Judul", "Tanggal", "Isi", "URL"]

    writer = pd.ExcelWriter(path, engine="xlsxwriter")

    df.to_excel(writer, sheet_name="Scraping", index=False)

    workbook = writer.book
    worksheet = writer.sheets["Scraping"]

    wrap = workbook.add_format({"text_wrap": True})

    worksheet.set_column("A:A", 40)
    worksheet.set_column("B:B", 20)
    worksheet.set_column("C:C", 80, wrap)
    worksheet.set_column("D:D", 50)

    writer.close()


def export_csv(data, path):

    df = pd.DataFrame(data)

    df = df[["title", "date", "content", "url"]]

    df.columns = ["Judul", "Tanggal", "Isi", "URL"]

    df.to_csv(path, index=False)