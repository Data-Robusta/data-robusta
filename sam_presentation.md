Briefly explain our data and its sources. 

At first we tried several models using price, temperature, precipitation, production quantities to predict price. We found that Colombian weather was a very poor predictor of their coffee price. We experimented with various transformations of weather data, including date-shifting and weighting them by regional production quantities. While neither of those ideas panned out directly, the latter did inform some improvements in our model. Since we only had a regional breakdown of coffee production back to 2002, that model appeared to greatly improve our predictions, but we quickly found this was due to limiting the time period, not the new aggregated weather variables.

Our best-performing model solely utilized production quantities and past prices from 1995 onward, but it still did not predict prices especially well. The model calculates prices that miss the actual price by 36.7 cents (or about 20%) per pound on average. We found that unpredictable events like plant disease, natural disasters, and major trade agreements drive extreme changes in the price of Colombian coffee.

What we'd like to include in our model.