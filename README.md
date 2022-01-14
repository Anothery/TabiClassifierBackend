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
    "colors": [
        {
            "meanHexColor": "#090c1b",
            "name": "black",
            "percentage": 0.2
        },
        {
            "meanHexColor": "#f7faef",
            "name": "white",
            "percentage": 0.15
        },
        {
            "meanHexColor": "#3e6376",
            "name": "blue",
            "percentage": 0.27
        },
        {
            "meanHexColor": "#94a4a1",
            "name": "gray",
            "percentage": 0.25
        },
        {
            "meanHexColor": "#66a19e",
            "name": "green",
            "percentage": 0.07
        },
        {
            "meanHexColor": "#285a85",
            "name": "violet",
            "percentage": 0.01
        },
        {
            "meanHexColor": "#eef1de",
            "name": "beige",
            "percentage": 0.05
        },
        {
            "meanHexColor": "#ddf7f1",
            "name": "cyan",
            "percentage": 0.01
        }
    ],
    "predictions": {
        "art": 1.0,
        "frame": 0.0,
        "manga": 0.0
    }
}
```
