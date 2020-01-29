### Presentation Structure
#### Beginning/Setting the scene
Presenter: Jeff

slide: cup of coffee

Good afternoon, this is Symeon White, Sam Callahan, Cari Holmes and I'm Jeff Roeder. We are data scientists for Data Robusta.

slide: flooding in Colombia

In 1997 heavy rain wiped out approximately 25% of Colombia's coffee plants. This caused global coffee prices to skyrocket to 2.5x the normal price. It took over 3 years for prices to return to normal. Events like this come in many forms: natural distasters, economic, disease, and political and greatly affect Colombia's single family farmers that produce 70% Colombia's coffee.
(awkward ending)

slide: Jaime and his fam

Farmers like my friend Jaime rely on stable coffee prices to provide for their family and events like the floods of 1997 are devestating for them.

Why should we care if Colombia is in a multi year drought or about to sign the next big trade agreement?

Governments and NGOs have been fighting for decades to convert farmers from illicit drugs crops to legal means of providing for their families. 

A stable and healthy coffee economy is key to Colombia's economy.

Price fluctuation may cost you a bit more on morning coffee run, but for farmers like Jaime it destroys their livelihood.

what can data science bring to this fight?

As data scientists we have the ability to uncover new insights and validate already existing knowledge through cutting edge analytic techniques and modeling.

Slide: Goal/Hypothesis

Our goal was to identify what data affected Colombian coffee prices. Our hypthosis was that weather and harvest data were good predictors of price. We found that while weather was decent at predicting weather, there were much stronger factors at play.

Slide: Process slide

We analyzed Colombian history, agricultural processes, and political effects on price.

Slide: Wrangle:

We fused data from weather stations and national harvest reports to paint a clear picture about the impact of coffee price for us as consumers; as well as for the local farmer in the hills of Colombia.

Catastrophes like this can create 3x the normal market volatility and lengthy periods of price uncertainty. We used time series analysis to create models to aid in long term crop forcasting and to assist Colombia's National Coffee Federation manage long price flucuations.

I'm going to hand it off to Symeon to talk about the in depth exploration conducted by our team.
(transition to Symeon)
2:40
#### Middle

Presenter: Symeon
*** exploratory discoveries and quantitative analysis
Fed - eh - cafeh

(Slide: FEDECAFE and NOAA pics)

I’m going walk us though some of the insights we uncovered exploring the data from the National Federation of Coffee Growers of Colombia known as Fedecafe and the National Oceanaic and Atmospheric Administration known as NOAA.

The exploration phase was instrumental in driving our teams understanding of what was, and just as importantly, what wasn’t driving price.

(Slide: NOAA mean_temp/min_temp and Fedecafe price over time)

After visualizing some of the data we aquired from NOAA you can see it appears to have a correlation between the mean temperature, the minimum temperature , and the price, year over year. After statistically analyzing the results it was determined the results did not have a significant correlation.

(Slide: Bimodal Distribution/ two normal dists)

In the early 90s, Fedecafe worked closely with Colombian farmers, helping them learn more advanced farming techniques.
Their effect on prices became more evident during exploration where we found prices were bimodal; from this two normal distributions can be created, one for pre-1995 and one for post-1995 data, both with unique trends and volatility.

The shift in trends and volatility can be largly attibuted to Fedecafe’s involvement to create long-term sustainability of family farms which lead to a more stable coffee economy.

(Slide: Colombia and Brazil Exports)

Next we asked ourselves: Do international export volumes of coffee provide predictive power for Colombia’s coffee price?
We aquired additional data from the Observatory of Economic Complexity which provided us with coffee export data both internationally and for Colombian.

We had chosen to compare Colombia’s exports to that of Brazil as it is the next largest producer of coffee.
We analyzed the Brazilian data for indicators that would ahead of time influence Colombia’s exports or price.
After comparing Colombia’s exports to that of Brazil’s as can be seen in this graph, we determined that there was no early indicators given off by Brazilian export data.

