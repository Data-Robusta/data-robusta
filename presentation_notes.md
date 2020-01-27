### Presentation Structure

#### Beginning/Setting the scene
Presenter: Jeff
slide: cup of coffee

Good afternoon, i'm Jeff Roeder, this is Sam Callahan, this is Symeon White, and Cari Holmes. We are data scientists for Data Robusta.

slide: flooding in Colombia

In 1997 heavy rain wiped out approximately 25% of Colombia's coffee plants. This caused global coffee prices to skyrocket to 2.5x the normal price. It took over 3 years for prices to return to normal. These types of events come in many forms: natural distasters, economic, plant disease, and political and greatly affects Colombia's single family farmers that produce 70% Colombia's coffee. 
(awkward ending)

slide: Jaime and his fam

Farmers like my friend Jaime rely on stable coffee prices to provide for their family and events like the floods of 1997 are devestating for them.

Price fluctuations may cause a slight cost increase in your morning cup of joe, but for farmers like Jaime it destroys their livelihood.

Slide: Goal/Hypothesis

Coffee is $200 billion industry and the second most traded commodity worldwide. Knowing that coffee is such an important global product; we decided to take a deep dive into the most well known coffee producting country in the world: Colombia

We set out to find the effect of Colombian weather and harvest data as predictors for price. In the end we found that while weather was decent at predicting weather, there were much stronger factors at play driving price.

Slide: Process slide
We are going to walk you through our work of in depth domain research, wrangling, exploring, analyzing, and predicting price. 

How does this affect you and I? Why should we care a world away if Colombia is in a multi year drought, dealing with a coffee plant disease epidemic, or about to sign the next big trade agreement?

Worldwide and Colombian governments and NGOs have been fighting for decades to stabalize and convert farmers from illicit drugs crops to legal means of providing for their families. A stable and healthy coffee economy is a key pillar of that transformation and Colombia's economy as a whole.

what can data bring to this fight?

Slide: Wrangle: 

We fused data from Colombian weather stations, national growers reports, and international commodity market activity to paint a clear picture about the impact of coffee price for us as consumers; as well as for the local farmer in the hills of Colombia. ...initial challenges with the data and predicting missing values bla blah

Catastrophes like this can create 3x the normal market volatility and lengthy periods of price uncertainty. As data scientists we created models to aid in long term crop forcasting and assisting Colombia's National Coffee Federation manage long price spikes with optimized stockpile quantity.

I'm going to hand it off to Symeon to talk about the in depth exploration conducted by our team.
(transition to Symeon)



#### Middle 

I’m going talk about some of the insights we uncovered exploring the data from the National Federation of Coffee Growers and the National Oceanaic and Atmospheric Administration. The exploration phase was instrumental in helping our team understand what was, and just as importantly, what wasn’t driving price.

(Slide: Bimodal Distribution)

 the model we explored the shape and distribution of the price over time. It was quickly apparent the prices were bimodal, with two distinct distributions: one pre 1995 and one post 1995. This split left us with two unique price trends that were normally distributed. Attempting to model these together would be the equivalent of attempting to model car production rates pre and post Henry Ford's asseumbly line.

 Slide: weather stuff


Next we asked ourselves: Do international export volumes of coffee provide predictive power for Colombia’s coffee price?

Slide: Colombia and Brazil Exports

Next we asked ourselves: Do international export volumes of coffee provide predictive power for Colombia’s coffee price?
We aquired additional data from the Observatory of Economic Complexity; this provided us with coffee export data for Brazilian and Colombian coffee.
We had chosen to use Brazil as it was the next largest producer of coffee.
We analyzed the Brazilian data for indicators that would ahead of time influence Colombia’s exports or price.
After comparing Colombia’s exports to that of Brazil’s we determined that there was no early indicators given off by Brazilian export data.
The graph here shows that there was no early indications given reagarding Colombia’s production based on Brazil’s prior activity,meaning Brazilian and Colombian production tend to move in concert.



Presenter: Sam
 
 Slide: Prophet

