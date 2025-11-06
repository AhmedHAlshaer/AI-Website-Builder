import sys
import os
import shutil
from builder.crew import SiteBuilderCrew


def run():
    """Entry point for crewai run command"""
    # Prompt the user for a website description
    print("Hi, how can I help you today? What website do you want me to build for you today?")
    print("(Enter your description, then press Enter twice or Ctrl+D when done)\n")
    
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
    
    # Validate input length
    if len(user_spec) > 5000:
        print("Error: Description too long (max 5000 characters)")
        sys.exit(1)
    
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
    print("\n🚀 Starting website generation...")
    print("📋 This may take a few minutes. The crew will:")
    print("   1. 📝 Plan the project")
    print("   2. 🎨 Build the frontend")
    print("   3. ⚙️  Build the backend (if needed)")
    print("   4. 🔗 Integrate all components")
    print("   5. ✅ Test the final website")
    print("\nPlease wait...\n")
    
    crew_instance = SiteBuilderCrew()
    try:
        result = crew_instance.crew().kickoff(inputs={"customer_request": user_spec})
    except Exception as e:
        print("\n❌ An error occurred during site generation:")
        print(e)
        sys.exit(1)
    
    # Output the final result or summary
    print("\n" + "="*60)
    print("🎉 GENERATION COMPLETE")
    print("="*60)
    if result:
        print(result)
    else:
        print("Site generation completed. Your website is ready in the 'website/' directory.")
    print("\n" + "="*60)


def train():
    """Train the crew (if training features are implemented)"""
    print("Training not yet implemented")
    pass


def replay():
    """Replay the crew execution (if replay features are implemented)"""
    print("Replay not yet implemented")
    pass


def test():
    """Test the crew (if test features are implemented)"""
    print("Testing not yet implemented")
    pass


if __name__ == "__main__":
    run()