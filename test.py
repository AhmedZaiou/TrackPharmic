
def generate_barcode(barcode_data):  
    barcode_format = barcode.get_barcode_class('EAN13')  # Barcode format (EAN13 in this case)
    barcode_instance = barcode_format(barcode_data, writer=ImageWriter())

    # Save the barcode as an image file
    barcode_image = barcode_instance.render()  # Generate the barcode image
    barcode_image.save("barcode.png")  # Save the barcode as PNG