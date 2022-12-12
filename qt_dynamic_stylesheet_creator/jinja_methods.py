from typing import Optional, Union

from PySide6 import QtGui


# Template functions declaration [DO NOT MODIFY BEHAVIOUR, IMPLEMENT USER FUNCTIONS SEPRATELY] -------------------------
# pylint: disable=C0103
def opacity(
        color: str, value: Optional[float] = 0.5, as_str: Optional[bool] = True
) -> Union[QtGui.QColor, str]:
    """
    Colour opacity filter

    Args:
        color (str): color
        value (Optional[float]): opacity value (0 to 1)
        as_str (Optional[bool]): set true to return value as str

    Returns:
        str: rgba string
        QtGui.QColor: Colour object
    """
    r, g, b = color[1:][0:2], color[1:][2:4], color[1:][4:]
    color = QtGui.QColor.fromRgbF(int(r, 16), int(g, 16), int(b, 16), value)

    if as_str:
        return f"rgba({color.red()}, {color.green()}, {color.blue()}, {round(color.alphaF(), 3)})"
    return color


# pylint: disable=C0103
def luminosity(
        color: str, brightness: Optional[float] = 0, as_str: Optional[bool] = True
) -> Union[QtGui.QColor, str]:
    """
    Colour luminosity filter

    Args:
        color (str): color
        brightness (Optional[float]): luminosity value (-1 to 1)
        as_str (Optional[bool]): set true to return value as str

    Returns:
        str: rgba string
        QtGui.QColor: Colour object
    """

    r, g, b = color[1:][0:2], color[1:][2:4], color[1:][4:]
    r, g, b = int(r, 16), int(g, 16), int(b, 16)
    # pylint: disable=C3001
    lumn = lambda x: int(min(255, (x + (255 * brightness))))
    color = QtGui.QColor.fromRgb(lumn(r), lumn(g), lumn(b))

    if as_str:
        return f"rgba({color.red()}, {color.green()}, {color.blue()}, {float(1)})"
    return color


# User Method Declaration ----------------------------------------------------------------------------------------------


methods = dict(
    FILTER_OPACITY=opacity,
    FILTER_LUMINOSITY=luminosity,
)