4:55

Presenter: Sam
 
Slide: Prophet
​
Hi I'm Sam. I acquired data from FEDECAFE and NOAA, used time series modeling to fill in missing data, and modeled prices.
​
The Data Robusta team wanted to see if we could develop a model for predicting Colombian wholesale coffee prices in 2018 dollars per pound. Our initial hypothesis was that temperature and more volatile precipitation are strong drivers of coffee price. So does weather predict price? Like any good data scientist will tell you...it depends.
​
We initially tried models using all of our available features: price, temperature, precipitation, and production quantities to predict price. We used Prophet, a time-series modeling library developed by Facebook, to create these models. Prophet models create three functions: an overall trend, seasonal trends, and holiday trends. These come together to predict the overall pattern of temporal data.
​
Slide: Price over time and baseline model
​
Initially, climate data appeared to worsen our models; our best early model only used prior prices and production quantities. We experimented with various transformations of weather data, including date-shifting and weighting them by regional production quantities. While these changes did not result in better predictions than the models that excluded weather data, they did provide a key insight for later models. 
​
Since we only had regional production data from 2002 to present, that model appeared to greatly improve our predictions, but we quickly realized this was due to limiting the time period, not the new aggregate weather variables.
After some analysis on the date cutoff, we settled on 1995. 
​
Slide: Best Model
​
At this point, finally, our model including weather did significantly out-perform the model solely using quantity and price. This final model missed actual prices by an average of 30 cents, or 17% of the average price.
​
Going forward, we think including factors that represent demand, cost of business, and the exchange rate between the US Dollar and Colombian Peso could yield a more accurate model.


7:08

Presenter: Cari
*** Showing our thought process and qualitative analysis

slide: price spike with timeline

The data exploration identified extreme price spikes, but it did not tell us what was creating them. We decided to take a deeper dive into the data to see what was causing these lengthy disruptions.
We found that coffee volatility can be caused by several different types of events. Hard frost, trade agreements, exchange rates, and plant disease can all cause fluctuations from 2-10x of the normal price.

slide: baby and adult plants

These events have serious long term effects on the price of coffee as well; prices can take 18 months to 5 years to return to normal. This is because coffee plants take 3 to 4 years to start producing their fruit.

In 1975, the Brazilian "Black Frost" destroyed 70% of Brazil's coffee plants, causing prices to skyrocket for several years. Nation Coffee prices are not insulated from other countries' misfortunes. Such disasters can benefit unaffected countries in the short term, but make long term planning difficult for farmers.

2002 emerging markets

In the years leading up to the crash, farmers were aggresively expanding their farms.In 2002, Coffee prices plummeted to a 39 cents per pound, due to a sharp decrease in global demand. 


Coffee prices remained depressed through 2008. This forced the Fe Growers to reexamine its loyalty to the coffee industry as its number one priority.

2011 plant disease

Plant disease is yet another concern for Colombian coffee farmers. Coffee Rust destroyed 30% of  Colombia's coffee farms from 2008 to 2011. This reduction in output led to suboptimal coffee management and widespread food scarcity.

#### End

Coffee is $200 billion industry and the second most traded commodity worldwide. Knowing that coffee is such an important global product; we decided to take a deep dive into the most well known coffee producting country in the world: Colombia

Price instability in the markets affects real people, but as 
data scientists we can bring some clarity to their problem. We created models to aid in thier long term crop forcasting and assisting Colombia's National Coffee Federation manage long term price flucuations with optimized stockpile quantity.

We also believe a natural language processing model to examine local Colombian weather social media posts, FEDECAFE news, and trade/economic news would be very beneficial in assisting in predicting these major market disruptions. Data science will be part of the future success of providing a stable economy for the more than half a million family coffee farmers of Colombia and those of us around that world that enjoy their coffee.

Please come by our booth to sample some delicous Colo,bian coffee and to hear more about our project.

10:33