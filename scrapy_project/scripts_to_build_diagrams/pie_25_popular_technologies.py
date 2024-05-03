import pandas as pd
import matplotlib.pyplot as plt
from setup_dataframe import setup_dataframe


def plot_graph(df):
    """
    This code creates a pie chart
    showing the top 25 most popular technologies,
    with added title, customized colors, and removed axis labels.
    """
    df_only_tech = df.drop(columns=["name", "posted_date", "company"])
    df_only_tech = df_only_tech.apply(pd.to_numeric)

    top_technologies = df_only_tech.sum().sort_values(ascending=False).head(25)

    plt.figure(figsize=(8, 10))
    top_technologies.plot(kind="pie", autopct="%1.1f%%", fontsize=12, colors=plt.cm.tab20.colors)
    plt.title("Top 25 Popular Technologies")
    plt.ylabel("")
    plt.axis("equal")
    plt.show()


if __name__ == "__main__":
    d_f = setup_dataframe()
    plot_graph(d_f)
