class XMLRPCClient:
    def __init__(self, host, port):
        self.url = f"http://{host}:{port}/skills/xmlrpc"
    
    def call(self, method_name, params=None):
        import xmlrpc.client
        with xmlrpc.client.ServerProxy(self.url) as proxy:
            if params is None:
                return getattr(proxy, method_name)()
            else:
                return getattr(proxy, method_name)(*params)

    def get_box_metadata(self):
        return self.call("get_box_metadata")

    def get_trained_skills(self):
        return self.call("get_trained_skills")

    def execute_skill(self, skill_id):
        return self.call("execute_skill", [skill_id])

    def get_result(self, skill_id):
        return self.call("get_result", [skill_id])

    def get_last_endstate_values(self, skill_id):
        return self.call("get_last_endstate_values", [skill_id])