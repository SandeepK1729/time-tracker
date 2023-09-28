# time-tracker
It is task managing application, that is used to CRUD on tasks


## Installation

To run the Transaction Manager application locally, follow these steps:

1. Clone the repository:

   ```shell
   git clone https://github.com/SandeepK1729/time-tracker.git
   cd time-tracker
   ```

1. Create a virtual environment:

   ```shell
   python3 -m venv env
   source env/bin/activate
   ```

1. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

1. Set up environmental variables

    ```shell
    echo "SECRET_KEY=<secret_key>" > time_tracker/.env
    echo "DEBUG=True" > time_tracker/.env
    echo "DATABASE_TYPE=local" > time_tracker/.env
    ```

1. Set up the database:

   ```shell
   python manage.py migrate
   ```

1. Create a superuser (admin account):

   ```shell
   python manage.py createsuperuser
   ```

1. Start the development server:

   ```shell
   python manage.py runserver
   ```

1. Access the application by visiting `http://localhost:8000` in your web browser.

## Contributing

Contributions are welcome! If you'd like to contribute to the Transaction Manager project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive messages.
4. Push your changes to your forked repository.
5. Submit a pull request explaining your changes.

Please ensure that your code adheres to the existing coding style and includes relevant tests.

## License

The Transaction Manager application is open-source software licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute it as per the terms of the license.

## Contact

If you have any questions, suggestions, or issues, please contact the project maintainer at [sandeepkumargalipelly@gmail.com](mailto:sandeepkumargalipelly@gmail.com).
