from xhtml2pdf import pisa
import barcode
from barcode.writer import ImageWriter

from io import BytesIO
import base64


def generate_barcode(barcode_data):
    options = {
        "module_width": 200 / 1000,  # Adjust module width (barcode thickness)
        "module_height": 2.5,  # Barcode height
        "font_size": 3,  # Font size for the label (you can adjust this)
        "text_distance": 2,  # Distance between the barcode and text
        "quiet_zone": 1,  # Quiet zone (padding) around the barcode
    }
    barcode_format = barcode.get_barcode_class(
        "EAN13"
    ) 
    barcode_format = barcode.get_barcode_class(
        "code128"
    )  # Barcode format (EAN13 in this case)
    barcode_instance = barcode_format(barcode_data, writer=ImageWriter())

    # Save the barcode as an image file
    barcode_image = barcode_instance.render(options)  # Generate the barcode image
    # Save the barcode to a BytesIO object

    # Resize the image
    buffered = BytesIO()
    barcode_image.save(buffered, format="PNG")
    # Convert the image to base64
    barcode_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    barcode_image.save(f"bare_code/barcode_{barcode_data}.png", format="PNG")

    return barcode_base64


barcode_data_list = [
    "ART6536",
    "VC",
    "20094827",
]
for item in barcode_data_list:
    generate_barcode(item)
