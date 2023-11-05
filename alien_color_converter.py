from PIL import Image

def convert_alien_color(current_image_path, converted_image_path, 
                        current_color, desired_color, tolerance):
    """Convert the current alien color to the desired alien color."""

    # Load the current alien image.
    current_image = Image.open(current_image_path)

    # Convert the image to RGB if it is not.
    if current_image.mode != 'RGB':
        current_image = current_image.convert('RGB')

    # Access all the pixels of the image.
    pixels = current_image.load()

    # Iterate over each pixel.
    for i in range(current_image.width):
        for j in range(current_image.height):
            # If the pixel is within the tolerance of the current alien color,
            #  replace it.
            if _within_tolerance(pixels[i, j], current_color, tolerance):
                pixels[i, j] = desired_color

    # Save the modified image.
    current_image.save(converted_image_path)


def _within_tolerance(current_pixel, target_color, tolerance):
    """
    Check if the current pixel is sufficiently different from the target color.
    """
    return all(abs(current_pixel[i] - target_color[i]) <= tolerance 
               for i in range(3))
