import csv
import json
from inventory_report.reports.complete_report import CompleteReport
from inventory_report.reports.simple_report import SimpleReport
import xml.etree.ElementTree as ET


class Inventory:
    @classmethod
    def import_data(csl, file, report_type):
        file_type = file.split(".")

        if file_type[-1] == "csv":
            with open(file, 'r') as file:
                reader_csv = csv.DictReader(file, delimiter=",", quotechar='"')
                list_csv = [row_csv for row_csv in reader_csv]
                return Inventory.conditional_type(list_csv, report_type)

        elif file_type[-1] == "json":
            with open(file, 'r') as file:
                list_json = json.load(file)
                return Inventory.conditional_type(list_json, report_type)

        else:
            with open(file, 'r') as file:
                reader_xml = ET.parse(file)
                root = reader_xml.getroot()
                list_xml = []
                for item in root:
                    item_dict = {}
                    for child in item:
                        item_dict[child.tag] = child.text
                    list_xml.append(item_dict)
                return Inventory.conditional_type(list_xml, report_type)

    def conditional_type(file, report_type):
        if report_type == "simples":
            return SimpleReport.generate(file)
        else:
            return CompleteReport.generate(file)

# https://python.readthedocs.io/fr/latest/library/xml.etree.elementtree.html -
