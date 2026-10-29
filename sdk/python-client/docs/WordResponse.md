# WordResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**word** | **str** |  | 
**definition** | **str** |  | 
**language** | **str** |  | 
**created_at** | **datetime** |  | 

## Example

```python
from vocabulary_trainer_client.models.word_response import WordResponse

# TODO update the JSON string below
json = "{}"
# create an instance of WordResponse from a JSON string
word_response_instance = WordResponse.from_json(json)
# print the JSON string representation of the object
print(WordResponse.to_json())

# convert the object into a dict
word_response_dict = word_response_instance.to_dict()
# create an instance of WordResponse from a dict
word_response_from_dict = WordResponse.from_dict(word_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


