import os
import json

def load_mcp_config(*server_names):
    config_path = os.path.join(os.path.dirname(__file__),'mcp_config.json')

    with open(config_path,'r') as f:
        all_configs = json.load(f)

    if len(server_names) == 0:
        return all_configs
    
    selected_configs={}

    for i in server_names:
        if i in all_configs:
            selected_configs[i] = all_configs[i]

    return selected_configs


if __name__ == '__main__':
    print(load_mcp_config('google-sheets','yahoo-finance'))


