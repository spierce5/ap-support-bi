# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

import msal
import os
from dotenv import load_dotenv

class AadService:

    def get_access_token():
        '''Generates and returns Access token

        Returns:
            string: Access token
        '''
        load_dotenv()
        response = None
        try:
            # Service Principal auth is the recommended by Microsoft to achieve App Owns Data Power BI embedding
            if os.environ['AUTHENTICATION_MODE'].lower() == 'serviceprincipal':
                authority = os.environ['AUTHORITY_URL'].replace('organizations', os.environ['TENANT_ID'])
                clientapp = msal.ConfidentialClientApplication(os.environ['CLIENT_ID'], client_credential=os.environ['CLIENT_SECRET'], authority=authority)

                # Make a client call if Access token is not available in cache
                scope_list = [os.environ['SCOPE_BASE']]
                response = clientapp.acquire_token_for_client(scopes=scope_list)

            try:
                return response['access_token']
            except KeyError:
                raise Exception(response['error_description'])

        except Exception as ex:
            raise Exception('Error retrieving Access token\n' + str(ex))