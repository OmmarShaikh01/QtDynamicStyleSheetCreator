import json
import os
import re
import shutil
import sys
from pathlib import PurePath

import jinja2

try:
    from qt_dynamic_stylesheet_creator.jinja_methods import methods
except ModuleNotFoundError:
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from qt_dynamic_stylesheet_creator.jinja_methods import methods


# Global Declarations
ASSETS = PurePath(os.path.dirname(__file__), "assets")
STYLESHEETS = ASSETS / "stylesheets"
FONTS = ASSETS / "fonts"
ICONS = ASSETS / "icons"
GENERATED = ASSETS / "generated"
BUILD = PurePath(os.path.dirname(ASSETS), "build")


class ResourceGenerator:
    """
    Resource Generator that compiles and build the application stylesheets and icons
    """

    # noinspection PyMissingConstructor,PyDictCreation,SpellCheckingInspection
    def __init__(self, name: str, theme: dict):
        """
        Constructor

        Args:
            name (str): name the theme to load and generate
            theme (dict): Theme dict with UI colours
        """
        self.theme_name = name
        self.app_theme = {}
        self.app_theme["QTCOLOR_PRIMARYCOLOR"] = theme["QTCOLOR_PRIMARYCOLOR"]
        self.app_theme["QTCOLOR_PRIMARYLIGHTCOLOR"] = theme["QTCOLOR_PRIMARYLIGHTCOLOR"]
        self.app_theme["QTCOLOR_PRIMARYDARKCOLOR"] = theme["QTCOLOR_PRIMARYDARKCOLOR"]
        self.app_theme["QTCOLOR_SECONDARYCOLOR"] = theme["QTCOLOR_SECONDARYCOLOR"]
        self.app_theme["QTCOLOR_SECONDARYLIGHTCOLOR"] = theme["QTCOLOR_SECONDARYLIGHTCOLOR"]
        self.app_theme["QTCOLOR_SECONDARYDARKCOLOR"] = theme["QTCOLOR_SECONDARYDARKCOLOR"]
        self.app_theme["QTCOLOR_PRIMARYTEXTCOLOR"] = theme["QTCOLOR_PRIMARYTEXTCOLOR"]
        self.app_theme["QTCOLOR_SECONDARYTEXTCOLOR"] = theme["QTCOLOR_SECONDARYTEXTCOLOR"]
        self.app_theme["QTCOLOR_DANGER"] = "#DC3545"
        self.app_theme["QTCOLOR_WARNING"] = "#FFC107"
        self.app_theme["QTCOLOR_SUCCESS"] = "#17A2B8"
        self.app_theme["FONT_FAMILY"] = "Roboto"

        # adds the jinja methods
        self.app_theme.update(methods)

    # pylint: disable=W0123,C3001,W0612
    def generate_theme_icons(self):
        """
        Uses the themes colours to generate the icon pack
        """

        def replace_file_content(_file_content: str, _file: str, _type: str, _color: str):
            """
            Replaces placeholder color of the SVG file with given color

            Args:
                _file_content (str): file contents
                _file (str): file name
                _type (str): style type
                _color (str): replacement color
            """
            with open((GENERATED / "icons" / _type / _file), "w", encoding="utf-8") as file_output:
                _file_content = _file_content.replace("#0000FF".upper(), _color)
                _file_content = _file_content.replace("#0000FF".lower(), _color)
                replace = "#ffffff00"
                placeholder = "#000000"
                _file_content = _file_content.replace(placeholder, replace)

                file_output.write(_file_content)

        luminosity = methods["FILTER_LUMINOSITY"]
        primary = str(
            luminosity(self.app_theme["QTCOLOR_PRIMARYTEXTCOLOR"], 0.4, as_str=False).name()
        )
        secondary = str(
            luminosity(self.app_theme["QTCOLOR_SECONDARYCOLOR"], 0.1, as_str=False).name()
        )
        disabled = str(luminosity(self.app_theme["QTCOLOR_PRIMARYCOLOR"], 0.5, as_str=False).name())
        success = str(luminosity(self.app_theme["QTCOLOR_SUCCESS"], 0.1, as_str=False).name())
        warning = str(luminosity(self.app_theme["QTCOLOR_WARNING"], as_str=False).name())
        danger = str(luminosity(self.app_theme["QTCOLOR_DANGER"], as_str=False).name())

        self._validate_output_dir()
        for _dir, _sdir, _files in os.walk(ICONS):
            for file in filter(lambda ext: str(os.path.splitext(ext)[1]).lower() == ".svg", _files):
                with open(PurePath(_dir, file), encoding="utf-8") as svg_file:
                    content = svg_file.read()
                    replace_file_content(content, file, "primary", primary)
                    replace_file_content(content, file, "secondary", secondary)
                    replace_file_content(content, file, "disabled", disabled)
                    replace_file_content(content, file, "success", success)
                    replace_file_content(content, file, "warning", warning)
                    replace_file_content(content, file, "danger", danger)

    def generate_theme_stylesheet(self) -> str:
        """
        Generates and saves the compiles stylesheets into a file

        Returns:
            str: compiled stylesheets
        """
        self._validate_output_dir()

        loader = jinja2.FileSystemLoader(STYLESHEETS.as_posix())
        env = jinja2.Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)

        template = env.get_template("main.css.jinja")
        rendered = template.render(self.app_theme)

        # Removes all Comments
        rendered, _ = re.subn(r"/\*.*\*/", "", rendered)
        # Flattens the Document
        rendered = (
            rendered.replace(";\n", "; ")
            .replace(",\n", ", ")
            .replace("{\n", "{ ")
            .replace("    ", "")
        )
        # Combines the Document
        rendered = "\n".join(filter(lambda x: x != "", rendered.splitlines()))

        with open(GENERATED / "stylesheets.css", "w", encoding="utf-8") as css:
            css.write(rendered)

        return rendered

    def build_theme(self):
        """
        Builds the theme pack for the application
        """
        self.generate_theme_icons()
        self.generate_theme_stylesheet()

    def package_theme(self):
        """
        Packages the generated theme pack into a theme zip
        """
        path = BUILD
        if not os.path.exists(path):
            os.mkdir(path)
        shutil.make_archive((path / self.theme_name).as_posix(), "zip", GENERATED)
        shutil.rmtree(GENERATED)

    @staticmethod
    def _validate_output_dir():
        """
        Validates the output directory for the theme pack
        """
        paths = (
            GENERATED,
            GENERATED / "icons",
            GENERATED / "icons" / "primary",
            GENERATED / "icons" / "secondary",
            GENERATED / "icons" / "disabled",
            GENERATED / "icons" / "success",
            GENERATED / "icons" / "warning",
            GENERATED / "icons" / "danger",
        )
        for path in paths:
            if not os.path.exists(path):
                os.mkdir(path)

        path = GENERATED / "stylesheets.css"
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as file:
                file.close()

        path = GENERATED / "apptheme.json"
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as file:
                file.close()


