# Basic usage with default prompt file
python singleshot_prompt.py

# Custom prompt file
python singleshot_prompt.py ticket_analysis.txt

# Run only Claude with custom output directory
python singleshot_prompt.py support_ticket.txt --claude-only --output-dir results

# Run without streaming and thinking
python singleshot_prompt.py --no-streaming --no-thinking

# Help
python singleshot_prompt.py --help
