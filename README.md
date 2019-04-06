# [TWINT](https://github.com/twintproject/twint) - More practical (and optimized) use with Elasticsearch and Kibana

## See also [Twint Flask-Celery Server](https://github.com/Nedja995/twint_server) for http server


## Table of Contents
1. [Analyze keywords tutorial](#analyze-keywords-tutorial)
    - [Generate visualization](#generate-visualization)
2. [Share dashboard](#share-dashboard)  
3. [Optimized twint use](#optimized-twint-use)
4. [Tips](#tips)

## Requirements
- Python3, [Twint](https://github.com/twintproject/twint)
- Elasticsearch
- Kibana

## Analyze keywords tutorial

1. Create ES index with [index-tweets.json](elasticsearch/index-tweets.json)

2. Gather tweets containing keyword<br />
- `twint -s "<keyword>" --since 2019-1-1 -es localhost:9200 -it <es index name> --count`
- [Optimized](#optimized): `python3 utils/otwint.py -s "<keyword>" --since 2019-1-1 --until 2019-2-1 -es localhost:9200 -it "<es index name>" -rd 1 -mi 4`

3. Create Kibana Index Pattern

4. (optional) Add scripted field `shared_url_base` to Kibana Index Pattern using [painless_url_base.txt](elasticsearch/painless_url_base.txt)

5. Generate visualization and import in Kibana Saved Objects<br />
`python3 elasticsearch/generate_visualizations.py <Kibana index patter id> -n <optional (index)name>`
 
## Share dashboard
- Share responsive size Embeded iFrame with template [iframe_sampleword.html](sharing/iframe_sampleword.html)

## Optimized twint use
- New parametars: `-rd Request Days` and `-mi Maximum Instances to run`.

- `python3 utils/otwint.py -s "<keyword>" --since 2019-1-1 --until 2019-2-1 -es localhost:9200 -it "<es index name>" -rd 1 -mi 4`

### Tips
- Enable regex. In `/etc/elasticsearch/elasticsearch.yml` add line `script.painless.regex.enabled: true`

### TODO
- `user_created_at` (python script)
- resolve short urls (bit.ly,..) (python script)

### TODO: Automatize
After user enter parametars `keyword`, `since datetime`, `until datetime` do in backround
1. create ES index
2. create Kibana index pattern [Ref](https://gist.github.com/falkenbt/cace7f0bd1329d18699c022242491857) [Ref 2](https://github.com/elastic/kibana/issues/3709)
3. get new Kibana index id
4. generate visualizations
5. import visualization to Kibana Saved Objects
6. Kibana dashboard ready