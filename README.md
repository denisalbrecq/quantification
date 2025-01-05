# Quantification

This Python script processes grayscale images to perform uniform and adaptive quantization while visualizing the results. It also includes functionality to calculate and display quantization errors, allowing for a deeper understanding of image compression techniques.

# Features
Uniform Quantization: Converts an image into specified grayscale levels (e.g., 8, 4, 2).
Adaptive Quantization: Dynamically adjusts grayscale levels based on local variance for better detail preservation.
Pixel Group Analysis: Extracts and displays pixel values for a defined region.
Visualization: Displays the original image, quantized versions, and error maps side-by-side.

# How to Use
Prepare the Image:
Place your image in the script's directory.
Update the chemin_image variable with your image name (default: image_003.jpg).

Configure Parameters:
Adjust options like quantization levels (niveaux_de_gris), pixel group coordinates, and adaptive mode.

Run the Script:
Execute the script to visualize and compare the quantized images.

# Output
Original and quantized images (with specified grayscale levels).
Error maps (difference between original and quantized images).
Optionally, adaptively quantized images with average levels calculated dynamically.

# Explore and analyze your images with ease!

created in december 2024 by Denis Albrecq
