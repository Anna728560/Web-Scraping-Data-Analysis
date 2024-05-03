import matplotlib.pyplot as plt
from setup_dataframe import setup_dataframe


def plot_graph(df):
    """
    This code generates a horizontal bar chart
    displaying the 30 most popular technologies
    based on the frequency of occurrence in the dataset.
    """
    df_only_tech = df.drop(columns=["name", "posted_date", "company"])
    top_technologies = df_only_tech.sum().sort_values(ascending=False).head(30)

    total_technologies = top_technologies.sum()
    percentages = (top_technologies / total_technologies) * 100

    plt.figure(figsize=(12, 8))
    top_technologies.plot(kind="barh", color="skyblue")
    plt.title("Top 30 Popular Technologies")
    plt.xlabel("Technologies")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45, ha="right")

    for index, value in enumerate(top_technologies):
        plt.text(value, index, f"{round(percentages[index], 2)}%", ha="left", va="center")

    plt.grid(axis="x", linestyle="--", alpha=0.7)
    plt.show()


if __name__ == "__main__":
    d_f = setup_dataframe()
    plot_graph(d_f)
