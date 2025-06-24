# cpg-radar-data-updated_code

## Used Pandas for Data Processing
I replaced manual row-level processing with Pandas-based operations.

 used pandas.read_csv() to load the movie data.

Grouped the data by year to compute the average IMDb rating per year using groupby().

## Structured Code with Functions
Modularized the script into clear, reusable functions such as:

load_data(), compute_yearly_average(), build_movie_entry(), process_movies(), and validate_output().

I created a main() function to organize the overall workflow.

## Added Robust Error Handling
Wrapped all JSON file reading in except blocks to catch:

Missing files

Invalid JSON formats

Added clear error messages for debugging.

## Used Consistent and Correct Naming
Renamed variables and functions for better clarity and consistency.

Preserved necessary typos like 'writters.json' and 'imbd_votes' only for compatibility with the given input/output files.

Used names such as genre_map, year_avg_map, and valid_writers.

### Avoided Hardcoding with Constants
Defined all filenames and "magic values" at the top of the script using constants:

MOVIES_FILE, GENRE_FILE, WRITERS_FILE, DESIRED_OUTPUT_FILE, and OUTPUT_FILE

## Followed Code Style Best Practices
Ensured PEP8-compliant formatting and indentation.

## Validated and Tested the Output
Added a validate_output() function that compares the generated output with the expected output (desired_output.json).

## Leveraged Pandas for Specific Tasks
Used Pandas to calculate:

Year-wise average IMDb ratings.

New computed columns like rating_percentage, popularity_score, and duration_hours.

Used Pandas row access with .iterrows() for complex row transformations.

Ensured all operations involving structured data use Pandas DataFrames.

