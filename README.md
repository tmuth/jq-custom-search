# jq-custom-search
jq Custom Search command wrapper for Splunk that exposes the jq binary from https://stedolan.github.io. jq is a lightweight and flexible command-line JSON processor. jq is like sed for JSON data - you can use it to slice and filter and map and transform structured data with the same ease that sed, awk, grep and friends let you play with text.

## Installation
You must install the jq binary first

## Parameters
**input** this is the Splunk field that contains the json you wish to transform

**output** is the name of the field that this command will create with the output of the transform

**args** are the jq parameters documeted here https://stedolan.github.io/jq/manual/#Invokingjq. `-r` should be used within Splunk. The other parameters are optional. 

**split** is used to split a single Splunk event into multiple events based on a boundary string. The use-case is json field that actually contains multiple events. 

**filter** is the jq filter or transform logic used to manipulate the json document. 

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
Combine keys in one array with values in another array
```
| makeresults count=1
| eval json="{\"result\":{ \"event.AuditKeyValues{}.Key\": [ \"name\", \"gender\", \"employee\", \"email\"],\"event.AuditKeyValues{}.ValueString\": [ \"tyler\", \"male\", \"yes\", \"tyler@nowhere.com\"],\"foo\": \"1\",\"bar\": \"2\"}}"
| jq input=json output=json_original args="-r" split="" filter="."
| jq input=json output=json_new args="-r" split="" filter=".result | [.\"event.AuditKeyValues{}.Key\", .\"event.AuditKeyValues{}.ValueString\"] | transpose | map({(.[0]): .[1]}) | add"
| table json_original,json_new
```
