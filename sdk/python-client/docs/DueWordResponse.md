# DueWordResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**word** | **str** |  | 
**definition** | **str** |  | 
**language** | **str** |  | 
**created_at** | **datetime** |  | 
**next_review** | **datetime** |  | 
**interval** | **int** |  | 
**repetition** | **int** |  | 
**easiness_factor** | **float** |  | 

## Example

```python
from vocabulary_trainer_client.models.due_word_response import DueWordResponse

# TODO update the JSON string below
json = "{}"
# create an instance of DueWordResponse from a JSON string
due_word_response_instance = DueWordResponse.from_json(json)
# print the JSON string representation of the object
print(DueWordResponse.to_json())

# convert the object into a dict
due_word_response_dict = due_word_response_instance.to_dict()
# create an instance of DueWordResponse from a dict
due_word_response_from_dict = DueWordResponse.from_dict(due_word_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


