import matplotlib.pyplot as plt
from setup_dataframe import setup_dataframe


def plot_graph(df):
    """
    This code creates a bar chart
    showing the top 10 most popular vacancies,
    with added title, axis labels, rotated X-axis labels,
    and displaying the number of job postings on each bar.
    """
    plt.figure(figsize=(12, 8))
    top_vacancies = df["name"].value_counts().sort_values(ascending=False).head(10)
    top_vacancies.plot(kind="bar", color="skyblue")

    for i, v in enumerate(top_vacancies):
        plt.text(i, v + 0.2, str(v), ha='center', va='bottom', fontsize=10)

    plt.title("Top 10 Popular Vacancies")
    plt.xlabel("Vacancy Name")
    plt.ylabel("Number of Postings")
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.9)
    plt.show()


if __name__ == "__main__":
    d_f = setup_dataframe()
    plot_graph(d_f)
