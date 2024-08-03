let choice the one team like Man City which have id of b8fd03ef and find out its best lineup for the 2015/16 season.

let's do the data cleaning and preprocessing first.

the matches data frame look like this
```csv
0,2018-08-05,/en/comps/602/2018-2019/schedule/2018-FA-Community-Shield-Scores-and-Fixtures,/en/comps/602/2018-2019/schedule/2018-FA-Community-Shield-Scores-and-Fixtures,Sun,72724,Jonathan Moss,NaN,True,b8fd03ef,cff3d9bb,0,2,53,47,/en/players/101da2b5/Fernandinho,NaN,NaN,NaN,NaN,NaN,4-3-3,NaN,2018-08-05 15:00:00,0e0a9cee
1,2018-08-12,/en/comps/9/2018-2019/schedule/2018-2019-Premier-League-Scores-and-Fixtures,/en/comps/9/2018-2019/schedule/2018-2019-Premier-League-Scores-and-Fixtures,Sun,59934,Michael Oliver,NaN,True,18bb7c10,b8fd03ef,2,0,42,58,NaN,/en/players/101da2b5/Fernandinho,NaN,1.7,NaN,0.5,NaN,4-2-3-1,2018-08-12 16:00:00,478e9dab
2,2018-08-19,/en/comps/9/2018-2019/schedule/2018-2019-Premier-League-Scores-and-Fixtures,/en/comps/9/2018-2019/schedule/2018-2019-Premier-League-Scores-and-Fixtures,Sun,54021,Andre Marriner,NaN,True,b8fd03ef,f5922ca5,1,6,76,24,/en/players/d2bff301/Vincent-Kompany,NaN,4.2,NaN,0.7,NaN,3-1-4-2,NaN,2018-08-19 13:30:00,64ee90d5
3,2018-08-25,/en/comps/9/2018-2019/schedule/2018-2019-Premier-League-Scores-and-Fixtures,/en/comps/9/2018-2019/schedule/2018-2019-Premier-League-Scores-and-Fixtures,Sat,31322,Martin Atkinson,NaN,True,8cec06e1,b8fd03ef,1,1,29,71,NaN,/en/players/d2bff301/Vincent-Kompany,NaN,1.6,NaN,1.0,NaN,4-3-3,2018-08-25 12:30:00,a25a3f33
4,2018-09-01,/en/comps/9/2018-2019/schedule/2018-2019-Premier-League-Scores-and-Fixtures,/en/comps/9/2018-2019/schedule/2018-2019-Premier-League-Scores-and-Fixtures,Sat,53946,Kevin Friend,NaN,True,b8fd03ef,b2b47a98,1,2,78,22,/en/players/e2716bd0/David-Silva,NaN,2.0,NaN,0.5,NaN,4-1-3-2,NaN,2018-09-01 17:30:00,f74a4680

```

First to remove duplicates, and sort the matches by date and extract the league ids


```python

for match in matches:
    match = remove_duplicates_from_csv(match, 'id')
    match['league'] = match['league'].str.split('/')
    match['league'] = match['league'].apply(lambda x: x[3])
    match.drop(columns=['Round'], inplace=True)
```




