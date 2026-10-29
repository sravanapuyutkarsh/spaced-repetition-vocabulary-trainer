# ReviewResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**word_id** | **int** |  | 
**word** | **str** |  | 
**score** | **int** |  | 
**interval** | **int** |  | 
**repetition** | **int** |  | 
**easiness_factor** | **float** |  | 
**next_review** | **datetime** |  | 

## Example

```python
from vocabulary_trainer_client.models.review_response import ReviewResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ReviewResponse from a JSON string
review_response_instance = ReviewResponse.from_json(json)
# print the JSON string representation of the object
print(ReviewResponse.to_json())

# convert the object into a dict
review_response_dict = review_response_instance.to_dict()
# create an instance of ReviewResponse from a dict
review_response_from_dict = ReviewResponse.from_dict(review_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


