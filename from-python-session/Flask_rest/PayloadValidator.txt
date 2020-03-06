#!/usr/bin/env python
# encoding: utf-8
"""
Licensed Materials - Property of IBM
(C) Copyright IBM Corp. 2017,2018. All Rights Reserved.
US Government Users Restricted Rights - Use, duplication or disclosure
restricted by GSA ADP Schedule Contract with IBM Corp.
"""
import json

from flask_restplus import abort
from werkzeug.exceptions import BadRequest

NO_WHITESPACE_REGEX = "^[^-\s].*$"
NO_WHITESPACE_SPECIALCHAR_REGEXP = "^([^\!\^\&\`\s\:\/\\\[\]\:\;\|\=\,\*\?\<\>])+$"
NO_UNICODE_SPECIALCHAR_REGEXP = "^(?:(?![!&^\s:\/\\\[\]\:\;\|\=\,\*\?\<\>])[\x00-\x7F])+$"
NO_SPECIAL_CHAR_ALLOW_UNDERSCORE = "^([a-zA-Z0-9_]*)$"
INVALID_PAYLOAD = "Input payload validation failed"
RANGE_0_TO_1000 = "^([0-9][0-9]{0,2}|1000)$"


def validate_payload(self, func, baseclass):
    """
    :param self:
    :param func:
    :param baseclass:
    """
    try:
        super(baseclass, self).validate_payload(func)
    except BadRequest as e:
        # pylint: disable=maybe-no-member
        if hasattr(e, 'data'):
            message = e.data
            if e.data['message'] == INVALID_PAYLOAD and NO_WHITESPACE_REGEX in next(iter(e.data[
                    'errors'].values())).replace(
                        "\\\\", "\\"):
                cust_msg = "field: '{0}' can't be empty " \
                           "or start with white space ".format(
                               next(iter(e.data['errors'])))
                cust_res = {"msg": str(e.data['errors'])}
                message['errors'] = cust_res
            elif e.data['message'] == INVALID_PAYLOAD and NO_WHITESPACE_SPECIALCHAR_REGEXP in next(iter(e.data[
                    'errors'].values())).replace(
                        "\\\\", "\\"):
                cust_msg = "field: % s can't be empty or start " \
                           "with white space or / \\ [] : | =, * ? < > are " \
                           "not allowed ", next(iter(e.data['errors']))
                cust_res = {"msg": str(e.data['errors'])}
                message['errors'] = cust_res
            elif e.data['message'] == INVALID_PAYLOAD and NO_SPECIAL_CHAR_ALLOW_UNDERSCORE in next(iter(e.data[
                    'errors'].values())).replace(
                        "\\\\", "\\"):
                cust_msg = "field: '{0}' only _ and alphanumeric " \
                           "characters are allowed ".format(
                               next(iter(e.data['errors'])))
                cust_res = {"msg": str(e.data['errors'])}
                message['errors'] = cust_res
            abort(400, json.dumps(message))
        else:
            abort(400, json.dumps(e))
