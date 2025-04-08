import boto3
import requests

def manage_7dtd_server(method: str) -> str:
    def execute_lambda():
        command = method.lower()
        url = f'https://3fjerz7vlsfbjylpikx42cjpau0sjghz.lambda-url.us-east-2.on.aws/?command={command}'
        requests
    
    result: str = ''
    if method == 'Start':
        # TODO - Fill in with start code
        method = 'Server is now online. Please wait up to 5 mins for services to warm up'
    elif method == 'End':
        # TODO - Fill in with end code
        method = 'Server is now offline. Thank you for playing!'


if __name__ == '__main__':
    print('\n\nTesting AWS')
