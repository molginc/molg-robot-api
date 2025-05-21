import argparse
import xmlrpc.client

from typing import Any, Dict, List
import requests

MIRAI_BOX = "172.16.22.56"
SKILL_API_PORT = 6543
SKILL_URL = f"http://{MIRAI_BOX}:{SKILL_API_PORT}/skills/"

class HTTPClient:

    @staticmethod
    def get_box_metadata() -> List[Dict[str, Any]]:
        r = requests.get(SKILL_URL + "get_box_metadata")
        return r.json()

    @staticmethod
    def get_trained_skills() -> List[Dict[str, Any]]:
        r = requests.get(SKILL_URL + "get_trained_skills")
        return r.json()

    @staticmethod
    def prepare_skill_async(skill_id) -> List[Dict[str, Any]]:
        r = requests.post(SKILL_URL + "prepare_skill_async", json={"skill_id": skill_id})
        return r.json()

    @staticmethod
    def execute_skill(skill_id) -> List[Dict[str, Any]]:
        r = requests.post(SKILL_URL + "execute_skill", json={"skill_id": skill_id})
        return r.json()

    # Example call

    # POST SKILL_URL/get_last_endstate_values params={“skill_id”: 15}



    # Example response

    # Returns {'status': 'success', 'data': [0.000667944479889174, 0.0, 0.00194020033814013, -1.0107421875, 0.04916917532682419, 4.916917532682419e-05]}

    

    # Meaning of each number

    #     - item 0 contains tcp speed info

    #     - item 1 contains force encountered info

    #     - item 2 contains the visual done probability

    #     - item 3 contains the anomaly score

    #     - item 4 contains an approximate upper bound on the cartesian

    #                       distance to the target pose, in cm

    #     - item 5 contains an approximate upper bound on the rotational

    #                       distance to the target pose, in degrees
    # after execution of the skill this will return the type of endstate
    @staticmethod
    def get_result(skill_id) -> List[Dict[str, Any]]:
        r = requests.post(SKILL_URL + "get_result", json={"skill_id": skill_id})
        return r.json()


    # after execution of the skill this will return the last endstate values
    @staticmethod
    def get_last_endstate_values(skill_id) -> List[Dict[str, Any]]:
        r = requests.post(SKILL_URL + "get_last_endstate_values", json={"skill_id": skill_id})
        return r.json()  


class XMLRPCClient:
    def __init__(self, host):
        self.server = xmlrpc.client.ServerProxy(f'http://{host}:6543/skills/xmlrpc')

    def get_box_metadata(self):
        return self.server.get_box_metadata()

    def get_trained_skills(self):
        return self.server.get_trained_skills()

    def execute_skill(self, skill_id):
        return self.server.execute_skill(skill_id)

    def get_result(self, skill_id):
        return self.server.get_result(skill_id)

    def get_last_endstate_values(self, skill_id):
        return self.server.get_last_endstate_values(skill_id)

def main():
    parser = argparse.ArgumentParser(description='XMLRPC Skill CLI')
    # parser.add_argument('--host', type=str, required=True, help='Host address of the XMLRPC server')
    parser.add_argument('command', type=str, choices=['get_box_metadata', 'get_trained_skills', 'execute_skill', 'get_result', 'get_last_endstate_values'], help='Command to execute')
    parser.add_argument('--skill_id', type=int, help='Skill ID for execute_skill, get_result, and get_last_endstate_values commands')

    args = parser.parse_args()

    # client = XMLRPCClient(args.host)
    client = HTTPClient()

    if args.command == 'get_box_metadata':
        print(client.get_box_metadata())
    elif args.command == 'get_trained_skills':
        print(client.get_trained_skills())
    elif args.command == 'prepare_skill_async':
        if args.skill_id is None:
            print("Skill ID is required for prepare_skill_async command.")
        else:
            print(client.prepare_skill_async(args.skill_id))
    elif args.command == 'execute_skill':
        if args.skill_id is None:
            print("Skill ID is required for execute_skill command.")
        else:
            print(client.execute_skill(args.skill_id))
    elif args.command == 'get_result':
        if args.skill_id is None:
            print("Skill ID is required for get_result command.")
        else:
            print(client.get_result(args.skill_id))
    elif args.command == 'get_last_endstate_values':
        if args.skill_id is None:
            print("Skill ID is required for get_last_endstate_values command.")
        else:
            print(client.get_last_endstate_values(args.skill_id))

if __name__ == '__main__':
    main()