import pandas as pd


def setup_dataframe():
    """
    This code performs the following steps:

    1. Splitting the technologies listed in the "technologies" column into separate entries and converting them into a list of lists.

    2. Creating a new column called "all_technologies" containing a list of technologies for each record.

    3. Exploding the list of technologies in the new "all_technologies" column, i.e., converting each list of technologies into separate rows.

    4. Creating a new DataFrame based on the cross-tabulation, which counts the occurrences of each technology and joining it with the original DataFrame.

    5. Dropping the "all_technologies" and "technologies" columns as they are no longer needed.

    6. Converting the "posted_date" column to datetime format.

    7. Displaying the first few rows of the DataFrame.
    """
    df = pd.read_csv("../technologies.csv")

    technologies = df["technologies"].str.split(",").values.tolist()

    df["all_technologies"] = technologies

    all_technologies = df["all_technologies"].explode()

    df = df.join(
       pd.crosstab(
           all_technologies.index, all_technologies
       )
    )

    df = df.drop(columns=["all_technologies", "technologies"])

    df["posted_date"] = pd.to_datetime(df["posted_date"])

    return df


if __name__ == "__main__":
    d_f = setup_dataframe()
