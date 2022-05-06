# es_post_filter_for_Splunk

_ES Post-filter for Splunk_

## Example usage

ES Post-filter for Splunk implements several macros used for building `where` clauses from lookup files and an eventing/streaming custom SPL search command called `parsespl`.


## Filtering example

Apply a filter to search results
```
index=_internal | `filter_results(splunk_internals,exclude)`
```

For reviewing a filter's generated case statement, run:

```
| `filter_expression_build_case(splunk_internals,include)`
```

## Danger

A single typo in the `where_expression` field can cause all searches using the same `filter_id` to fail at once.  This can be detected ahead of time using the `parsespl` command.  This sends in all expression to the `search/parser` rest endpoint.


## Parse-SPL command

**Syntax:**

```
parsespl mode=(search|eval|where|raw) (field=<field>|value=<str>)
```

**Examples:**

Simple do nothing example:
```
| makeresults | eval where_expr="true()" | parsespl mode=where field=where_expr
```

All good. No errors!  :-)


| makeresults | eval where_expr="notafunction()" | parsespl mode=where field=where_expr
```

Resulting message:  `Error in 'eval' command: The 'notafunction' function is unsupported or undefined.`


Probe saved searches for SPL errors:
```
| rest /servicesNS/-/-/saved/searches count=50
| table title eai:acl.app eai:acl.owner search
| parsespl mode=search field=search
| search error=*
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
| parsespl logging_level=DEBUG field=...
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
