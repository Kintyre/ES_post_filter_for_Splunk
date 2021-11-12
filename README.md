# es_post_filter_for_Splunk

_ES Post-filter for Splunk_

## Example usage

ES Post-filter for Splunk implements a eventing custom SPL search command called `parsespl`.

```
| parsespl type=robot height=tall

| parsespl action=ping target=fancy_pig
```

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
| command:parsespl | Internal logs and stats related to custom Kintyre ES Post Filter SPL command. |


## Troubleshooting

Find internal/script errors:

### Enable debug logging

Add `logging_level=DEBUG` to your existing query to enable additional debug logs:

```
| parsespl logging_level=DEBUG query=...
```

### Search internal logs

Search for the above debug logs, or other messages from or about the KintyreSPL search command:

```
index=_internal (source=*kintyre_es_post_filter.log*) OR (sourcetype=splunkd parse_spl.py)
```

Review SPL search command logs group by request:

```
index=_internal sourcetype=command:parsespl | transaction host Pid
```

## License

## Development

If you would like to develop or build this TA from source, see the [development](./DEVELOPMENT.md) documentation.

## Reference

 * **API Docs**:  https://....


This addon was built from the [Kintyre Splunk App builder](https://github.com/Kintyre/cypress-cookiecutter) (version 1.6.2) [cookiecutter](https://github.com/audreyr/cookiecutter) project.