def validate_theme(path: PurePath) -> bool:
    keys = [
        "QTCOLOR_PRIMARYCOLOR",
        "QTCOLOR_PRIMARYLIGHTCOLOR",
        "QTCOLOR_PRIMARYDARKCOLOR",
        "QTCOLOR_SECONDARYCOLOR",
        "QTCOLOR_SECONDARYLIGHTCOLOR",
        "QTCOLOR_SECONDARYDARKCOLOR",
        "QTCOLOR_PRIMARYTEXTCOLOR",
        "QTCOLOR_SECONDARYTEXTCOLOR",
    ]
    print(f"Loading {path} theme")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as file:
            theme = json.load(file)
            return all(map(lambda x: x in keys, theme.keys()))
    else:
        print(f"Loading {path} theme failed")
        raise FileNotFoundError("Failed to load theme file")


def compile_theme(name: str, path: PurePath):
    if os.path.exists(BUILD):
        shutil.rmtree(BUILD)

    if os.path.exists(GENERATED):
        shutil.rmtree(GENERATED)

    with open(path, encoding="utf-8") as file:
        theme = json.load(file)
        res = ResourceGenerator(name, theme)
        res.build_theme()
        res.package_theme()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.description = (
        "For the compiler to work an assets directory with fonts, icons, stylesheets needs to be\n"
        "created that will be compiled into a theme zip that can be used with Qt Apps.\n"
        "> Icons need to be in svg format with the placeholder colour being #0000FF.\n"
        "> Provided theme Colours are \n"
        "    QTCOLOR_PRIMARYCOLOR\n"
        "    QTCOLOR_PRIMARYLIGHTCOLOR\n"
        "    QTCOLOR_PRIMARYDARKCOLOR\n"
        "    QTCOLOR_SECONDARYCOLOR\n"
        "    QTCOLOR_SECONDARYLIGHTCOLOR\n"
        "    QTCOLOR_SECONDARYDARKCOLOR\n"
        "    QTCOLOR_PRIMARYTEXTCOLOR\n"
        "    QTCOLOR_SECONDARYTEXTCOLOR\n"
        "> Custom methods to use inside Jinja tempaltes can be defined in jinja_methods\n"
    )
    parser.add_argument("name", help="name to use when generating theme", type=str)
    parser.add_argument("theme_json", help="path of theme.json to use", type=PurePath)
    args = parser.parse_args()
    if validate_theme(args.theme_json):
        compile_theme(args.name, args.theme_json)
        print(f"Successfully Compiled >> {args.name}")
    else:
        print(f"Failed to Compile >> {args.name}")
    print()
