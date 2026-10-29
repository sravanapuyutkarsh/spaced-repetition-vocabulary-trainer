# vocabulary_trainer_client.DefaultApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**add_word_words_post**](DefaultApi.md#add_word_words_post) | **POST** /words/ | Add Word
[**delete_word_words_word_id_delete**](DefaultApi.md#delete_word_words_word_id_delete) | **DELETE** /words/{word_id} | Delete Word
[**get_due_words_words_due_get**](DefaultApi.md#get_due_words_words_due_get) | **GET** /words/due/ | Get Due Words
[**get_learning_history_words_history_get**](DefaultApi.md#get_learning_history_words_history_get) | **GET** /words/history/ | Get Learning History
[**get_learning_insights_words_insights_get**](DefaultApi.md#get_learning_insights_words_insights_get) | **GET** /words/insights/ | Get Learning Insights
[**health_check_health_get**](DefaultApi.md#health_check_health_get) | **GET** /health | Health Check
[**home_get**](DefaultApi.md#home_get) | **GET** / | Home
[**submit_review_words_word_id_review_post**](DefaultApi.md#submit_review_words_word_id_review_post) | **POST** /words/{word_id}/review/ | Submit Review


# **add_word_words_post**
> WordResponse add_word_words_post(word_create)

Add Word

### Example


```python
import vocabulary_trainer_client
from vocabulary_trainer_client.models.word_create import WordCreate
from vocabulary_trainer_client.models.word_response import WordResponse
from vocabulary_trainer_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = vocabulary_trainer_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with vocabulary_trainer_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = vocabulary_trainer_client.DefaultApi(api_client)
    word_create = vocabulary_trainer_client.WordCreate() # WordCreate | 

    try:
        # Add Word
        api_response = api_instance.add_word_words_post(word_create)
        print("The response of DefaultApi->add_word_words_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->add_word_words_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **word_create** | [**WordCreate**](WordCreate.md)|  | 

### Return type

[**WordResponse**](WordResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_word_words_word_id_delete**
> object delete_word_words_word_id_delete(word_id)

Delete Word

### Example


```python
import vocabulary_trainer_client
from vocabulary_trainer_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = vocabulary_trainer_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with vocabulary_trainer_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = vocabulary_trainer_client.DefaultApi(api_client)
    word_id = 56 # int | 

    try:
        # Delete Word
        api_response = api_instance.delete_word_words_word_id_delete(word_id)
        print("The response of DefaultApi->delete_word_words_word_id_delete:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->delete_word_words_word_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **word_id** | **int**|  | 

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_due_words_words_due_get**
> List[DueWordResponse] get_due_words_words_due_get()

Get Due Words

### Example


```python
import vocabulary_trainer_client
from vocabulary_trainer_client.models.due_word_response import DueWordResponse
from vocabulary_trainer_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = vocabulary_trainer_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with vocabulary_trainer_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = vocabulary_trainer_client.DefaultApi(api_client)

    try:
        # Get Due Words
        api_response = api_instance.get_due_words_words_due_get()
        print("The response of DefaultApi->get_due_words_words_due_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_due_words_words_due_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[DueWordResponse]**](DueWordResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_learning_history_words_history_get**
> object get_learning_history_words_history_get()

Get Learning History

### Example


```python
import vocabulary_trainer_client
from vocabulary_trainer_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = vocabulary_trainer_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with vocabulary_trainer_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = vocabulary_trainer_client.DefaultApi(api_client)

    try:
        # Get Learning History
        api_response = api_instance.get_learning_history_words_history_get()
        print("The response of DefaultApi->get_learning_history_words_history_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_learning_history_words_history_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_learning_insights_words_insights_get**
> object get_learning_insights_words_insights_get()

Get Learning Insights

### Example


```python
import vocabulary_trainer_client
from vocabulary_trainer_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = vocabulary_trainer_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with vocabulary_trainer_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = vocabulary_trainer_client.DefaultApi(api_client)

    try:
        # Get Learning Insights
        api_response = api_instance.get_learning_insights_words_insights_get()
        print("The response of DefaultApi->get_learning_insights_words_insights_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->get_learning_insights_words_insights_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **health_check_health_get**
> object health_check_health_get()

Health Check

### Example


```python
import vocabulary_trainer_client
from vocabulary_trainer_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = vocabulary_trainer_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with vocabulary_trainer_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = vocabulary_trainer_client.DefaultApi(api_client)

    try:
        # Health Check
        api_response = api_instance.health_check_health_get()
        print("The response of DefaultApi->health_check_health_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->health_check_health_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **home_get**
> object home_get()

Home

### Example


```python
import vocabulary_trainer_client
from vocabulary_trainer_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = vocabulary_trainer_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with vocabulary_trainer_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = vocabulary_trainer_client.DefaultApi(api_client)

    try:
        # Home
        api_response = api_instance.home_get()
        print("The response of DefaultApi->home_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->home_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

**object**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **submit_review_words_word_id_review_post**
> ReviewResponse submit_review_words_word_id_review_post(word_id, review_create)

Submit Review

### Example


```python
import vocabulary_trainer_client
from vocabulary_trainer_client.models.review_create import ReviewCreate
from vocabulary_trainer_client.models.review_response import ReviewResponse
from vocabulary_trainer_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = vocabulary_trainer_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with vocabulary_trainer_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = vocabulary_trainer_client.DefaultApi(api_client)
    word_id = 56 # int | 
    review_create = vocabulary_trainer_client.ReviewCreate() # ReviewCreate | 

    try:
        # Submit Review
        api_response = api_instance.submit_review_words_word_id_review_post(word_id, review_create)
        print("The response of DefaultApi->submit_review_words_word_id_review_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling DefaultApi->submit_review_words_word_id_review_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **word_id** | **int**|  | 
 **review_create** | [**ReviewCreate**](ReviewCreate.md)|  | 

### Return type

[**ReviewResponse**](ReviewResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

