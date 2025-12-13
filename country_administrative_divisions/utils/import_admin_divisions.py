import frappe
import csv
import os

BASE_PATH = frappe.get_site_path("private", "files", "admin_divisions")


def get_country_by_iso(iso_code):
    country = frappe.db.get_value(
        "Country",
        {"code": iso_code.upper()},
        "name"
    )
    if not country:
        frappe.throw(f"Country ISO not found: {iso_code}")
    return country


def import_country(country_folder):
    level_1_file = f"{BASE_PATH}/{country_folder}/level_1.csv"
    level_2_file = f"{BASE_PATH}/{country_folder}/level_2.csv"

    import_admin_level_1(level_1_file)
    import_admin_level_2(level_2_file)


def import_admin_level_1(file_path):
    with open(file_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            country = get_country_by_iso(row["country_iso"])

            if not frappe.db.exists(
                "Admin Level 1 Province_Region_State",
                {
                    "country_id": country,
                    "province_region_state": row["province_region_state"],
                },
            ):
                frappe.get_doc({
                    "doctype": "Admin Level 1 Province_Region_State",
                    "country_id": country,
                    "province_region_state": row["province_region_state"],
                }).insert(ignore_permissions=True)

    frappe.db.commit()


def import_admin_level_2(file_path):
    with open(file_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            country = get_country_by_iso(row["country_iso"])

            parent = frappe.db.get_value(
                "Admin Level 1 Province_Region_State",
                {
                    "country_id": country,
                    "province_region_state": row["province_region_state"],
                },
                "name",
            )

            if not parent:
                frappe.throw(
                    f"Missing Admin Level 1: {row['province_region_state']} ({country})"
                )

            if not frappe.db.exists(
                "Admin Division Level 2 Districts_County_City_Town",
                {
                    "admin_division_level_1": parent,
                    "district_county_city_town": row["district_county_city_town"],
                },
            ):
                frappe.get_doc({
                    "doctype": "Admin Division Level 2 Districts_County_City_Town",
                    "admin_division_level_1": parent,
                    "district_county_city_town": row["district_county_city_town"],
                }).insert(ignore_permissions=True)

    frappe.db.commit()
