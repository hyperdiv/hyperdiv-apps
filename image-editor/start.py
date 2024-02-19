import os
import io
import hyperdiv as hd
from PIL import Image, ImageEnhance

input_path = os.path.join(os.path.dirname(__file__), "assets", "kitten.jpg")
original = Image.open(input_path)


def adjust_image(saturation_level, brightness_level, contrast_level):
    """
    Takes an image path and saturation, brightness, contrast values on
    a scale from 0 to 100, where a value of 50 denotes the value in
    the original image, and a value other than 50 denotes a
    modification.

    Returns the bytes of a modified copy of the image.
    """

    # Adjust saturation
    enhancer_saturation = ImageEnhance.Color(original)
    adjusted_saturation = enhancer_saturation.enhance(1 + (saturation_level - 50) / 50)

    # Adjust brightness
    enhancer_brightness = ImageEnhance.Brightness(adjusted_saturation)
    adjusted_brightness = enhancer_brightness.enhance(1 + (brightness_level - 50) / 50)

    # Adjust contrast
    enhancer_contrast = ImageEnhance.Contrast(adjusted_brightness)
    adjusted_contrast = enhancer_contrast.enhance(1 + (contrast_level - 50) / 50)

    buffered = io.BytesIO()
    adjusted_contrast.save(buffered, format=original.format)

    return buffered.getvalue()


def main():
    state = hd.state(image_bytes=None)
    if state.image_bytes is None:
        # Prime the 'modified' image with default values:
        state.image_bytes = adjust_image(50, 50, 50)

    template = hd.template(title="Image Editor", sidebar=False)
    with template.body:
        # Render the side by side images
        with hd.hbox():
            with hd.box(width="50%", gap=1):
                hd.text("Original")
                hd.image("/assets/kitten.jpg")
            with hd.box(width="50%", gap=1):
                hd.text("Modified")
                hd.image(state.image_bytes)

        # Render the sliders
        saturation_slider = hd.slider("Saturation", value=50)
        brightness_slider = hd.slider("Brightness", value=50)
        contrast_slider = hd.slider("Contrast", value=50)

        changed = (
            saturation_slider.changed
            or brightness_slider.changed
            or contrast_slider.changed
        )

        if changed:
            # Update the image with the new slider values:
            state.image_bytes = adjust_image(
                saturation_slider.value,
                brightness_slider.value,
                contrast_slider.value,
            )


hd.run(main)
