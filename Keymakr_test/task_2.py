import os
import json
import argparse
import xml.etree.ElementTree as ET


def validate_product_data(product: dict) -> dict | None:
    """Перевірка даних продукту на валідність"""
    try:
        product["id"] = int(product["id"])
        product["price"] = float(product["price"])
        if product["id"] <= 0 or product["price"] <= 0:
            raise ValueError("Id and price must be greater than 0")
    except (ValueError, KeyError, TypeError):
        return None
    return product


def parse_xml_to_json(input_dir, output_dir):
    """Парсить XML-файли з вхідної директорії та зберігає JSON у вихідну директорію."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".xml"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename.replace(".xml", ".json"))

            try:
                tree = ET.parse(input_path)
                root = tree.getroot()

                product = {child.tag: child.text for child in root}
                product = validate_product_data(product)

                if product:
                    with open(output_path, "w") as json_file:
                        json.dump(product, json_file, indent=4, ensure_ascii=False)
                    print(f"File {filename} was converted to {output_path} successfully.")
                else:
                    print(f"Invalid data in {filename}, skipping.......")
            except ET.ParseError:
                print(f"Error parsing {filename}, skipping.......")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert XML files to JSON")
    parser.add_argument("--input-dir", required=True, help="Directory with XML files")
    parser.add_argument("--output-dir", required=True, help="Directory for JSON files")

    args = parser.parse_args()
    parse_xml_to_json(args.input_dir, args.output_dir)
