# Score Function
### Why a score function is needed
1. When a detector operator takes in an image, a group of images are detected. But the number of the images is uncertain. So when an image is processed by a pipeline containing detector operators, an uncertain number of feature vectors are returned. In order to filter the set of results that best meets the needs from the nearest neighbor search results of these vectors, a specific scoring mechanism is required.

2. Phantoscope 0.2.0 and later versions support multiple pipelines. In order to filter the set of results that best meets the needs from the search results of multiple fields, a specific scoring mechanism is required.

### Score function settings
1. Inner Field Score Mode

    For an uncertain number of sets of search results in a single field of an application, Phantoscope provides the InnerFieldScoreMode to support personalized filtering of final results.

    The following modes are supported:
        
    | Inner field score mode | Explanation                                                                                     | Notes                                                       |
    | ---------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------ |
    | first                  | Selects the first entity from several entities detected from a single field and conducts topk search. | Generally detected entities are sorted by confidence; the first entity has the highest confidence. |
    | avg-select             | Conducts topk search on several entities detected from a single field and evenly selects the first few entities from the result sets as the final results. | Evenly selects in order to guarantee that the result sets include all kinds of entities. |
    | random-select          | Selects an entity from several entities detected from a single field and conducts topk search. | Randomly selects in order to increase search diversity.                   |
    | distance_first         | Conducts topk search on several entities detected from a single field and selects the nearest entities from the result sets as the final results. | Selects the nearest entities to guarantee that the results are the most similar ones to a certain part of the input image.  |
    
    Take the detection of an object as an example. When the search data is a specific image, Phantoscope first uses the processor (specifically the detector processors, such as SSD) to extract a table, a chair, and a lamp from the image. Then the three images of the objects are encoded using the encoder to obtain three feature vectors. Each vector is used as input data, and the most similar topk entities are found in the Milvus base library. 
    
    If the `distance_first` inner field score mode is selected, then all search results are sorted by vector distance and the nearest one is the final result. The result obtained at this time must be the result set most similar to an object in the searched image.
    
    
2. Inter-field Score Mode
    
    For the search results in multiple fields of an application, Phantoscope provides the ScoreMode to support personalized combination of search results of each field, and sorts the final scores to select the highest score as the final result.

    The following modes are supported:
    
    | Score mode | Explanation                            | Notes |
    | ---------- | --------------------------------- | ---- |
    | first      | Selects the score of the first field as the final score. |      |
    | sum        | Sums the scores of all fields as the final score.  |      |
    | max        | Selects the highest score of all fields as the final score. |      |
    | min        | Selects the lowest score of all fields as the final score. |      |
    | multiple   | Multiplies the scores of all fields as the final score. |      |
    | avg        | Averages the scores of all fields as the final score. |      |

3. Score Function
    
    1. weight
    
        Assigns the weight of a specific field to change the effect of the field result on the final result.
    
    2. decay functions: linear
    
        The search results within a specific field are sorted by default, and the corresponding scores of the results decay accordingly. Currently, only linear decay is implemented.