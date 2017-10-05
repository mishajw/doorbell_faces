# API specification draft

## POST `face-server/capture`
Add a capture to the database and recognise faces

Request body parameters:
1) `images`: Sequence of captured images
2) `start_time`: Start time of the captured images in unix time

Returns:
1) A list of recognitions in the capture. Each recognition contains:
    1) `person` object containing:
        1) `id`: The ID of the person
        2) `name`: The name of the person
    2) `location_x`: The X pixel in the image of the recognised face
    3) `location_y`: The Y pixel in the image of the recognised face
    4) `location_width`: The width in pixels of the recognised face in the image
    5) `location_height`: The height in pixels of the recognised face in the image

## GET `face-server/recognitions/list`
List all recognised faces by time

Request body parameters:
1) `start_time`: Optional. The earliest time to fetch
2) `end_time`: Optional. The latest time to fetch

Returns:
1) `recognitions`: The list of recognitions that happened between `start_time` and `end_time`, sorted by `time`.
Contains:
    1) `person`: Object for recognised person, containing:
        1) `id`: The ID of the person
        2) `name`: The name of the person
    2) `capture`: Object for the capture used for recognitions, containing:
        1) `id`: The ID of the capture
        2) `time`: The time of the capture
        3) `hash`: The hash of the capture's image or video


Returns a list of Recognitions sorted by `recognition.capture.time`

## GET `face-server/capture/<id or hash>/image`
Get the image of a capture
URL parameters:
1) `id or hash`: Either the ID of the capture or the hash of the image

Returns:
1) A download stream of the image of a capture