The Data Robusta team set out to see if we could develop a model for predicting Colombian wholesale coffee prices. Our initial hypothesis was that temperature and more volatile precipitation would be strong drivers of coffee price. So does weather predict price? Like any good data scientist will tell you...it depends.


slide: Just price over time

At first we tried several models using price, temperature, precipitation, and production quantities to predict price. We found that Colombian weather was a very poor predictor of their coffee price. We experimented with various transformations of weather data, including date-shifting and weighting them by regional production quantities. While neither of those ideas panned out directly (fix wording), the latter did inform some improvements in our model. Since we only had a regional breakdown of coffee production back to 2002, that model appeared to greatly improve our predictions, but we quickly realized this was due to limiting the time period, not the new aggregate weather variables.

slide: improved model (old best model)


Our improved model used just coffee production quantity and prices from 1995 onward, but it still did not predict prices especially well. The mean price of coffee during this time was $1.80 per pound and the model calculated prices that miss the actual price by 37 cents (about 20%). We found that unpredictable events like plant disease, natural disasters, and major trade agreements drive extreme changes in the price of Colombian coffee. 

slide: best model

This led us to a pivitol point in our analysis. When splitting our model, one for "normal prices" plus or minus 20% of the average price and one to capture severe events, our model was able to reduce the calculated error down to 32 cents.


Going forward, we think it may yield a more accurate model to also include factors that would help predict demand and the cost of purchasing and transporting the coffee to destination. Including information such as US weather, crude oil prices, and the exchange rate between the US dollar and the Colombian Peso might account for these missing pieces and result in an even better model.


Presenter: Cari
*** Showing our thought process and qualitative analysis

slide: price spike with timeline

The data exploration identified extreme price spikes, but it did not tell us what was creating them. We decide to take a deeper dive into the data and to see what was causing these lengthy disruptions.

What we found was that coffee volatility can be created by several different types of events. Hard frost, trade agreements, exchange rates, and plant disease can all cause price spikes (change verbage) 2-10x the normal price. 

slide: baby and adult plants

These events have serious long term effects on the price of coffee as well; prices can take 18 months to 5 years to return to normal levels. This is largely caused by the long maturation process of the plant. Coffee plants take 3 to 4 years to start producing their fruit. 
(awkward transition to next paragraph)

In 1975, the Brazilian "Black Frost" destroyed 70% of Brazil's coffee plants. This caused prices to skyrocket to worldwide record highs and several years to return to normal. Coffee producing countries are not insulated from other countries' misfortunes affecting their own coffee export prices. Foreign disasters like this can be price beneficial to unaffected countries, but are not sustainable and make long term planning difficult for small farmers.

2002 emerging markets

In 2002, some interesting economic factors played a large part in the volatility of coffee prices. Coffee prices plummeted to a historic bottom of about 39 cents per pound, largely due to the demand for coffee being much less than the supply of coffee produced. Coffee prices remained depressed through 2008. This forced the Federation of National Coffee Growers to reexamine its loyalty to the coffee industry as its number one priority. 
(awkward sentence about coffee federation not interested in coffee)

2011 plant disease

Plant disease is yet another concern for Colombian coffee farmers. Coffee rust is a yellow powdery fungi that spreads quickly and is devasting to harvests. Rust ravaged Colombia's coffee farms from 2008 to 2011, reducing production by over 30%. This reduction in output led to suboptimal coffee management and widespread food scarcity for farmers across the country.

#### End

To sum up the true impact of these staggering stats and stories.

Price instability in the markets affects real people

As data scientists we created models to aid in long term crop forcasting and assisting Colombia's National Coffee Federation manage long price spikes with optimized stockpile quantity.
 
 
 We believe we can futher contribute to Colombian coffee farmer success by...a follow on project we would like to further develop our price spike model to identify early triggers of these types of events. 
We also believe a natural language processing model to examine local Colombian weather social media posts, FEDECAFE news, and trade/economic news would be very beneficial in assisting in predicting these major market disruptions. Data science will be part of the future success of providing a stable economy for the more than half a million family coffee farmers of Colombia and those of us around that world that enjoy their coffee.

(using "price spike" too frequently)



