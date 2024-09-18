import cv2
#this file is for the relative positioning functions
def draw_rectangle(image, x1_pct, y1_pct, x2_pct, y2_pct, color, thickness):
    """
    Draws a rectangle on the image using relative percentages for positioning.

    Args:
        image (numpy.ndarray): The image to draw on.
        x1_pct (float): The x-coordinate of the top-left corner as a percentage of frame width (0.0 to 1.0).
        y1_pct (float): The y-coordinate of the top-left corner as a percentage of frame height (0.0 to 1.0).
        x2_pct (float): The x-coordinate of the bottom-right corner as a percentage of frame width (0.0 to 1.0).
        y2_pct (float): The y-coordinate of the bottom-right corner as a percentage of frame height (0.0 to 1.0).
        color (tuple): The color of the rectangle in BGR format (e.g., (255, 255, 255) for white).
        thickness (int): The thickness of the rectangle border.
    """
    frame_height, frame_width = image.shape[:2]

    start_x = int(frame_width * x1_pct)
    start_y = int(frame_height * y1_pct)
    end_x = int(frame_width * x2_pct)
    end_y = int(frame_height * y2_pct)

    cv2.rectangle(image, (start_x, start_y), (end_x, end_y), color, thickness)


def put_text(image, text, x_pct, y_pct, font_scale, color, thickness):
    """
    Adds text to the image using relative percentages for positioning.

    Args:
        image (numpy.ndarray): The image to draw on.
        text (str): The text to display.
        x_pct (float): The x-coordinate of the text position as a percentage of frame width (0.0 to 1.0).
        y_pct (float): The y-coordinate of the text position as a percentage of frame height (0.0 to 1.0).
        font_scale (float): The scale of the font.
        color (tuple): The color of the text in BGR format (e.g., (0, 0, 0) for black).
        thickness (int): The thickness of the text.
    """
    frame_height, frame_width = image.shape[:2]

    text_x = int(frame_width * x_pct)
    text_y = int(frame_height * y_pct)

    cv2.putText(image, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness, cv2.LINE_AA)

