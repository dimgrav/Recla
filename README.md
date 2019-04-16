# Recla

*Easy on the eyes!*

2019 &copy; Dimitris Gravanis

### What is Recla?

Recla is a small Python application, that adjusts your screen color temperature at sunrise and sunset, to reduce the strain caused by blue light in dark ambience.

Currently, Recla requires your location coordinates in order to perform a GET request to the [Sunrise-Sunset.org public API](https://api.sunrise-sunset.org/) and receive the sunrise/sunset values per day.

In the future, scheduled times may be used instead.

Recla uses `sct`, created by [Ted Unangst](http://www.tedunangst.com/flak/post/sct-set-color-temperature).

More soon!

### Install dependencies

**Python**

Using Python 3:
```
pip install -r requirements.txt
```

**System**

If you want to compile `sct` yourself, for Ubuntu-based (18.04+) distros you will need:

```
sudo apt install libx11-dev libxrandr-dev
```

### Run

You can currently run Recla manually.

Short/long options list:

| option            | short| long           |
| ----------------- | ---- | -------------- |
| latitude          |  -z  | --lat=         |
| longitude         |  -y  | --lon=         |
| day temperature   |  -d  | --day_temp=    |
| night temperature |  -n  | --night_temp=  |

For example:

```
python3 recla.py -z <latitude> -y <longitude> -d <day temperature> -n <night temperature>

python3 recla.py --lat=<latitude> --lon=<longitude> --day_temp=<day temperature> --night_temp=<night temperature>
``` 

  
