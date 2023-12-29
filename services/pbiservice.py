from services.aadservice import AadService
import requests

class PbiService:

    def post_data_to_push_dataset_table(self, group_id, dataset_id, table_name, data):
        '''Post data to a table in a push dataset

        Args:
            group_id (str): Group Id
            dataset_id (str): Dataset Id
            table_name (str): Table Name
            data (dict): Data to be posted

        Returns:
            Response Status Code 
        '''
        data_to_post = {
            "rows": data
            } 
        endpoint = f'https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/tables/{table_name}/rows'
        token = AadService.get_access_token()
        header = {"Authorization": "Bearer " + token}
        response = requests.post(endpoint, json=data_to_post, headers=header)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f'Error while pushing data to datasetL\n{response.reason}:\t{response.text}\nRequestId:\t{response.headers.get("RequestId")}\n' + str(e))
        
        return response

    def delete_data_from_push_dataset_table(self, group_id, dataset_id, table_name):
        '''Delete all data from a table in a push dataset

        Args:
            group_id (str): Group Id
            dataset_id (str): Dataset Id
            table_name (str): Table Name

        Returns:
            Response Status Code 
        '''
        endpoint = f'https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/tables/{table_name}/rows'
        token = AadService.get_access_token()
        header = {"Authorization": "Bearer " + token}
        response = requests.delete(endpoint, headers=header)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f'Error while pushing data to datasetL\n{response.reason}:\t{response.text}\nRequestId:\t{response.headers.get("RequestId")}\n' + str(e))
        
        return response
    
    def post_push_dataset_to_group(self, group_id, dataset):
        '''Post new dataset to a group

        Args:
            group_id (str): Group Id
            dataset (dict): Dataset

        Example Dataset: 
            {
            "name": "test_push_dataset",
            "defaultMode": "Push",
            "tables": [
                {
                "name": "Case",
                "columns": [
                    {
                    "name": "Case",
                    "dataType": "string"
                    },
                    {
                    "name": "Subject",
                    "dataType": "string"
                    },
                    {
                    "name": "Date",
                    "dataType": "Datetime"
                    }
                ]
                }
            ]
            }

        Returns:
            Response Status Code 
        '''
        
        endpoint = f'https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets'
        token = AadService.get_access_token()
        header = {"Authorization": "Bearer " + token}
        response = requests.post(endpoint, json=dataset, headers=header)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f'Error while posting dataset\n{response.reason}:\t{response.text}\nRequestId:\t{response.headers.get("RequestId")}\n' + str(e))

        return response
    
    def update_table_in_dataset(self, group_id, dataset_id, table_name, updated_table):
        '''Post new dataset to a group

        Args:
            group_id (str): Group Id
            dataset_id (str): Dataset ID
            table_name (str): Table Name 
            updated_table (dict): Updated Table dict

        Example Table: 
            {
                "name": "Case",
                "columns": [
                    {
                    "name": "Case",
                    "dataType": "string"
                    },
                    {
                    "name": "Subject",
                    "dataType": "string"
                    },
                    {
                    "name": "Date",
                    "dataType": "Datetime"
                    }
                ]
                }

        Returns:
            Response Status Code 
        '''

        token = AadService.get_access_token()
        header = {"Authorization": "Bearer " + token}

        endpoint = f'https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/tables/{table_name}'
        response = requests.put(endpoint, json=updated_table, headers=header)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f'Error while posting dataset\n{response.reason}:\t{response.text}\nRequestId:\t{response.headers.get("RequestId")}\n' + str(e))

        return response
    
    def get_dataset_in_group(self, group_id):
        '''
            Get datasets in group.

            Args: 
                groupid (str): Group ID to search 
        '''
        endpoint = f'https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets'
        header = self.get_request_header()
        response = requests.get(endpoint, headers=header)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f'Error while getting datasets\n{response.reason}:\t{response.text}\nRequestId:\t{response.headers.get("RequestId")}\n' + str(e))
        return response
    
    def get_dataset_in_group_by_id(self, group_id, dataset_id):
        datasets = self.get_dataset_in_group(group_id)
        res_body = datasets.json()
        ds_matches = list(filter(lambda d: d['id'] == dataset_id, res_body['value']))
        if len(ds_matches) > 0:
            ds = ds_matches[0]
        else:
            ds = None

        return ds

    def get_request_header(self):
        '''Get Power BI API request header

        Returns:
            Dict: Request header
        '''

        return {'Authorization': 'Bearer ' + AadService.get_access_token()}