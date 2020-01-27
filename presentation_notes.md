### Backstory

#### Hero

The data science day audience

#### The damsel

The individual farmer with a small 7 hectare farm

#### Problem

The Colombian coffee farmer is far more greatly affected by price volatility than the average US Starbucks customer.

When coffee farming becomes unprofitable, the small farmer often abandons coffee in favor of illegal crops or migrating to another country to pursue more viable livelihood. This causes further volatility in the market due to lack of consistent coffee production.

#### What idea do you want the audience to adopt?

We want the audience to see that price volatility is a negative

Volatility in the market will increase prices at your local coffee shop **



#### What are the stakes if people adopt our view or reject

If you adopt our view, millions of single family farmers around the world will have a more sustainable livelihood to provide for their families

if the status quo is maintained, price volatility will continue to funnel farmers towards the illicit drug trade.

#### New Bliss

A more stable South America. 

Audience: Price volatility impact consumer prices over the long term, which means more expensive coffeee for you and me at the grocery store.

Sphere of influence: Use your new founnd knowledge of the single family farmer to inspire your network to purchase fair trade coffee and support single family farms

Benefit to world: Colombia is a mircocosom of Latin American, South American, and the Western Hemisphre as a whole. A more stable single family farmer is a more stable Colombia. A more stable Colombia is a more stable Americas. 


### Presentation Structure

#### Beginning/Setting the scene
Presenter: Jeff
slide: cup of coffee
You have probably paid about the same for a cup of coffee as far back as you can remember. We were curious to see if changing weather patterns would threaten the price of America's motor: Caffeine. 

With that in mind we decided to look at the weather and coffee production of the most well known coffee producting country in the world: Colombia

Coffee grows best in volcanic soil, at altitudes of 1,200 to 1,800 meters, in places without frost, and receiving around 80 inches of rain a year. Colombia ticks all those boxes.

slide: picture of Colombia/ maybe Juan Valdez

Since 1995 Colombia has sold it's coffee to the market around $1.50 to $2 per pound. BUTTT

slide: flooding in Colombia

In 1997 heavy rain wiped out approximately 25% of Colombia's coffee plants. This caused global coffee prices to skyrocket to 2.5x the normal price. It took over 3 years for prices to return to normal. 70% of Colombia's coffee is produced by single family farmers. 

slide: Farmers like my friend Jaime rely on stable coffee prices to provide for their family.

Price spikes like this may cause a slight cost increase in your morning cup of joe, but for these farmers it destroys their livelihood.

Slide: show price over time with huge price spikes

Catastrophes like this can create 4x the normal volatility seen in the market

These types of events come in many forms: Weather, economic, plant disease, and political

*** Slide with examples of different incidences ***

#### Middle 
Presenter: Sam


slide: models compared to actual price

*** Briefly explain our data and its sources. 

The Data Robusta team set out to see if we could develop a model for predicting Colombian wholesale coffee prices. Our initial hypothesis was that temperature and more volatile precipitation would be strong drivers of coffee price. So does weather predict price? Like any good data scientist will tell you...it depends.

At first we tried several models using price, temperature, precipitation, production quantities to predict price. We found that Colombian weather was a very poor predictor of their coffee price. We experimented with various transformations of weather data, including date-shifting and weighting them by regional production quantities. While neither of those ideas panned out directly, the latter did inform some improvements in our model. Since we only had a regional breakdown of coffee production back to 2002, that model appeared to greatly improve our predictions, but we quickly realized this was due to limiting the time period, not the new aggregate weather variables.

Our improved model soley utilized coffee production quantity and prices from 1995 onward, but it still did not predict prices especially well. The mean price of coffee during this time was $1.80 per pound and the model calculated prices that miss the actual price by 37 cents (about 20%). We found that unpredictable events like plant disease, natural disasters, and major trade agreements drive extreme changes in the price of Colombian coffee. This led us to a pivitol point in our analysis. When splitting our model, one for "normal prices" plus or minus 20% of the average price and one to capture severe events, our models were able to reduce the calculated error down to 32 cents.

