# es_post_filter_for_Splunk

_ES Post-filter for Splunk_

## Example usage

ES Post-filter for Splunk implements a eventing custom SPL search command called `parsespl`.

```
| parsespl type=robot height=tall

| parsespl action=ping target=fancy_pig
```

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
