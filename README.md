# jq-custom-search
jq Custom Search command wrapper for Splunk

## Installation
You must install the jq binary first

## Examples
Simple JSON Reformat
```
| makeresults count=1
| eval json="{\"fruit\":{\"name\":\"apple\",\"color\":\"green\",\"price\":1.20}}"
| jq input=json output=json_new args="-r" split="" filter=".fruit"
```
Extract Just a value based on a key
```
| makeresults count=1
| eval json="{\"fruit\":{\"name\":\"apple\",\"color\":\"green\",\"price\":1.20}}"
| jq input=json output=json_new args="-r" split="" filter=".fruit.color"
```
