# IoT_SkyImager-using-RaspberryPi

A low cost sky imager developed to focus on providing real time cloud images and cloud cover index data based on the colour of the clouds.

However due to my negligence, I dont have the raspberry pi with me sooo, I dont have the file to capture the sky images using the raspberry Pi :((( The file above is only the data processing part for the sky images.

Afraid not! The raspberry pi coding is easy, you just capture image -> transfer the image via Socket (you need to know your IP), and then the image is processed using the file above.

I created this project to predict the weather condition. To do this, the cloud colours are divided into 4 colour ranges.
1. White clouds typically indicate fair weather.
2. Gray clouds are usually associated with cloudy conditions and can indicate the presence of moisture in the air.
3. Dark clouds typically indicate the presence of rain.
4. Darker clouds (very dark), such as those that are black or deep gray, can indicate the presence of severe weather such as thunderstorms, which can bring heavy rain, high winds, and lightning.

To count the cloud pixels, Python's Imaging Library (PIL) is used.
The data of the clouds categorized in each colour ranges are then stored in an SQL database.
