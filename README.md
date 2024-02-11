# sqlacodegen-model-split
Contraption for create splited models generated by sqlacodegen 

# How use?
1. Download and install [sqlacodegen](https://github.com/agronholm/sqlacodegen/)
2. Run cmd `sqlacodegen mysql+oursql://user:password@localhost/dbname --outfile output-sqlacodegen.py`
3. Check variables `model_folder_name` and `unique_model_file` in `main.py`, change if necessary
4. Run `main.py`

📌 Note that it is not a professional solution, just a shortcut to cover the lack of the feature in the [sqlacodegen](https://github.com/agronholm/sqlacodegen/)
📌 Recommended that you check the generated models to avoid problems.
