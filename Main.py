import tensorflow as tf
import os
import numpy as np
import cv2  # For image processing

# Global variables
model = None
output_class = ["Batteries", "Clothes", "E-waste", "Glass", "Light Blubs", "Metal", "Organic", "Paper", "Plastic"]

data = {
    "Batteries": [
        "Used Batteries",
        "Batteries should be properly disposed of at designated recycling centers.",
        "Avoid throwing in regular trash to prevent leaks of toxic chemicals."
    ],
    "Clothes": [
        "Used Clothes",
        "Consider donating clean, wearable clothes to charity or recycling centers.",
        "Explore recycling options for fabrics like cotton, polyester, and wool."
    ],
    "E-waste": [
        "Electronic Waste",
        "E-waste includes items like old phones, computers, and other electronic devices.",
        "Recycle at e-waste collection points to prevent environmental contamination."
    ],
    "Glass": [
        "Glass Items",
        "Glass can be endlessly recycled without losing quality.",
        "Separate by color (clear, green, brown) if required by local guidelines."
    ],
    "Light Blubs": [
        "Used Light Bulbs",
        "CFLs and LEDs can be recycled but require special handling.",
        "Dispose of broken bulbs carefully to avoid injury and contamination."
    ],
    "Metal": [
        "Metal Waste",
        "Scrap metal like aluminum, steel, and copper can be recycled.",
        "Recycling metals reduces mining and conserves natural resources."
    ],
    "Organic": [
        "Organic Waste",
        "Includes food scraps, yard waste, and other biodegradable materials.",
        "Ideal for composting to create nutrient-rich soil."
    ],
    "Paper": [
        "Paper Products",
        "Paper and cardboard are highly recyclable materials.",
        "Ensure the paper is clean and dry before recycling."
    ],
    "Plastic": [
        "Plastic Items",
        "Recycle plastics marked with recycling symbols (e.g., PET, HDPE).",
        "Reduce usage of single-use plastics to minimize environmental impact."
    ]
}

def load_artifacts():
    """
    Load the trained model from the specified path.
    """
    global model
    try:
        model_path = os.path.join(os.path.dirname(__file__), 'Model', 'classifyWaste.keras')
        model = tf.keras.models.load_model(model_path)
        print("Model loaded successfully!")
    except Exception as e:
        print(f"Error loading model: {e}")

def calculate_waste_amount(image_path):
    """
    Analyze the image to estimate the amount of waste.
    Returns a string: 'Low', 'Medium', or 'Large'.
    """
    try:
        # Load image
        image = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if image is None:
            raise ValueError("Image could not be loaded.")

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray_image, 128, 255, cv2.THRESH_BINARY_INV)

        total_pixels = image.shape[0] * image.shape[1]
        waste_pixels = cv2.countNonZero(thresh)
        waste_ratio = waste_pixels / total_pixels

        if waste_ratio < 0.2:
            return "Low"
        elif waste_ratio < 0.5:
            return "Medium"
        else:
            return "Large"

    except Exception as e:
        print(f"Error calculating waste amount: {e}")
        return "Unknown"

def classify_waste(image_path):

    try:
        # Load and preprocess the image
        test_image = tf.keras.preprocessing.image.load_img(image_path, target_size=(224, 224))
        test_image = tf.keras.preprocessing.image.img_to_array(test_image) / 255
        test_image = np.expand_dims(test_image, axis=0)

        predicted_array = model.predict(test_image)
        predicted_value = output_class[np.argmax(predicted_array)]

        print(f"Predicted Value: {predicted_value}")
        print(f"Data for {predicted_value}: {data.get(predicted_value)}")

        # Retrieve additional information for the predicted category
        if predicted_value not in data:
            raise ValueError(f"Predicted value '{predicted_value}' not found in the 'data' dictionary.")
        
        predicted_data = data[predicted_value]
        if len(predicted_data) < 3:
            raise IndexError(f"Expected at least 3 elements in data[{predicted_value}], but found {len(predicted_data)}.")

        # Determine the waste amount
        waste_amount = calculate_waste_amount(image_path)

        return predicted_value, predicted_data[0], predicted_data[1], predicted_data[2], waste_amount

    except Exception as e:
        print(f"Error during classification: {e}")
        return None, None, None, None, "Unknown"
