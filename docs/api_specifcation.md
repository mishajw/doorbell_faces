## API specification draft

### Objects

#### Person

A distinct person that has been recognised

Fields:
1) `person_id`: The ID of this person
2) `name`: Optional. The name tied to this person
3) `capture_ids`: List of recognitions this person has been spotted in

#### Captures

A series of images that have been added for recognition

Fields:
1) `capture_id`: The ID of this capture
2) `time`: The unix time that this recognition happened
3) `recognitions`: A list of Recognitions

#### Recognitions

A recognition of a person in a capture

Fields:
1) `recognition_id`: The ID of this recognition
2) `person_id`: The person recognised
3) `capture_id`: The capture this was recognised in
4) `location`: The location in the image that this recognition happened

### API methods

#### `doorbell_faces.add_capture()`
Add a capture to the database and recognise faces

Parameters:
1) `images`: Sequence of captured images
2) `start_time`: Start time of the captured images in unix time

Returns a Capture

#### `doorbell_faces.list_recognitions()`
List all recognised faces by time

Parameters:
1) `start_time`: Optional. The earliest time to fetch
1) `end_time`: Optional. The latest time to fetch

Returns a list of Recognitions sorted by `recognition.capture.time`
