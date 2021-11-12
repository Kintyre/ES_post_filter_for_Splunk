#!/usr/bin/env python
# coding=utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

__version__ = "0.1.0"

import os
import sys
import json
import functools

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "lib"))  # nopep8
from splunklib.searchcommands import dispatch, EventingCommand, Configuration, Option, validators

from splunklib.client import HTTPError


@Configuration()
class ParseSplCommand(EventingCommand):

    mode = Option(
        require=False,
        default="search",
        validate=validators.Set("search", "raw", "eval", "where"))

    field = Option(
        require=False,
        validate=validators.Fieldname())

    value = Option(
        require=False)

    # Run on SH only (do not distributed to indexers)
    distributed = False

    # Don't allow this to run in preview mode to limit API hits
    run_in_preview = False

    """
    *** Method-level stuff ***

    # Log the commands given to the SPL command:
    self.logger.debug('ParseSplCommand: %s', self)

    # Access metadata about the search, such as earliest_time for the selected time range
    self.metadata.searchinfo.earliest_time

    *** Runtime / testing ***

    Enable debug logging:

        ... | parsespl logging_level=DEBUG ...

    """

    def prepare(self):
        super(ParseSplCommand, self).prepare()
        will_execute = bool(self.metadata.searchinfo.sid and
                            not self.metadata.searchinfo.sid.startswith("searchparsetmp_"))
        '''
        if will_execute:
            self.logger.info("Launching version %s", __version__)
        '''

        if self.fieldnames:
            self.write_error("The following arguments to parsespl are "
                             "unknown:  {!r}  Please check the syntax.", self.fieldnames)
            sys.exit(1)

        # Ensure that we either have 'field' or 'value' but not both:
        have_field = bool(self.field)
        have_value = bool(self.value)

        if not have_field ^ have_value:
            self.write_error("Please provide either a reference 'field' or an "
                             "expresion in 'value', but not both")
            sys.exit(1)

        if not have_field:
            self.write_error("Only field is currently implemented.")
            sys.exit(1)
            # In value mode, we switch into a 'generating' commands not a eventing command

    @functools.lru_cache(1000)
    def parse_search(self, query):
        data = error = None
        try:
            response = self.service.get("search/parser", q=query, output_mode="json")
            data = json.load(response.body)
        except HTTPError as e:
            try:
                data = json.loads(e.body)
                error = [m["text"] for m in data["messages"]]
            except (ValueError, TypeError):
                error = [str(e)]
        if error:
            return error, data
        else:
            return "", data

    @staticmethod
    def normalize_search(spl):
        if not spl.strip().startswith("|"):
            spl = "search " + spl
        return spl

    def transform(self, records):
        mode = self.mode
        field = self.field

        if mode == "search":
            translate = self.normalize_search
        elif mode == "eval":
            def translate(s): return "makeresults | eval {}".format(s)
        elif mode == "where":
            def translate(s): return "makeresults | eval cond = if({}, 0, 1)".format(s)
        else:
            def translate(s): return s

        for record in records:
            query = record.get(field, None)
            if query:
                expr = translate(query)
                '''
                if expr != query:
                    self.logger.info("Translated %r to %r", query, expr)
                else:
                    self.logger.info("[%s] Keeping %r", mode, expr)
                '''
                try:
                    status, info = self.parse_search(expr)
                    if info and isinstance(info, dict):
                        info = json.dumps(info, indent=2)
                    record["error"], record["info"] = status, info
                except Exception as e:
                    self.logger.exception("Error while handling %s expression:  %s", mode, expr)
                    raise
            else:
                # Silently ignore any records without 'field'; keep output field placeholder
                record["status"] = record["info"] = None

            yield record


if __name__ == '__main__':
    dispatch(ParseSplCommand, sys.argv, sys.stdin, sys.stdout, __name__)
