# mondaytoframe

This Python package helps convert data between the Monday.com API and DataFrames.

## Installation

You can install the package using pip:

```bash
pip install mondaytoframe
```

## Usage

Here's a basic example of how to use the package:

```python
from mondaytoframe.io import load, save
from monday import MondayClient

# Create a Monday client using your Monday API token
monday_token = "your_monday_token"

# Now you can use the client with mondaytoframe functions
df = load(monday_token, "your_board_id")

# ... perform data transformation on your dataframe
df_transformed = df.copy()

# ... and store the results in Monday again!
save(monday_token, "you_board_id", df_transformed)

```

## Features

- Easy conversion between Monday.com API data and DataFrames
- Simplifies data manipulation and analysis

## Contributing

Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) first.

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please open an issue.
