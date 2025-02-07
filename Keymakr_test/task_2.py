import argparse
import json
import logging
import os
import xml.etree.ElementTree as ET


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def validate_product_data(product: dict) -> dict | None:
    """Validates product data and returns a dictionary if valid, None otherwise."""

    required_fields = ["id", "name", "price"]

    try:
        for field in required_fields:
            if field not in product:
                raise KeyError(f"Missing required field: {field}")

        product = {
            key: value.strip() if isinstance(value, str) else value
            for key, value in product.items()
        }

        for field in required_fields:
            if isinstance(product[field], str) and not product[field]:
                raise ValueError(f"Field {field} cannot be empty")

        product["id"] = int(product["id"])
        product["price"] = float(product["price"])

        if product["id"] <= 0 or product["price"] <= 0:
            raise ValueError("Id and price must be greater than 0")

    except KeyError as ke:
        logging.error(f"Missing field in product data: {ke}. Data: {product}")
        return None
    except ValueError as ve:
        logging.error(f"Validation error in product data: {ve}. Data: {product}")
        return None
    except TypeError as te:
        logging.error(f"Type error in product data: {te}. Data: {product}")
        return None

    logging.info(f"Product data is valid: {product}")
    return product


def parse_xml_to_json(input_dir: str, output_dir: str) -> None:
    """Parses XML files in the input directory and converts them to JSON files in the output directory."""

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        logging.info(f"Output directory '{output_dir}' was created.")

    for filename in os.listdir(input_dir):
        if filename.endswith(".xml"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename.replace(".xml", ".json"))

            try:
                logging.info(f"Processing file: {filename}")

                tree = ET.parse(input_path)
                root = tree.getroot()

                product = {child.tag: child.text for child in root}
                logging.debug(f"Parsed data from XML: {product}")

                product = validate_product_data(product)

                if product:
                    try:
                        with open(output_path, "w", encoding="utf-8") as json_file:
                            json.dump(product, json_file, indent=4, ensure_ascii=False)
                        logging.info(
                            f"File '{filename}' successfully converted to '{output_path}'."
                        )
                    except OSError as ose:
                        logging.error(f"Error writing to {output_path}: {ose}")
                else:
                    logging.warning(f"Invalid data in file '{filename}', skipping.")
            except ET.ParseError as pe:
                logging.error(f"Error parsing file '{filename}': {pe}, skipping.")
            except Exception as e:
                logging.error(
                    f"Unexpected error with file '{filename}': {e}, skipping."
                )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert XML files to JSON")
    parser.add_argument("--input-dir", required=True, help="Directory with XML files")
    parser.add_argument("--output-dir", required=True, help="Directory for JSON files")

    args = parser.parse_args()
    parse_xml_to_json(args.input_dir, args.output_dir)
