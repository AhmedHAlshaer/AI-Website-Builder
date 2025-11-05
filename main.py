import sys, os, shutil
from crew import SiteBuilderCrew

if __name__ == "__main__":
    # Prompt the user for a website description
    print("Hi, how can I help you today? What website do you want me to build for you today?")
    # Read multi-line input from user (interactive or piped)
    if not sys.stdin.isatty():
        # If input is piped in or redirected, read all at once
        user_spec = sys.stdin.read().strip()
    else:
        # Otherwise, read from stdin until an empty line or EOF
        lines = []
        try:
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
        except EOFError:
            pass
        user_spec = "\n".join(lines).strip()
    # If no input provided, exit
    if not user_spec:
        print("No website description provided. Exiting.")
        sys.exit(0)
    # Handle existing website/ directory to ensure idempotency
    output_dir = "website"
    if os.path.exists(output_dir):
        backup_dir = f"{output_dir}_backup"
        # If backup directory exists from a previous run, add timestamp to make unique
        if os.path.exists(backup_dir):
            import datetime
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_dir = f"{output_dir}_{ts}"
        try:
            os.rename(output_dir, backup_dir)
            print(f"Note: Existing '{output_dir}' directory was renamed to '{backup_dir}'.")
        except Exception as e:
            print(f"Warning: Could not rename existing '{output_dir}' directory: {e}")
            try:
                shutil.rmtree(output_dir)
                print(f"Note: Existing '{output_dir}' directory was removed.")
            except Exception as e2:
                print(f"Error: Please remove or rename the existing '{output_dir}' directory and run again.")
                sys.exit(1)
    # Instantiate the Crew and run the generation process
    crew_instance = SiteBuilderCrew()
    try:
        result = crew_instance.crew().kickoff(inputs={"customer_request": user_spec})
    except Exception as e:
        print("An error occurred during site generation:")
        print(e)
        sys.exit(1)
    # Output the final result or summary
    if result:
        print(result)
    else:
        print("Site generation completed. Your website is ready in the 'website/' directory.")
