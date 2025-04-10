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
from mondaytoframe import create_board, create_items, read, update
import pandas as pd
import os

monday_token = "your_monday_token_here"

# Create a new board
columns = {"Numbers Column": "numbers", "Text Column": "text"}
board_id = create_board(columns, monday_token)

# Create items in a board
new_df = pd.DataFrame(
    {
        "Name": ["first", "second"],
        "Numbers Column": [1.0, 2.0],
        "Text Column": ["a", "b"],
    }
)
create_items(board_id, new_df, monday_token)

# Read your board as a dataframe...
df = read(board_id, monday_token)

# ... perform data transformation on your dataframe
df_transformed = df.copy()
df_transformed["Numbers Column"] = df["Numbers Column"] + 1

# ... and store the results in Monday again!
update(board_id, df_transformed, monday_token)

```

> [!TIP]
> Instead of providing `monday_token`, you could also set `MONDAYTOFRAME_TOKEN` environment variable.

## Features

- Easy conversion between Monday.com API data and DataFrames
- Simplifies data manipulation and analysis
- Support for multiple [monday column types](https://developer.monday.com/api-reference/reference/column-types-reference)

### Supported Data Types

| Column Type            | Supported by `read` | Supported by `update` |
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
