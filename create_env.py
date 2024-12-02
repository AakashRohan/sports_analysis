import os

def create_env_file():
    try:
        api_key = input("Please enter your API key: ").strip()
        
        if not api_key:
            print("API key cannot be empty. Please try again.")
            return
        
        with open('.env', 'w') as f:
            f.write(f'ODDS_API_KEY={api_key}\n')
        
        print("Environment file created successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_env_file() 