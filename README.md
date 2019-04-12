# Recla

Easy on the eyes

2019 (C) Dimitris Gravanis

### What is Recla?

Recla is a small Python application, that adjusts your screen color temperature.

More soon!

### Install

Using **Python 3**
```
pip install -r requirements.txt
```

### Run

Provide x-ecute privileges to start.sh:

```
chmod +x start.sh
```

Run with short/long options

| option            | short| long          |
| ----------------  | ---- | --------------|
| latitude          |  -z  | --lat=        |
| longitude         |  -y  | --lon=        |
| day temperature   |  -d  | -day_temp=    |
| night temperature |  -n  | -night_temp=  |

For example:

```
/path/to/start.sh -z <latitude> -y <longitude> -d <day temperature> -n <night temperature>

/path/to/start.sh --lat=<latitude> --lon=<longitude> --day_temp=<day temperature> --night_temp=<night temperature>
``` 

  