The Data Robusta team wanted to see if we could develop a model for predicting Colombian wholesale coffee prices in 2018 dollars per pound. We initially hypothesized that temperature and more volatile precipitation are strong drivers of coffee price. So does weather predict price? Like any good data scientist will tell you...it depends.

We first tried models using all of our available features: historical price, temperature, precipitation, and production quantities. We used Prophet, a time-series modeling library developed by Facebook, to create these models. Prophet models create three functions: an overall trend, seasonal trend, and holiday trend. These come together to predict the overall pattern of temporal data.

Slide: Price over time and baseline model

Initially, climate data appeared to worsen our models. Here, you can see how poorly our early weather model, the green line, predicted actual prices, the tan line. Our best early model only used prior prices and production quantities. We experimented with various transformations of weather data, including date-shifting and weighting them by regional production quantities. While these changes did not result in better predictions than the models that excluded weather data, they did provide a key insight for later models. 

Since we only had regional production data from 2002 to present, the weighted model greatly improved our predictions, but we quickly realized this was due to limiting the time period, not the new aggregate weather variables.
After some analysis on the date cutoff, we settled on 1995. 

Slide: Best Model

At this point, finally, our model including weather significantly out-performed the original model. This final model, the green line, missed actual prices by an average of 30 cents, or 17% of the average price - far more accurate than our old model, here represented by the grey line.

Going forward, we think including factors that represent demand and the cost of business could yield a more accurate model.

Now, I'm going to hand it off to Cari to discuss qualitative research and the effects of major events on Colombia coffee.