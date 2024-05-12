Azure Content Safety Testing
--

Testing toxcity strings provided via CSV against mpathic's api endpoint to see how they work.

```
poetry run python3 azcstesting.py   
```

Requires an enviornmental variable calle "BEARER_TOKEN" provided from the mpathicAPI.

Expects a csv with a column called 'text' with utterances.
Provides a csv with positive matches of AZCS hits.

