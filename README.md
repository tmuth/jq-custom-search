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
Combine keys in one array with values in another array
```
| makeresults count=1
| eval json="{\"result\":{ \"event.AuditKeyValues{}.Key\": [ \"name\", \"gender\", \"employee\", \"email\"],\"event.AuditKeyValues{}.ValueString\": [ \"tyler\", \"male\", \"yes\", \"tyler@nowhere.com\"],\"foo\": \"1\",\"bar\": \"2\"}}"
| jq input=json output=json_original args="-r" split="" filter="."
| jq input=json output=json_new args="-r" split="" filter=".result | [.\"event.AuditKeyValues{}.Key\", .\"event.AuditKeyValues{}.ValueString\"] | transpose | map({(.[0]): .[1]}) | add"
| table json_original,json_new
```
