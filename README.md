# es_post_filter_for_Splunk

_ES Post-filter for Splunk_


[![Build Status](https://github.com/Kintyre/es_post_filter_for_Splunk/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/Kintyre/es_post_filter_for_Splunk/actions)


## Install

This app is available for download and installation on [Splunkbase](https://splunkbase.splunk.com/apps/#/search/es_post_filter_for_Splunk/)
Additional details can be found [here](./.splunkbase/details.md).



## Example

Apply a filter to search results
```
index=_internal | `filter_results(splunk_internals,exclude)`
```

For reviewing a filter's generated case statement, run:

```
| `filter_expression_build_case(splunk_internals,include)`
```

## Danger

A single typo in the `where_expression` field can cause all searches using the same `filter_id` to fail at once.  Attempts to use `map` for eval validation have fallen flat.  Another possible approach to explore would be the use of the `search/parser` rest endpoint.

Look into "ast" endpoint (undocumented)



## Sourcetypes

| Sourcetype | Purpose |
| ---------- | ------- |
| kintyre:espostfilter  | Primary sourcetype |


## License

## Development

If you would like to develop or build this TA from source, see the [development](./DEVELOPMENT.md) documentation.

## Reference


This addon was built from the [Kintyre Splunk App builder](https://github.com/Kintyre/cypress-cookiecutter) (version 1.6.2) [cookiecutter](https://github.com/audreyr/cookiecutter) project.
