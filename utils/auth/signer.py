#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
# =============================================================================
#      FileName: signer.py
#          Desc: hw ak,sk signer
#        Author: Dong Wei Chao
#         Email: 435904632@qq.com
#      HomePage: https://github.com/hyperwd
#       Version: 0.0.1
#    LastChange: 2018-08-13 15:37:21
#       History:
# =============================================================================
'''
import datetime
import hashlib
import hmac
from urllib.parse import quote
import requests


class SignError(Exception):
    """Docstring for SignError. """
    pass


#    def __init__(self):
#        """TODO: to be defined1. """
#        Exception.__init__(self)


class Sign(object):
    """Docstring for Sign. """

    def __init__(self,
                 access_key,
                 secret_key,
                 req_method,
                 req_host,
                 req_uri,
                 x_project_id=None,
                 req_query_param=None,
                 req_custom_headers=None,
                 req_body=None,
                 req_timeout=10):
        """TODO: to be defined1.

        :access_key: ak
        :secret_key: sk
        :req_method: GET,POST,PUT等
        :req_host: 请求url,例如 ecs.cn-north-1.myhuaweicloud.com
        :req_uri: 请求资源路径,例如/v2/tenant_id/servers/
        :x_project_id: str类型,单个子项目id
        :req_query_param: dict类型,请求查询参数,例如{'name':'xxx','status':'ACTIVE'}或为空
        :req_custom_headers: dict类型,自定义请求头信息，可任意增加
        :req_body: str类型,请求消息体
        :req_timeout: 设置请求超时时间，默认10秒

        """
        self._access_key = access_key
        self._secret_key = secret_key
        self._req_method = req_method
        self._req_host = req_host
        self._req_uri = req_uri
        self._x_project_id = '' if x_project_id is None else x_project_id
        self._req_query_param = {} if req_query_param is None else req_query_param
        self._req_custom_headers = {} if req_custom_headers is None else req_custom_headers
        self._req_body = '' if req_body is None else req_body
        self._req_timeout = req_timeout

    @staticmethod
    def get_signature_key(secret_key, date_stamp, region_name, service_name):
        """Key derivation functions

        :secret_key: sk
        :date_stamp: 请求时间戳
        :region_name: 资源所在region名称
        :service_name: 请求的服务名称
        :returns: 加密后的key

        """
        key = ('SDK' + secret_key).encode('utf-8')
        for d_v in [date_stamp, region_name, service_name, 'sdk_request']:
            key = hmac.new(
                key=key, msg=d_v.encode('utf-8'),
                digestmod=hashlib.sha256).digest()
        return key

    @staticmethod
    def query_string(idict):
        """TODO: Docstring for query_string.

        :idict: TODO
        :returns: TODO

        """
        que_list = []
        for key, value in idict.items():
            if value == '':
                k_v = quote(key)
            else:
                k_v = quote(key) + '=' + quote(value)
            que_list.append(k_v)
        que_list.sort()
        return '&'.join(que_list)

    def sign(self):
        """TODO: Docstring for sign.
	:returns: TODO

	"""
        self.req_date = datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
        self.req_datestamp = datetime.datetime.utcnow().strftime(
            '%Y%m%d')  # Date w/o time, used in credential scope
        self.algorithm = 'SDK-HMAC-SHA256'
        self.req_region = self._req_host.split('.')[0]
        self.req_service = self._req_host.split('.')[1]

        # ************* TASK 1: CREATE A CANONICAL REQUEST *************
        # Step 1 is to define the verb (GET, POST, etc.)--alredy done--slef.req_method.
        # Step 2: Create canonical URI--the part of the URI from domain to
        # query---already done--self._req_uri
        # Step 3: Create the canonical query string.--use func query_string above

        self.canonical_querystring = self.query_string(self._req_query_param)

        # Step 4: Create the canonical headers and signed headers. Header names
        # must be trimmed and lowercase, and sorted in code point order from
        # low to high. Note that there is a trailing \n.

        self.canonical_headers = 'host:' + self._req_host.lower(
        ) + '\n' + 'x-sdk-date:' + self.req_date + '\n'

        # Step 5: Create the list of signed headers. This lists the headers
        # in the canonical_headers list, delimited with ";" and in alpha order.
        # Note: The request can include any headers; canonical_headers and
        # signed_headers lists those that you want to be included in the
        # hash of the request. "host" and "x-amz-date" are always required.

        self.signed_headers = 'host;x-sdk-date'

        # Step 6: Create payload hash (hash of the request body content)

        self.payload_hash = hashlib.sha256(
            self._req_body.encode('utf-8')).hexdigest()

        # Step 7: Combine elements to create canonical request
        if self._req_uri.endswith('/'):
            self._req_uri = self._req_uri
        else:
            self._req_uri = self._req_uri + '/'

        self.canonical_request = self._req_method.upper(
        ) + '\n' + self._req_uri + '\n' + self.canonical_querystring + '\n' + self.canonical_headers + '\n' + self.signed_headers + '\n' + self.payload_hash

        # ************* TASK 2: CREATE THE STRING TO SIGN*************
        # Match the algorithm to the hashing algorithm you use,SHA-256 (recommended)
        self.credential_scope = self.req_datestamp + '/' + self.req_region + '/' + self.req_service + '/' + 'sdk_request'
        self.string_to_sign = self.algorithm + '\n' + self.req_date + '\n' + self.credential_scope + '\n' + hashlib.sha256(
            self.canonical_request.encode('utf-8')).hexdigest()

        # ************* TASK 3: CALCULATE THE SIGNATURE *************
        # Create the signing key using the function defined above.
        self.signing_key = self.get_signature_key(
            self._secret_key, self.req_datestamp, self.req_region,
            self.req_service)

        # Sign the string_to_sign using the signing_key
        self.signature = hmac.new(self.signing_key,
                                  (self.string_to_sign).encode('utf-8'),
                                  hashlib.sha256).hexdigest()

        # ************* TASK 4: ADD SIGNING INFORMATION TO THE REQUEST *************
        # The signing information can be either in a query string value or in
        # a header named Authorization. This code shows how to use a header.
        # Create authorization header and add to request headers
        self.authorization_header = self.algorithm + ' ' + 'Credential=' + self._access_key + '/' + self.credential_scope + ', ' + 'SignedHeaders=' + self.signed_headers + ', ' + 'Signature=' + self.signature

        # The request can include any headers, but MUST include "host",
        # "x-sdk-date",# and (for this scenario) "Authorization". "host" and
        # "x-sdk-date" must# be included in the canonical_headers and
        # signed_headers, as noted# earlier. Order here is not significant.#
        # Python note: The 'host' header is added automatically by the Python
        # 'requests' library.
        if self._x_project_id:
            self.headers_base = {
                'X-Project-Id': self._x_project_id,
                'x-sdk-date': self.req_date,
                'Authorization': self.authorization_header
            }
        else:
            self.headers_base = {
                'x-sdk-date': self.req_date,
                'Authorization': self.authorization_header
            }

        self.headers = {**self.headers_base, **self._req_custom_headers}
        if self._req_query_param:
            self.request_url = 'https://' + self._req_host + self._req_uri[:
                                                                           -1] + '?' + self.canonical_querystring
        else:
            self.request_url = 'https://' + self._req_host + self._req_uri[:-1]

        try:
            if self._req_method == 'GET':
                self.respon = requests.get(
                    self.request_url,
                    data=self._req_body,
                    headers=self.headers,
                    timeout=self._req_timeout)
            elif self._req_method == 'POST':
                self.respon = requests.post(
                    self.request_url,
                    data=self._req_body,
                    headers=self.headers,
                    timeout=self._req_timeout)
            elif self._req_method == 'PUT':
                self.respon = requests.put(
                    self.request_url,
                    data=self._req_body,
                    headers=self.headers,
                    timeout=self._req_timeout)
            elif self._req_method == 'DELETE':
                self.respon = requests.delete(
                    self.request_url,
                    data=self._req_body,
                    headers=self.headers,
                    timeout=self._req_timeout)
            elif self._req_method == 'PATCH':
                self.respon = requests.patch(
                    self.request_url,
                    data=self._req_body,
                    headers=self.headers,
                    timeout=self._req_timeout)
            else:
                raise SignError(
                    'request method need one of GET,POST,PUT,DELETE,PATCH')
            return self.respon.json()
        except Exception as error:
            raise error
