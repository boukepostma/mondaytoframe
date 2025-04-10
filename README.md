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
from mondaytoframe import read, save

monday_token = "your_monday_token"

# Read your board as a dataframe... 
df = read("your_board_id", monday_token)

# ... perform data transformation on your dataframe
df_transformed = df.copy()

# ... and store the results in Monday again!
save("you_board_id", df_transformed, monday_token)

```

Alternatively, you can set `MONDAYTOFRAME_TOKEN` environment variable:

```python
from mondaytoframe import read, save

# Read your board as a dataframe... 
df = read("your_board_id")

# ... perform data transformation on your dataframe
df_transformed = df.copy()

# ... and store the results in Monday again!
save("you_board_id", df_transformed)

```


## Features

- Easy conversion between Monday.com API data and DataFrames
- Simplifies data manipulation and analysis
- Support for multiple [monday column types](https://developer.monday.com/api-reference/reference/column-types-reference)

### Supported Data Types

| Column Type            | Supported by `read` | Supported by `save` |
|------------------------|---------------------|---------------------|
| Item ID                | ✅                  | ✅                  |
| Name                   | ✅                  | ✅                  |
| Text                   | ✅                  | ✅                  |
| Long Text              | ✅                  | ✅                  |
| Number                 | ✅                  | ✅                  |
| Date                   | ✅                  | ✅                  |
| Status                 | ✅                  | ✅                  |
| Dropdown               | ✅                  | ✅                  |
| People                 | ✅                  | ✅                  |
| Tags                   | ✅                  | ✅                  |
| Checkbox               | ✅                  | ✅                  |
| Link                   | ✅                  | ✅                  |
| Email                  | ✅                  | ✅                  |
| Phone                  | ✅                  | ✅                  |
| Timeline               | ❌                  | ❌                  |
| Country                | ❌                  | ❌                  |
| Color Picker           | ❌                  | ❌                  |
| Rating                 | ❌                  | ❌                  |
| Progress Tracking      | ❌                  | ❌                  |
| Formula                | ❌                  | ❌                  |
| Auto Number            | ❌                  | ❌                  |
| Dependency             | ❌                  | ❌                  |
| Button                 | ❌                  | ❌                  |
| World Clock            | ❌                  | ❌                  |
| Location               | ❌                  | ❌                  |
| Hour                   | ❌                  | ❌                  |
| Week                   | ❌                  | ❌                  |
| File                   | ❌                  | ❌                  |
| Board Relation         | ❌                  | ❌                  |
| Mirror                 | ❌                  | ❌                  |
| Vote                   | ❌                  | ❌                  |
| Subitems               | ❌                  | ❌                  |


## Contributing

Contributions are welcome! Please read the [contributing guidelines](CONTRIBUTING.md) first.

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please open an issue.