Going forward, we think it may yield a more accurate model to also include factors that would help predict demand and the cost of purchasing and transporting the coffee to destination. Including information such as US weather, crude oil prices, and the exchange rate between the US dollar and the Colombian Peso might account for these missing pieces and result in an even better model.


*** Possibly another visual showing models.

Presenter: Symeon
*** exploratory discoveries and quantitative analysis

Sam broke down the model and variables we ended up using to predict prices. I would like to talk to you about some of the insights we uncovered exploring the data. The exploration phase was instrumental in helping our team understand what was, and just as important, what wasn't driving price.

The coffee data came from the National Federation of Coffee Growers in Colombia, commonly known as Fedecafé. These spreadsheets included records of all coffee export prices in dollars per pound, going back to 1960. They also listed the monthly quantity of coffee produced in thousands of sixty kilogram bags. We acquired our weather data from the National Oceanic and Atmospheric Administration. We selected all precipitation and temperature data from 1960 to 2018. We filled in missing weather data using a forecasting tool from Facebook.

Sam mentioned the final model used only post 1995 years. After discovering the newer dates improved the model we explored the shape and distribution of the price over time. It was quickly apparent the prices were bimodal, with two very distinct patterns: pre and post 1995. This split left us with two unique price trends that were very close to normal distribution. This was very helpful in understanding why our model performed so much better with newer dates.

Slide: Bimodal Distribution

Next we asked ourselves: Does international production volume provide predictive power for Colombia's coffee price?

We compared Colombia's exports to that their geographic neighbor and coffee competitor, Brazil. We were looking for potential leading indicators from Brazil's exports that would move Colombia's exports/price in a predicable manner. 

Slide: Colombia and Brazil Exports

The graph here shows that there was not a strong predictor of Colombia's coffee price or production based on Brazil's coffee activity.

One very interesting insight we found. Was a drastic drop in the size of 




Huila, Antioquia, and Tolima produce about half of Colombia's coffee



Presenter: Cari
*** Showing our thought process and qualitative analysis

The data exploration identified the extreme price spikes, but it did not tell us what was creating them. We decide to take a deeper dive into the data and to see what was causing these spikes.

What we found was that coffee volatility can be created by several different types of events. Hard frost, trade agreements, exchange rates, and plant disease can all cause price spikes 2-10x the normal price. These events have serious long term effects on the price of coffee as well; prices can take 18 months to 5 years to return to normal levels.

In 1975, the now named Brazilian "Black Frost" destroyed 70% of Brazil's coffee plants. This caused prices to skyrocket to worldwide record highs and several years to return to normal. Coffee producing countries are not insulated from other countries' misfortunes affecting their own coffee export prices. Foreign disasters like this can be price beneficial to unaffected countries, but are not sustainable and make long term planning difficult for small farmers.

2002 emerging markets

In 2002, some interesting economic factors played a large part in the volatility of coffee prices. Coffee prices plummeted to a historic bottom of about 39 cents per pound, greatly due to the demand for coffee being much less than the supply of coffee produced. Coffee prices remained depressed through 2008. This forced the Federation of National Coffee Growers to reexamine its loyalty to the coffee industry as its number one priority. 

2011 plant disease

Plant disease is yet another concern for Colombian coffee farmers. Coffee rust is a yellow powdery fungi that spreads quickly and is devasting to harvests. Coffee rust ravaged Colombia's coffee farms from 2008 to 2011, reducing producting by over 30%. This reduction in output led to suboptimal coffee management and widespread food scarcity for farmers across the country.

#### End

To sum up the true impact of these staggering stats and stories. Price spikes come from many different directions and can be difficult to predict. Our model was adequate at predicting prices during periods of relative stability, but as a follow on project we would like to further develop our price spike model to identify early triggers of these types of events. We also believe a natural language processing model to examine local Colombian weather social media posts, FEDECAFE news, and trade/economic news would be very beneficial in assisting in predicting these major market disruptions and possibly even provide stable incomes for the more than half a million family coffee farmers of Colombia.



