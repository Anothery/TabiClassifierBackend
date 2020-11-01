# TabiClassifierBackend

Image classifier that also determines dominant picture colors

Technology stack: Flask for API, Tensorflow for classifying

Main and the only one endpoint is /classify. 

Just send a POST request with multipart image as value (key is "file")

### Example

**Request:**
```
POST /classify HTTP/1.1
Host: localhost
Content-Type: multipart/form-data;
Content-Disposition: form-data; name="file"; filename="CvTLFqD2-lw.jpg"
```

**Image:**

<img src="https://i.imgur.com/3i8CmBq.jpg" width="400">

**Response:**

```
{
    "colors": {
        "beige": {
            "meanHexColor": "#eef1de",
            "percentage": 0.05
        },
        "black": {
            "meanHexColor": "#090c1b",
            "percentage": 0.2
        },
        "blue": {
            "meanHexColor": "#3e6376",
            "percentage": 0.27
        },
        "cyan": {
            "meanHexColor": "#ddf7f1",
            "percentage": 0.01
        },
        "gray": {
            "meanHexColor": "#94a4a1",
            "percentage": 0.25
        },
        "green": {
            "meanHexColor": "#66a19e",
            "percentage": 0.07
        },
        "violet": {
            "meanHexColor": "#285a85",
            "percentage": 0.01
        },
        "white": {
            "meanHexColor": "#f7faef",
            "percentage": 0.15
        }
    },
    "predictions": {
        "art": 1.0,
        "frame": 0.0,
        "manga": 0.0
    }
}
```
