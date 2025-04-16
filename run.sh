# Save this as run.sh
#!/bin/bash

# Activate virtual environment
source llm_env/bin/activate

# Display menu
echo "========================================"
echo "      Academic LLM Assistant Launcher   "
echo "========================================"
echo "1. Test Basic Model"
echo "2. Run Academic Assistant"
echo "3. Exit"
echo "========================================"

# Get user choice
read -p "Enter your choice (1-3): " choice

case $choice in
    1)
        echo "Launching Basic Test Interface..."
        python test_model.py
        ;;
    2)
        echo "Launching Academic Assistant..."
        python academic_assistant.py
        ;;
    3)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
