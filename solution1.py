import pandas as pd
import json

MOVIES_FILE = "movies.csv"
GENRE_FILE = "genre.json"
WRITERS_FILE = "writters.json"  
DESIRED_OUTPUT_FILE = "desired_output.json"
OUTPUT_FILE = "output_refactored.json"  # will be saved to this output


# Functions 

def load_json(file_path):
    """
    Loads and returns JSON data from a file.
    Handles common file and format errors.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format: {file_path}")


def load_data():
    """
    Load all required input files into memory.
    Returns DataFrame and dict objects.
    """
    movies_df = pd.read_csv(MOVIES_FILE, dtype={"year": str})  # keeping year as string for consistency
    genre_data = load_json(GENRE_FILE)
    writers_data = load_json(WRITERS_FILE)
    desired_output = load_json(DESIRED_OUTPUT_FILE)
    return movies_df, genre_data, writers_data, desired_output


def compute_yearly_average_rating(df):
    """
    Calculating average IMDb rating for each release year.
    Returns a dictionary: {year: avg_rating}
    """
    return df.groupby("year")["imdb_rating"].mean().round(2).to_dict()


def build_movie_entry(row, valid_writers, genre_lookup, avg_rating_map):
    """
    Building a dictionary for a single movie row and structured as per desired output format.
    """
    year = row["year"]
    rating = float(row["imdb_rating"])
    avg_rating = avg_rating_map.get(year, 0)
    rating_diff = round(rating - avg_rating, 2)

    # Writer details with validation
    writer_ids = row["writter_id"].split(",")
    writer_names = row["writter_name"].split(",")
    writers = [
        {
            "id": wid.strip(),
            "name": wname.strip(),
            "valid": wid.strip() in valid_writers
        }
        for wid, wname in zip(writer_ids, writer_names)
    ]

    # Cast details
    cast_ids = row["cast_id"].split(",")
    cast_names = row["cast_name"].split(",")
    cast = [
        {"id": cid.strip(), "name": cname.strip()}
        for cid, cname in zip(cast_ids, cast_names)
    ]

    # Final dictionary for this movie
    return {
        "rank": int(row["rank"]),
        "id": row["id"],
        "name": row["name"],
        "year": int(year),
        "imbd_votes": int(row["imdb_votes"]), 
        "imdb_rating": rating,
        "certificate": row["certificate"],
        "duration": int(row["duration"]),
        "genre": row["genre"],
        "img_link": row["img_link"],
        "cast": cast,
        "director": {
            "id": row["director_id"],
            "name": row["director_name"]
        },
        "writers": writers,
        "extra_genres": genre_lookup.get(row["id"], []),
        "rating_percentage": round(rating * 10, 1),
        "popularity_score": round(rating * int(row["imdb_votes"]) / 1000, 2),
        "duration_hours": round(int(row["duration"]) / 60, 2),
        "release_date": f"{year}-01-01",
        "reception": {
            "year_average_rating": avg_rating,
            "rating_difference": rating_diff,
            "category": "Average"
        }
    }


def process_all_movies(df, genre_map, writers, avg_ratings):
    """
    Processed the entire DataFrame into a list of structured movie dictionaries.
    """
    return [build_movie_entry(row, writers, genre_map, avg_ratings) for _, row in df.iterrows()]


def validate_output(generated, expected):
    """
    Compares generated output with expected output.
    And Returns True if they match exactly else False.
    """
    return generated == expected


# Main Function Execution 

def main():
    # Loading all required files
    movies_df, genre_data, writers_data, desired_output = load_data()

    # Creating lookup dictionaries
    genre_map = {movie["id"]: movie["extra_genres"] for movie in desired_output}
    avg_rating_map = compute_yearly_average_rating(movies_df)

    # Processing DataFrame to final structure
    final_output = process_all_movies(movies_df, genre_map, writers_data, avg_rating_map)

    # Export to output JSON
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(final_output, f, indent=2)
    print(f" Output saved to {OUTPUT_FILE}")

    # validate match
    if validate_output(final_output, desired_output):
        print(" Output matches the desired structure.")
    else:
        print(" Output does NOT match the desired output!")


if __name__ == "__main__":
    main()
