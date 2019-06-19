# Target Selection
---
#### Motivation
In preparation for building a player projection model, we sought to identify a metric that represented a player's 'value' at the season level that was a leading indicator of the player's future performance in subsequent seasons. This leading indicator would serve as our target variable when attempting to build a model that would effectively predict future performance. To determine which metric was the best leading indicator we calculated the pairwise cross-correlation of Box Plus-Minus (BPM), Real Plus-Minus (RPM), Net Rating, Wins (RPM Wins), VORP (Value Over Replacement Player), and WOR (Wins Over Replacement) for all players since the 2004-2005 season to determine the seasonal-lead (or lag) between the two metrics. The distribution of these seasonal-leads across all players provides evidence of which metrics lead or lag others.

After examining the resulting distributions of all pairwise metric comparisons, we determined that BPM is the best target variable candidate for our player projection modeling. It leads all other metrics mentioned above and does so consistently when this process was repeated using only those players that met the starter-criteria (>2000 MP), met a fringe-player criteria (>500 MP), or played since the 2013-2014 season (when RPM first became available). This finding coincides with that of the [538 Player Projection model](https://fivethirtyeight.com/methodology/how-our-nba-predictions-work/), one of the most prevalent public models, which uses a blend of BPM and RPM as its target variable.

The following documentation describes our data sources, methodology, and additional findings which will later influence our player projection model.

![BPM Normalized Cross Correlation](/Plots/Full_Sample/BPM_Cross_Correlation.png)

---
#### Methodology
In an attempt to quantify the lead or lag between two metrics, we utilized
[Cross-Correlation](https://en.wikipedia.org/wiki/Cross-correlation), a measure of similarity between two time series. This will tell us that if two metrics move in perfect synchrony they will be most correlated with a seasonal lag of 0. If instead one metric lags another by 1 season they will be most correlated with a season lag of 1. To exemplify this let's use a hypothetical player:

Simple Example: Two time series lagged by one season.

Simple Player Example: Two metrics of a player with one lagging the other.

MP vs. RPM, BPM, and VORP Example.
    - If two metrics moved in perfect synchrony, the distribution would be perfectly normal. If instead, one metric leads another the distribution will be skewed in either direction.

When run in a pairwise-fashion between all metrics we can see whether a metric in question leads or lags all other metrics. Using Minutes Played (MP) as an example below we see that MP lags all major box-score metrics indicating that a player's future minute total lags behind his current on-court performance. This makes intuitive sense as players who play well are subsequently rewarded with more minutes the following season and those who under-perform see their minutes played decrease.

![MP Normalized Cross Correlation](/Plots/Full_Sample/MP_Cross_Correlation.png)

One question we had during this process was if these findings held true across smaller subsets of the data. We ran this same analysis using only players that met the NBA-defined starter criteria of 2,000+ MP in addition to a self-defined fringe-player criteria of 500+ MP and observed the same results. Similarly, we were curious if the findings would hold true if the data was limited to only those seasons since 2013 when RPM was first introduced and in fact we did see similar results but less drastic. It appears that RPM and BPM are quite similar, which may provide an explanation of why 538's model uses a blend of the two.

---
#### Additional Findings
We were able to show that MP lags the majority of major box-score metrics. We were also curious if salary payouts would do the same. This might answer the question of if players are paid for future or historical performance. Using this same process we looked at Salary (raw dollar amount) and Salary Cap Prop (the proportion of the league salary cap) each of which told the same story. Salary is a leading indicator of most box-score metrics, with the exception of BPM, in addition to MP. This suggests that teams on average are correctly paying players for future performance.

![Salary Normalized Cross Correlation](/Plots/Full_Sample/Salary_Cross_Correlation.png)

![Salary Cap Prop Normalized Cross Correlation](/Plots/Full_Sample/Salary_Prop_Cap_Cross_Correlation.png)

---
#### Data
BPM, VORP, WOR, and Net Rating were all scraped from Basketball-Reference, while RPM and Wins were scraped from ESPN. Additionally, salary data was scraped from Basketball-Reference.
