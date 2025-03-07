# mondaytoframe

This Python package helps convert data between the Monday.com API and DataFrames.

## Installation

You can install the package using pip:

```bash
pip install mondaytoframe
```

## Usage

Here's a basic example of how to use the package using a token string:

```python
from mondaytoframe import load, save

monday_token = "your_monday_token"

# Load your board to a dataframe... 
df = load("your_board_id", monday_token)

# ... perform data transformation on your dataframe
df_transformed = df.copy()

# ... and store the results in Monday again!
save("you_board_id", df_transformed, monday_token)

```

Alternatively, you can set `MONDAYTOFRAME_TOKEN` environment variable:

```python
from mondaytoframe import load, save

# Load your board to a dataframe... 
df = load("your_board_id")

# ... perform data transformation on your dataframe
df_transformed = df.copy()

# ... and store the results in Monday again!
save("you_board_id", df_transformed)

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
