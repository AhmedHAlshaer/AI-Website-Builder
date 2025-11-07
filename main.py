import sys
import os
import shutil
from builder.crew import SiteBuilderCrew
from crewai import Agent, LLM, Task, Crew

# Initialize LLM (similar to crew.py)
model_name = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    raise RuntimeError("DEEPSEEK_API_KEY environment variable is not set.")

llm = LLM(model=model_name, api_key=api_key, base_url="https://api.deepseek.com/v1")


def route_user_intent(user_input: str) -> str:
    """
    Uses LLM to determine if user wants NEW or EDIT
    Returns: "NEW" or "EDIT"
    """
    prompt = f"""
    Analyze this user request and determine if they want to:
    A) Create a NEW website
    B) EDIT an existing website

    User request: "{user_input}"

    Reply with only: NEW or EDIT
    """
    
    agent = Agent(
        role="Intent Classifier",
        goal="Determine if user wants NEW or EDIT",
        backstory=prompt,
        llm=llm 
    )
    
    task = Task(
        description=f"Classify this intent: {user_input}",
        agent=agent,
        expected_output="Either NEW or EDIT"
    )
    
    # Create a mini crew to execute this single task
    mini_crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=False
    )
    
    result = mini_crew.kickoff()
    
    # Parse result
    result_str = str(result)
    
    if "EDIT" in result_str.upper():
        return "EDIT"
    else:
        return "NEW"


def collect_multiline_input(prompt_message: str) -> str:
    """
    Helper function to collect multi-line input from user
    """
    print(prompt_message)
    print("(Enter your description, then press Enter twice or Ctrl+D when done)\n")
    
    if not sys.stdin.isatty():
        user_input = sys.stdin.read().strip()
    else:
        lines = []
        try:
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
        except EOFError:
            pass
        user_input = "\n".join(lines).strip()
    
    return user_input


def run_new_website_workflow(user_spec: str):
    """
    Run the workflow for creating a NEW website
    """
    # Validate input length
    if len(user_spec) > 5000:
        print("Error: Description too long (max 5000 characters)")
        sys.exit(1)
    
    # Handle existing website/ directory to ensure idempotency
    output_dir = "website"
    if os.path.exists(output_dir):
        backup_dir = f"{output_dir}_backup"
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
    
    # Output the final result
    print("\n" + "="*60)
    print("🎉 GENERATION COMPLETE")
    print("="*60)
    if result:
        print(result)
    else:
        print("Site generation completed. Your website is ready in the 'website/' directory.")
    print("\n" + "="*60)


def run_edit_website_workflow(edit_spec: str):
    """
    Run the workflow for EDITING an existing website
    TODO: You need to implement this!
    """
    print("\n🔧 EDIT MODE")
    print("="*60)
    print("⚠️  Edit functionality is not yet implemented.")
    print("This is where you would:")
    print("  1. 📖 Analyze the existing website")
    print("  2. 📝 Plan the modifications")
    print("  3. ✏️  Apply the changes")
    print("  4. ✅ Test the updated website")
    print("\nFor now, this feature is coming soon!")
    print("="*60)
    
    # TODO: Create SiteEditorCrew and run it here
    # crew_instance = SiteEditorCrew()
    # result = crew_instance.crew().kickoff(inputs={"edit_request": edit_spec})


def run():
    """Entry point for crewai run command"""
    
    # Step 1: Get initial user input to classify intent
    print("="*60)
    print("🌐 Welcome to the AI Website Builder!")
    print("="*60)
    initial_input = input("\nHi! How can I help you today?\nDo you want to work on a (N)ew website or (E)dit an existing one? ")
    
    # Step 2: Classify the intent
    decision = route_user_intent(initial_input)
    print(f"\n📋 Understood! Mode: {decision}")
    
    # Step 3: Branch based on decision
    if decision == "NEW":
        print("\n" + "="*60)
        print("🆕 NEW WEBSITE MODE")
        print("="*60)
        
        user_spec = collect_multiline_input("Great! Please describe the website you want to build:")
        
        if not user_spec:
            print("No website description provided. Exiting.")
            sys.exit(0)
        
        run_new_website_workflow(user_spec)
    
    elif decision == "EDIT":
        print("\n" + "="*60)
        print("✏️  EDIT WEBSITE MODE")
        print("="*60)
        
        # Check if website exists
        if not os.path.exists("website"):
            print("❌ Error: No existing 'website' directory found.")
            print("Please create a new website first before trying to edit.")
            sys.exit(1)
        
        edit_spec = collect_multiline_input("What changes would you like to make to your existing website?")
        
        if not edit_spec:
            print("No changes specified. Exiting.")
            sys.exit(0)
        
        run_edit_website_workflow(edit_spec)
    
    else:
        print("❌ Could not determine your intent. Please try again.")
        sys.exit(1)


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