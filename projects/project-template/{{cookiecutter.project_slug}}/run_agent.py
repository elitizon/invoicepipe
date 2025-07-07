#!/usr/bin/env python3
"""
{{cookiecutter.project_name}} Runner

This script provides a simple way to run the FastAPI application.
It serves as an entry point for development and testing purposes.
"""

import uvicorn
from {{cookiecutter.package_name}}.config import settings


def main() -> None:
    """Run the FastAPI application with uvicorn."""
    print(f"Starting {settings.app_name}...")
    print(f"Version: {settings.version}")
    print(f"Server will be available at http://{settings.host}:{settings.port}")
    
    uvicorn.run(
        "{{cookiecutter.package_name}}.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )


if __name__ == "__main__":
    main()
    # Check for Application Default Credentials or Service Account
    adc = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    gcloud_adc = os.path.exists(os.path.expanduser("~/.config/gcloud/application_default_credentials.json"))
    if not adc and not gcloud_adc:
        print("\n❌ Google Cloud authentication not found!\n")
        print("To use Vertex AI, you must authenticate with Google Cloud:")
        print("- For development: run 'gcloud auth application-default login'")
        print("- For production: set GOOGLE_APPLICATION_CREDENTIALS to your service account key JSON file\n")
        print("See the README for more details. Exiting.")
        sys.exit(1)


# Constants
APP_NAME = "{{cookiecutter.project_name}}"
USER_ID = "demo_user"
SESSION_ID = "demo_session"


async def main() -> None:
    """Main entry point for the agent runner."""

    # Check for required config and authentication
    try:
        Config.validate()
    except Exception as e:
        print(f"\n❌ Configuration error: {e}\n")
        print("Please check your .env file and environment variables.")
        sys.exit(1)
    check_gcp_auth()

    print("🌤️  {{cookiecutter.project_name}} with Real Weather Data")
    print("=" * 50)

    # Initialize session service
    session_service = InMemorySessionService()

    # Create a session
    session = await session_service.create_session(
        app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
    )

    # Create runner
    runner = Runner(
        agent=root_agent, app_name=APP_NAME, session_service=session_service
    )

    print(f"Session created: {session.id}")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    # Interactive conversation loop
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()

            # Check for exit commands
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Goodbye! 👋")
                break

            if not user_input:
                continue

            # Create message content
            content = types.Content(role="user", parts=[types.Part(text=user_input)])

            print("Agent: ", end="", flush=True)

            # Run the agent and stream response
            async for event in runner.run_async(
                user_id=USER_ID, session_id=session.id, new_message=content
            ):
                if event.is_final_response() and event.content:
                    for part in event.content.parts:
                        if part.text:
                            print(part.text)
                            break
            print()  # New line after response

        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {e}")
            continue


if __name__ == "__main__":
    asyncio.run(main())
