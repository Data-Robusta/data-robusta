The coffee data came from the National Federation of Coffee Growers in Colombia, commonly known as Fedecafé. These spreadsheets included records of all coffee export prices in dollars per pound, going back to 1960. They also listed the monthly quantity of coffee produced in thousands of sixty kilogram bags. We acquired our weather data from the National Oceanic and Atmospheric Administration. We selected all precipitation and temperature data from 1960 to 2018. We filled in missing weather data using a forecasting tool from Facebook.

At first we tried several models using price, temperature, precipitation, production quantities to predict price. We found that Colombian weather was a very poor predictor of their coffee price. We experimented with various transformations of weather data, including date-shifting and weighting them by regional production quantities. While neither of those ideas panned out directly, the latter did inform some improvements in our model. Since we only had a regional breakdown of coffee production back to 2002, that model appeared to greatly improve our predictions, but we quickly found this was due to limiting the time period, not the new aggregate weather variables.

Our best-performing model solely utilized production quantities and past prices from 1995 onward, but it still did not predict prices especially well. The model calculates prices that miss the actual price by 37 cents (or about 20%) per pound on average. We found that unpredictable events like plant disease, natural disasters, and major trade agreements drive extreme changes in the price of Colombian coffee. When excluding these severe events, our model performed better, only missing the actual price by 26 cents per pound (or 15%).

Going forward, we think it may yield a more accurate model to also include factors that would help predict demand and the cost of purchasing and transporting the coffee to destination. Including information such as US weather, crude oil prices, and the exchange rate between the US dollar and the Colombian Peso might account for these missing pieces and result in a more accurate model.

The best model had an RMSE of 36.68. This means on average it missed its guess by 20.28% of the price.
During stable months, its RMSE was 25.92, and missed by 15.25% of the price.

The weather model had an RMSE of 60.81. This means on average it missed its guess by 33.68% of the price.
During stable months, its RMSE was 20.51, and missed by 11.95% of the price.

Hi I'm Sam. My work focused on acquiring the data, filling in missing data, and modeling price.

The Data Robusta team set out to see if we could develop a model for predicting Colombian wholesale coffee prices. Our initial hypothesis was that temperature and more volatile precipitation would be strong drivers of coffee price. So does weather predict price? Like any good data scientist will tell you...it depends.

slide: Just price over time

At first we tried several models using price, temperature, precipitation, and production quantities to predict price. We found that Colombian weather was a very poor predictor of their coffee price. We experimented with various transformations of weather data, including date-shifting and weighting them by regional production quantities. While neither of those ideas panned out directly (fix wording), the latter did inform some improvements in our model. Since we only had a regional breakdown of coffee production back to 2002, that model appeared to greatly improve our predictions, but we quickly realized this was due to limiting the time period, not the new aggregate weather variables.

slide: improved model (old best model)

Our improved model used just coffee production quantity and prices from 1995 onward, but it still did not predict prices especially well. The mean price of coffee during this time was $1.80 per pound and the model calculated prices that miss the actual price by 37 cents (about 20%). We found that unpredictable events like plant disease, natural disasters, and major trade agreements drive extreme changes in the price of Colombian coffee. 

slide: best model

This led us to a pivotal point in our analysis. When splitting our model, one for "normal prices" plus or minus 20% of the average price and one to capture severe events, our model was able to reduce the calculated error down to 32 cents.

Going forward, we think it may yield a more accurate model to also include factors that would help predict demand and the cost of purchasing and transporting the coffee to destination. Including information such as US weather, crude oil prices, and the exchange rate between the US dollar and the Colombian Peso might account for these missing pieces and result in an even better model.