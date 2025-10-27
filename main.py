import os, argparse
from dotenv import load_dotenv
import uvicorn
from utilities.tools import parse_boolean

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the server in different modes.")
    # 將 parser.add_argument 的部分，分成不同的 group
    app_mode = parser.add_argument_group(title="App Mode", description="Run the server in different modes.")
    app_mode.add_argument("--prod", action="store_true", help="Run the server in production mode.")
    app_mode.add_argument("--test", action="store_true", help="Run the server in test mode.")
    app_mode.add_argument("--dev", action="store_true", help="Run the server in development mode.")
 
    # Read settings and parsing to environment variables...
    args = parser.parse_args()
    if args.prod:
        load_dotenv("setting/.env.prod")
    elif args.test:
        load_dotenv("setting/.env.test")
    else:
        load_dotenv("setting/.env.dev") # default

    app_name: str = "api_runner:app"
    host_name: str = "0.0.0.0"
    port_num: int = int(os.getenv("PORT")) 
    if_reload: bool = parse_boolean(os.getenv("RELOAD"))
    
    print(f"Uvicron starting:(app_name={app_name}, host_name={host_name}, port_num={port_num}, if_reload={if_reload})...")
    uvicorn.run(app_name, host=host_name, port=port_num, reload=if_reload)