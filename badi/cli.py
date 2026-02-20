"""
Command Line Interface for B.A.D.I.

Provides interactive chat and setup commands.
"""

import asyncio
import click
from pathlib import Path

from badi.config import get_config
from badi.memory import init_db, get_db, get_or_create_user, save_interaction
from badi.core.router import Request, route_request


@click.group()
def cli():
    """B.A.D.I. - Balanced Autonomous Digital Intelligence"""
    pass


@cli.command()
def setup():
    """Run initial setup wizard"""
    click.echo("🤖 B.A.D.I. Setup Wizard\n")
    
    # Initialize database
    click.echo("Initializing database...")
    init_db()
    click.echo("✓ Database initialized\n")
    
    # Create default user
    db = get_db()
    name = click.prompt("Your name", default="User")
    user = get_or_create_user(db, name=name)
    click.echo(f"✓ User created: {user.name}\n")
    
    # Check configuration
    config = get_config()
    click.echo("Configuration:")
    click.echo(f"  Mode: {config.mode}")
    click.echo(f"  Database: {config.db_path}")
    
    # Check AI backends
    from badi.ai_backends import get_selector
    selector = get_selector()
    backends = selector.list_available_backends()
    
    click.echo("\nAvailable AI Backends:")
    for name, available in backends.items():
        status = "✓" if available else "✗"
        click.echo(f"  {status} {name}")
    
    if not any(backends.values()):
        click.echo("\n⚠️  No AI backends configured!")
        click.echo("Please set up at least one backend:")
        click.echo("  - Local: Download GGUF model and set BADI_LOCAL_MODEL_PATH")
        click.echo("  - Cloud: Set API key (OPENAI_API_KEY, ANTHROPIC_API_KEY, or GEMINI_API_KEY)")
    
    click.echo("\n✓ Setup complete! Run 'python -m badi.cli chat' to start chatting.")


@cli.command()
def chat():
    """Start interactive chat session"""
    asyncio.run(chat_session())


async def chat_session():
    """Run interactive chat session"""
    click.echo("🤖 B.A.D.I. Chat (type 'exit' or 'quit' to end)\n")
    
    # Get or create user
    db = get_db()
    user = get_or_create_user(db, name="CLI User")
    
    while True:
        try:
            # Get user input
            user_input = click.prompt("\nYou", prompt_suffix=": ")
            
            if user_input.lower() in ["exit", "quit", "q"]:
                click.echo("Goodbye! 👋")
                break
            
            # Save user message
            save_interaction(db, user.id, "user", user_input)
            
            # Create request
            request = Request(text=user_input, user_id=user.id)
            
            # Route and get response
            click.echo("\n🤖 B.A.D.I.: ", nl=False)
            response = await route_request(request)
            click.echo(response.text)
            
            # Save assistant response
            save_interaction(db, user.id, "assistant", response.text)
            
        except (KeyboardInterrupt, EOFError):
            click.echo("\n\nGoodbye! 👋")
            break
        except Exception as e:
            click.echo(f"\n❌ Error: {e}")


@cli.command()
def info():
    """Show system information"""
    from badi import __version__
    from badi.modules.base import MODULE_REGISTRY
    
    click.echo(f"B.A.D.I. v{__version__}\n")
    
    config = get_config()
    click.echo(f"Mode: {config.mode}")
    click.echo(f"Database: {config.db_path}")
    click.echo(f"Vector Store: {config.vector_dir}\n")
    
    # List modules
    modules = MODULE_REGISTRY.list_enabled_modules()
    click.echo(f"Enabled Modules ({len(modules)}):")
    for name in modules:
        module = MODULE_REGISTRY.get(name)
        click.echo(f"  - {name}: {module.description}")


if __name__ == "__main__":
    cli()
