# Qt Dynamic Stylesheet Creator

> Dynamic Qt Stylesheet generator using Jinja templates
<hr>

## Usage
```sh 
python.exe -m qt_dynamic_stylesheet_creator name path_to theme.json 
```

## theme.json 
```json
{
    "QTCOLOR_PRIMARYCOLOR": "#212121",
    "QTCOLOR_PRIMARYLIGHTCOLOR": "#484848",
    "QTCOLOR_PRIMARYDARKCOLOR": "#000000",
    "QTCOLOR_SECONDARYCOLOR": "#f9a825",
    "QTCOLOR_SECONDARYLIGHTCOLOR": "#ffd95a",
    "QTCOLOR_SECONDARYDARKCOLOR": "#c17900",
    "QTCOLOR_PRIMARYTEXTCOLOR": "#ffffff",
    "QTCOLOR_SECONDARYTEXTCOLOR": "#ffffff"
}
```

## Interface
```
python.exe -m qt_dynamic_stylesheet_creator
usage: __main__.py [-h] name theme_json

For the compiler to work an assets directory with fonts, icons, stylesheets needs to be
created that will be compiled into a theme zip that can be used with Qt Apps.
> Icons need to be in svg format with the placeholder colour being #0000FF.
> Provided theme Colours are
    QTCOLOR_PRIMARYCOLOR
    QTCOLOR_PRIMARYLIGHTCOLOR
    QTCOLOR_PRIMARYDARKCOLOR
    QTCOLOR_SECONDARYCOLOR
    QTCOLOR_SECONDARYLIGHTCOLOR
    QTCOLOR_SECONDARYDARKCOLOR
    QTCOLOR_PRIMARYTEXTCOLOR
    QTCOLOR_SECONDARYTEXTCOLOR
> Custom methods to use inside Jinja tempaltes can be defined in jinja_methods

positional arguments:
  name        name to use when generating theme
  theme_json  path of theme.json to use

options:
  -h, --help  show this help message and exit
```