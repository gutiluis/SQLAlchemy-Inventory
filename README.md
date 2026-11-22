# Inventory Management

A Python console application for managing store inventory using SQLAlchemy ORM and SQLite.

## Overview

The application imports product data from a CSV file, stores records in a SQLite database, and allows users to manage inventory through a console menu.

## Features

- Import and clean inventory data from CSV.
- Store products using SQLAlchemy ORM.
- View product details by ID.
- Add new products.
- Convert product prices into cents.
- Export database records to a CSV backup.

## Technologies

- Python
- SQLAlchemy
- SQLite
- CSV and File I/O

## Installation

Install the dependencies:

```bash
pip install sqlalchemy
```

Run the application:

```bash
python app.py
```

## Usage

Choose an option from the console menu:

| Option | Description             |
| ------ | ----------------------- |
| `V`    | View a product by ID    |
| `A`    | Add a new product       |
| `B`    | Export inventory to CSV |

## Data Model

The `Product` model contains:

- `product_id` – Automatically generated primary key.
- `product_name` – Product name.
- `product_quantity` – Available quantity.
- `product_price` – Price stored in cents.
- `date_updated` – Last update date.

## Input and Output

- **Input:** `inventory.csv`
- **Database:** SQLite
- **Output:** CSV inventory backup

---

### to run the flask rest api

```
python3 flask_rest_api.py
```

---

## Contributing

If you are interested in reporting/fixing issues and contributing directly to the code base, please see [CONTRIBUTING.md](https://github.com/gutiluis/.github/blob/main/CONTRIBUTING.md) for more information on what we're looking for and how to get started.

---

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](https://github.com/gutiluis/.github/blob/main/CODE_OF_CONDUCT.md).

---

## Security Policy

If you discover a security vulnerability, please review our [Security Policy](https://github.com/gutiluis/.github/blob/main/SECURITY.md) for reporting guidelines.

---

## Support

If you run into any issues or have questions, please check our [SUPPORT.md](https://github.com/gutiluis/.github/blob/main/SUPPORT.md) file for guidance, or reach out through one of our community channels below.

---

## Community

Info on reporting bugs, getting help, finding third-party tools and sample apps, and more can be found on our **Community** channels:

- **Slack Workspace:** [technobool.slack.com](https://technobool.slack.com)
- **GitHub Discussions:** [Open a discussion](https://github.com/gutiluis/SQLAlchemy-Inventory/discussions)

---

## License

[MIT LICENSE](LICENSE)
