import random

def predict_function(topic,estimated_time):
    """ We need to """
    print(f" We were asked to predict {topic} value at {estimated_time}")
    predicted_value = random.choice([True, False])
    predicted_confidence = random.randint(1,100)
    return(predicted_value,predicted_confidence)