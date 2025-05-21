# XMLRPC Skill CLI

This project provides a command line interface (CLI) for interacting with the XMLRPC skill API. It allows users to execute skills, retrieve metadata, and check results through a simple command line interface.

## Project Structure

```
xmlrpc-skill-cli
├── src
│   ├── cli.py               # Entry point for the command line interface
│   ├── xmlrpc_client.py     # XMLRPC client implementation
│   └── utils
│       └── __init__.py      # Utility functions and constants
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```

## Installation

To get started, clone the repository and install the required dependencies:

```bash
git clone <repository-url>
cd xmlrpc-skill-cli
pip install -r requirements.txt
```

## Usage

To run the command line interface, execute the following command:

```bash
python src/cli.py
```

## Commands

The CLI supports the following commands:

- `get_box_metadata`: Retrieve metadata for the box.
- `get_trained_skills`: List all available skills.
- `execute_skill <skill_id>`: Execute a skill by its ID.
- `get_result <skill_id>`: Get the result of a skill execution.
- `get_last_endstate_values <skill_id>`: Retrieve the last endstate values for a skill.

## Examples

1. Get box metadata:
   ```bash
   python src/cli.py get_box_metadata
   ```

2. List trained skills:
   ```bash
   python src/cli.py get_trained_skills
   ```

3. Execute a skill:
   ```bash
   python src/cli.py execute_skill 1
   ```

4. Get the result of a skill execution:
   ```bash
   python src/cli.py get_result 1
   ```

5. Get last endstate values:
   ```bash
   python src/cli.py get_last_endstate_values 1
   ```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.